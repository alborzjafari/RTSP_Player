from PyQt5.QtWidgets import QWidget, QMainWindow

from . import utils
from .rtsp_player import RtspPlayer


class VideoWidget(QWidget):
    """
    A widget to display video.
    This class currently used for RTSP player.
    """
    def __init__(self, parent,
                 url="rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"):
        QMainWindow.__init__(self, parent)
        self.window_id = self.winId()
        self.url = url
        self.player = RtspPlayer(self.window_id, self.url)
        self.snapshot_path = "Screenshots"

    def set_info_event_handler(self, handler):
        self.player.set_info_event_handler(handler)

    def get_url(self):
        """
        Returns current URL.
        """
        return self.player.get_url()

    def set_url(self, url):
        self.player.set_url(url)
        self.url = self.player.get_url()

    def stop(self):
        if self.player:
            self.player.stop()

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def reload(self):
        """
        Reloads stream, sometimes data can't be gathered from the network and
        stream needs reloading.
        """
        self.player.set_state_null()
        self.player = None
        self.player = RtspPlayer(self.winId(), self.url)
        self.play()

    def take_snapshot(self):
        """
        Takes a snapshot from last sample.
        """
        file_name = utils.generate_snapshot_file_name()
        self.player.take_snapshot(self.snapshot_path, file_name)
