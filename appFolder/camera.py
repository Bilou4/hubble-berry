import time
from appFolder.base_camera import BaseCamera


class Camera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    folder = './appFolder/static/photos/'
    imgs = [open(f + '.jpg', 'rb').read() for f in [folder + '1', folder + '2', folder + '3']]

    @staticmethod
    def frames():
        while True:
            time.sleep(1)
            yield Camera.imgs[int(time.time()) % 3]
