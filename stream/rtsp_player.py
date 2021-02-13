import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')

from gi.repository import Gst, GstVideo, GstBase

Gst.init(None)

from . import utils


class RtspPlayer:
    """
    Streams media from RTSP source.
    This class can display media from the source and take snapshot.
    """
    def __init__(self, window_id, url):
        self.window_id = window_id
        self.url = url
        self.buffer_map = None
        self.player = None
        self.info_handler = None
        self.setup_pipeline()

    def setup_pipeline(self):
        """
        Create pipeline string and launch it.
        """
        pipeline = "rtspsrc protocols=tcp location={}  name=src src. ! "\
                   "application/x-rtp, media=(string)audio"" !"\
                   "decodebin ! audioconvert ! pulsesink src. !"\
                   "application/x-rtp, media=(string)video"" !"\
                   "decodebin ! tee name=t ! queue ! videoconvert !"\
                   "videoscale ! queue ! jpegenc ! "\
                   "appsink name=sink t.! queue ! "\
                   "autovideosink".format(self.url)

        self.player = Gst.parse_launch(pipeline)
        bus = self.player.get_bus()
        bus.enable_sync_message_emission()
        bus.connect('sync-message::element', self.on_sync_message)
        bus.add_signal_watch()
        bus.connect('message', self.on_watch_message)

    def set_info_event_handler(self, handler):
        """
        Sets handler to notify media information.
        """
        self.info_handler = handler

    def on_watch_message(self, bus, msg):
        """
        This method calls when streaming started.
        """
        msg_struct = msg.get_structure()
        if msg_struct:
            if msg_struct.get_name() == 'GstMessageTag':
                codec_name = ((msg_struct["taglist"].nth_tag_name(0)))
                codec_value = msg_struct["taglist"].get_string(codec_name)
                info_name = codec_name
                c_result, info_value = codec_value
                if c_result:
                    self.info_handler(info_name, info_value)
                if codec_name == "video-codec":
                    self.info_handler(codec_name, info_value)
                    r_result, width, height = self.get_resolution()
                    if r_result:
                        info_name = "resolution"
                        info_value = "[{}x{}]".format(width, height)
                        self.info_handler(info_name, info_value)
                        bus.remove_signal_watch()

    def on_sync_message(self, _, msg):
        """
        This method when sync message arrives and prepares the window handler
        for displaying properly on GUI.
        """
        message_name = msg.get_structure().get_name()
        print(message_name)
        if message_name == "prepare-window-handle":
            win_id = self.window_id
            assert win_id
            imagesink = msg.src
            imagesink.set_window_handle(win_id)

    def stop(self):
        """
        Stops the player and destroys the player object.
        """
        self.set_state_null()
        self.player = None

    def play(self):
        """
        Plays the video.
        """
        self.player.set_state(Gst.State.PLAYING)

    def pause(self):
        """
        Pauses the video.
        """
        self.player.set_state(Gst.State.PAUSED)

    def get_resolution(self):
        """
        Used for getting media resolution using a sample from stream.
        """
        ret_val = False
        width = 0
        height = 0
        try:
            sink = self.player.get_by_name('sink')
            sample = GstBase.BaseSink.get_last_sample(sink)
            caps = Gst.Sample.get_caps(sample)
            struct = Gst.Caps.get_structure(caps, 0)
            h_result, height = Gst.Structure.get_int(struct, "height")
            w_result, width = Gst.Structure.get_int(struct, "width")
            if h_result and w_result:
                ret_val = True
        except:
            ret_val = False

        return ret_val, width, height

    def take_snapshot(self, path, file_name):
        """
        Take snapshot from last sample.

        path: path for storing image file.
        file_name: image file name.
        """
        pipelie_state = self.player.get_state(1)
        p_state = pipelie_state.state
        if p_state not in (Gst.State.PLAYING, Gst.State.PAUSED):
            print("Stream is not ready")
        else:
            try:
                sink = self.player.get_by_name('sink')
                sample = GstBase.BaseSink.get_last_sample(sink)
                image_buffer = Gst.Sample.get_buffer(sample)
                buffer_map = Gst.Buffer.map(image_buffer, Gst.MapFlags.READ)
                image_binary_data = bytearray(buffer_map.info.data)
                utils.store_image(image_binary_data, path, file_name + ".jpeg")
            except:
                print("Capturing image failed.")

    def set_state_null(self):
        self.player.set_state(Gst.State.NULL)

    def get_url(self):
        """
        Gets current URL
        """
        return self.url

    def set_url(self, source_url):
        """
        Set streaming source URL.
        source_url: The URL of streaming source, the initial value is:
            "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
        """
        if utils.validate_url(source_url, "rtsp"):
            self.url = source_url
            self.set_state_null()
            self.setup_pipeline()
            self.play()
        else:
            print("Invalid URL")
