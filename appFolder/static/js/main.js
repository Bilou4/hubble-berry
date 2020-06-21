function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "inline-block";
	evt.currentTarget.className += " active";
	
	$("#message").text(""); // deleting text in message paragraph to hide previous text
	$("#filename").text("");
}

function disable_tables(){
	$(".tablinks").prop('disabled', true);
	$("#save_in_usb").hide();
}

function enable_tables(){
	$(".tablinks").prop('disabled', false);
	$("#save_in_usb").show();
}


var the_timeout_handler = null;
const default_time_camera_warmup = 5;

$(document).ready(function(){
	document.getElementById("default_open").click(); // default tab 'photo' is opened	

	// ############ Photo ############

	$("#take_a_photo").click(function(e){
		e.preventDefault();
		$("#message").text("Photo en cours");

		disable_tables();
		$("#take_a_photo").hide();

		$.ajax({
			url:'/take_a_photo',
			type:'POST',
			dataType:"json",
			data:'exposure_photo='+$('#exposure_photo').val(),
			
			success : function(response){
				if(response.length!=0){
					$("#message").text(response.text);
					$("#filename").text(response.name);
				}
				if(response.status === "error"){
					clearTimeout(the_timeout_handler);
				}
			},
			error : function(result, status, error){
				console.log(result,status,error);
			},
		});

		the_timeout_handler = setTimeout( () => {
			enable_tables();
			$("#take_a_photo").show();
			the_timeout_handler = null;
		}, (parseFloat($('#exposure_photo').val())+default_time_camera_warmup)*1000);
	});


	// ############ Timelapse ############

	$("#take_timelapse").click(function(e){
		e.preventDefault();
		
		disable_tables();
		$("#take_timelapse").hide();
		$("#message").text("Timelapse en cours");

		$.ajax({
			url:'/take_timelapse',
			type:'POST',
			dataType:"json",
			data:'exposure_photo='+$('#exposure_photo_timelapse').val()
					+'&time_between_photos=' + $('#time_between_photos').val()
					+'&number_photos=' + $('#number_photos').val(),
			
			success : function(response){
				if(response.length!=0){
					$("#message").text(response.text);
					$("#filename").text(response.name);
				}
				if(response.status === "error"){
					clearTimeout(the_timeout_handler);
				}
			},
			error : function(result, status, error){
				console.log(result,status,error);
			},
		});

		the_timeout_handler = setTimeout( () => {
			enable_tables();
			$("#take_timelapse").show();
			the_timeout_handler = null;
		}, (parseFloat($("#calculated_time").text())+default_time_camera_warmup)*1000);
	});

	// ############ Video ############

	$("#start_video").click(function(e){
		e.preventDefault();

		disable_tables();
		$("#start_video").hide();
		$("#message").text("Vidéo en cours");
		
		$.ajax({
			url:'/start_video',
			type:'POST',
			dataType:"json",
			data:'video_time='+$("#video_time").val(),
			
			success : function(response){
				if(response.length!=0){
					$("#message").text(response.text);
					$("#filename").text(response.name);
				}
				if(response.status === "error"){
					clearTimeout(the_timeout_handler);
				}
			},
			error : function(result, status, error){
				console.log(result,status,error);
			},
		});

		the_timeout_handler = setTimeout( () => {
			enable_tables();
			$("#start_video").show();
			the_timeout_handler = null;
		}, (parseFloat($("#video_time").val())+default_time_camera_warmup)*1000);
	});

 	// ############ Calculated time ############

	$("#exposure_photo_timelapse, #number_photos, #time_between_photos").change(function() {
		var time = (parseFloat($('#exposure_photo_timelapse').val())
					+ parseFloat($('#time_between_photos').val()) ) 
					* parseFloat($('#number_photos').val());
		$("#calculated_time").text(time);
	});

	
	// ############ Save in USB ############

	$("#save_in_usb").click( (e) => {
		e.preventDefault();
		$.ajax({
			url:'/save_usb',
			type:'POST',
			dataType:"json",
			data:'',
			
			success : function(response){
				if(response.length!=0){
					$("#usb_status").text(response.text);
				}
			},
			error : function(result, status, error){
				console.log(result,status,error);
			},
		});
	});
});
