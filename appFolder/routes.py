from appFolder import app, db, logger
from appFolder.models import User, Role
from appFolder.forms import LoginForm, RegistrationForm
from appFolder.utils import gen, add_exif_tags, get_dic_of_files, move_files,\
    utils_take_photo, utils_take_timelapse, utils_take_video, PROJECT_NAME, \
    picture_directory, timelapse_directory, video_directory

from flask import render_template, flash, redirect,\
     url_for, request, Response
from flask_login import current_user, login_user, logout_user,\
    login_required
from werkzeug.urls import url_parse
from flask_babel import _

from datetime import datetime
import os

try:
    from appFolder.camera_pi import Camera
except:
    from appFolder.camera import Camera




@app.route('/video_feed')
def video_feed():
    """This stream returns the images that are going to be displayed in the web page

    Returns:
        Response: The streaming response
    """
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
@app.route('/index')
def index():
    """Render the default page for the User

    Returns:
        template: the default template according if the user is connected or not
    """
    if current_user.is_authenticated:
        return redirect(url_for('gallery'))
    return render_template('index.html', title=PROJECT_NAME + _("- Index"))

@app.route('/logout')
def logout():
    """Function to logout a user

    Returns:
        template: Returns to the default page
    """
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Function to sign in the User

    Returns:
        template: The login page if he is not already connected or the index page
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_("Invalid username or password"))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        logger.info(user.username + ' is now connected')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '': # empecher l'utilisateur de rediriger vers un site malicieux
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title=PROJECT_NAME + _("- Sign In"), form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Function to allow a new User to register

    Returns:
        template: The register page or the login page if the registration went well
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.set_default_role()
        db.session.add(user)
        db.session.commit()
        logger.info('A new user is registered => ', user.username)
        flash(_("Congratulations, you are now a registered user!"))
        return redirect(url_for('login'))
    return render_template('register.html', title=PROJECT_NAME + _("- Register"), form=form)


@app.route('/functionalities', methods=['GET','POST'])
@login_required
def functionalities():
    """Function to redirect to the functionnalities page

    Returns:
        template: If the User is an admin, he can access the page
    """
    user_role = db.session.query('name').filter(Role.id == current_user.role_id).first()
    if user_role[0] == 'admin':
        return render_template('functionalities.html', title=PROJECT_NAME + _("- Direct"), role=user_role[0])
    else:
        return redirect(url_for('preview'))
        
@app.route('/preview')
@login_required
def preview():
    """Function to redirect to the preview page

    Returns:
        template: Any user can access the preview page
    """
    user_role = db.session.query('name').filter(Role.id == current_user.role_id).first()
    return render_template("preview.html", title=PROJECT_NAME + _("- Preview"), role=user_role[0])

@app.route('/gallery')
@login_required
def gallery():
    """Function to redirect to the gallery page

    Returns:
        template: Send all pictures, timelapse and videos to the page
    """
    dic_of_files = get_dic_of_files()
    user_role = db.session.query('name').filter(Role.id == current_user.role_id).first()
    return render_template("gallery.html", title=PROJECT_NAME + _("- Gallery"), 
            role=user_role[0], photo_file=dic_of_files['photos'], 
            timelapse_file=dic_of_files['timelapse'], video_file=dic_of_files['video'])

@app.errorhandler(404)
def page_not_found(error):
    """Function to redirect to a 404 error page

    Args:
        error (404): The server did not find the requested resource. 

    Returns:
        template: The default 404 page
    """
    # note that we set the 404 status explicitly
    return render_template('404.html', title=PROJECT_NAME + _("- ERROR")), 404

@app.route('/take_a_photo', methods=['POST'])
@login_required
def take_a_photo():
    """Function to take a photo with the Rpi camera

    Returns:
        dict: text=a message to display to the User; 
                     name=name of the pictures; 
                     status=if something went wrong
    """
    try:
        photo_name = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
        exposure_photo = int(float(request.form['exposure_photo'].replace(',','.')))
        resolution = (int(request.form['resolution_photo'].split(',')[0]), int(request.form['resolution_photo'].split(',')[1]))
        iso = int(request.form['iso_photo'])
        file_format = request.form['format_photo']
        advanced_options_is_checked = True if request.form['advanced_options_checkbox']=='true' else False
        dic_forms = {
            'photo_name': photo_name,
            'exposure_photo': exposure_photo,
            'resolution': resolution,
            'iso': iso,
            'file_format': file_format,
            'advanced_options_is_checked': advanced_options_is_checked
        }
        if advanced_options_is_checked:
            brightness = int(float(request.form['brightness_photo'].replace(',','.')))
            contrast = int(float(request.form['contrast_photo'].replace(',','.')))
            sharpness = int(float(request.form['sharpness_photo'].replace(',','.')))
            saturation = int(request.form['saturation_photo'])
            rotation = int(float(request.form['rotation_photo'].replace(',','.')))
            hflip = True if request.form['hflip_photo']=='true' else False
            vflip = True if request.form['vflip_photo']=='true' else False
            exposure_compensation = int(float(request.form['exposure_compensation_photo'].replace(',','.')))
            exposure_mode = request.form['exposure_mode_photo']
            image_effect = request.form['image_effect_photo']
            meter_mode = request.form['meter_mode_photo']
            awb_mode = request.form['awb_mode_photo']
            dic_forms.update([('brightness', brightness),
                              ('contrast', contrast),
                              ('sharpness', sharpness),
                              ('saturation', saturation),
                              ('rotation', rotation),
                              ('hflip', hflip),
                              ('vflip', vflip),
                              ('exposure_compensation', exposure_compensation),
                              ('exposure_mode', exposure_mode),
                              ('image_effect', image_effect),
                              ('meter_mode', meter_mode),
                              ('awb_mode', awb_mode)
            ])
    except Exception as e:
        message_error = "[take_a_photo] " + str(e)
        logger.error(message_error)
        return {'text': message_error, 'name':"", 'status':"error"}

    logger.info('Retrieved information from form')
    return utils_take_photo(dic_forms)

@app.route('/take_timelapse', methods=['POST'])
@login_required
def take_timelapse():
    """Function to take a timelapse with the Rpi camera

    Returns:
        dict: text=a message to display to the User; 
                status=if something went wrong
     """
    try:
        exposure_photo = int(float(request.form['exposure_photo'].replace(',','.')))
        time_between_photos = int(float(request.form['time_between_photos'].replace(',','.')))
        number_photos = int(float(request.form['number_photos'].replace(',','.')))
        resolution = (int(request.form['resolution_timelapse'].split(',')[0]), int(request.form['resolution_timelapse'].split(',')[1]))
        iso = int(request.form['iso_timelapse'])
        dic_forms = {
            'exposure_photo': exposure_photo,
            'time_between_photos': time_between_photos,
            'number_photos': number_photos,
            'resolution': resolution,
            'iso': iso,
        }
    except Exception as e:
        message_error = "[take_timelapse] " + str(e)
        logger.error(message_error)
        return {'text': message_error, 'name':"", 'status':"error"}

    logger.info('Retrieved information from form')
    return utils_take_timelapse(dic_forms)


@app.route('/start_video', methods=['POST'])
@login_required
def start_video():
    """Function to take a video with the Rpi camera

    Returns:
        dict: text=a message to display to the User; 
                name=video name;
                status=if something went wrong
      """
    try:
        video_time = int(float(request.form['video_time'].replace(',','.')))
        video_name = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
        resolution = (int(request.form['resolution_video'].split(',')[0]),int(request.form['resolution_video'].split(',')[1]))
        dic_forms = {
            'video_time': video_time,
            'video_name': video_name,
            'resolution': resolution,
        }
    except Exception as e:
        message_error = "[start_video] " + str(e)
        logger.error(message_error)
        return {'text': message_error, 'name':"", 'status':"error"}

    logger.info('Retrieved information from form')
    return utils_take_video(dic_forms)



@app.route('/save_usb', methods=['POST'])
@login_required
def save_usb():
    """Function to save files in the USB key

    Returns:
        dictionnary: text=a message to inform the User
    """
    path_to_usb = "/media/pi/HUBBLE_SAVE/camera/"
    # TODO: check for possibility to mount the usb key
    if os.path.exists(path=path_to_usb):
        move_files(picture_directory, path_to_usb+'pictures')
        logger.info('I moved pictures')
        move_files(timelapse_directory, path_to_usb+'timelapse')
        logger.info('I moved timelapse')
        move_files(video_directory, path_to_usb+'video')
        logger.info('I moved video')
        return {'text': _("Files have been transferred")}
    else:
        return {'text': _("No USB key detected")}

@app.route('/messier')
@login_required
def messier():
    """Function to render the messier's catalog page

    Returns:
        template: The messier web page
    """
    user_role = db.session.query('name').filter(Role.id == current_user.role_id).first()
    return render_template("messier.html", title=PROJECT_NAME + _("- Messier's catalog"), role=user_role[0])




# TODO ==> camera integration
# https://picamera.readthedocs.io/en/release-1.13/api_camera.html#piframeraterange

# TODO ==> cf splitter (plusieurs ports)

