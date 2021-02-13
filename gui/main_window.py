import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

from .url_dialog import UrlDialog


class Ui_MainWindow(object):
    def __init__(self):
        self.button_style_sheet = "background-color: rgb(0, 173, 118);"
        self.info_dict = dict()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(10, 61, 51);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.video_frame_widget = QtWidgets.QWidget(self.centralwidget)
        self.video_frame_widget.setObjectName("video_frame_widget")
        self.gridLayout.addWidget(self.video_frame_widget, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.playButton = QtWidgets.QPushButton(self.centralwidget)
        self.playButton.setObjectName("playButton")
        self.playButton.setStyleSheet(self.button_style_sheet)
        self.horizontalLayout.addWidget(self.playButton)

        self.pauseButton = QtWidgets.QPushButton(self.centralwidget)
        self.pauseButton.setObjectName("pauseButton")
        self.pauseButton.setStyleSheet(self.button_style_sheet)
        self.horizontalLayout.addWidget(self.pauseButton)

        self.reloadButton = QtWidgets.QPushButton(self.centralwidget)
        self.reloadButton.setObjectName("reloadButton")
        self.reloadButton.setStyleSheet(self.button_style_sheet)
        self.horizontalLayout.addWidget(self.reloadButton)

        self.info_label = QtWidgets.QLabel(self.centralwidget)
        self.info_label.setObjectName("info_label")
        self.info_label.setStyleSheet("color: rgb(55, 237, 182);")
        self.horizontalLayout.addWidget(self.info_label)

        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.screenshotButton = QtWidgets.QPushButton(self.centralwidget)
        self.screenshotButton.setObjectName("screenshotButton")
        self.screenshotButton.setStyleSheet(self.button_style_sheet)
        self.horizontalLayout.addWidget(self.screenshotButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setStyleSheet("color: rgb(0, 250, 137);")
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionExit.triggered.connect(self.exit_app)
        self.actionNew.triggered.connect(self.open_url_dialog)
        self.playButton.clicked.connect(self.play_trigger)
        self.reloadButton.clicked.connect(self.reload_trigger)
        self.pauseButton.clicked.connect(self.pause_trigger)
        self.screenshotButton.clicked.connect(self.take_snapshot_trigger)

        MainWindow.shortcut_menubar_toggle = QShortcut(QKeySequence('Ctrl+M'), MainWindow)
        MainWindow.shortcut_menubar_toggle.activated.connect(
            lambda: self.hide_menubar_trigger(MainWindow))

        MainWindow.shortcut_new_dialog = QShortcut(QKeySequence("Ctrl+N"), MainWindow)
        MainWindow.shortcut_new_dialog.activated.connect(self.open_url_dialog)
        MainWindow.shortcut_new_dialog.setEnabled(False)
        MainWindow.shortcut_close_app = QShortcut(QKeySequence('Ctrl+Q'), MainWindow)
        MainWindow.shortcut_close_app.activated.connect(self.exit_app)
        MainWindow.shortcut_close_app.setEnabled(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.playButton.setText(_translate("MainWindow", "Play"))
        self.reloadButton.setText(_translate("MainWindow", "Reload"))
        self.pauseButton.setText(_translate("MainWindow", "Pause"))
        self.screenshotButton.setText(_translate("MainWindow", "Screenshot"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.screenshotButton.setShortcut("i")
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))

    def hide_menubar_trigger(self, MainWindow):
        if self.menubar.isVisible():
            self.menubar.hide()
            MainWindow.shortcut_close_app.setEnabled(True)
            MainWindow.shortcut_new_dialog.setEnabled(True)
        else:
            self.menubar.show()
            MainWindow.shortcut_close_app.setEnabled(False)
            MainWindow.shortcut_new_dialog.setEnabled(False)

    def take_snapshot_trigger(self):
        self.video_widget.take_snapshot()

    def pause_trigger(self):
        self.video_widget.pause()
        self.reload_status_text()

    def play_trigger(self):
        self.video_widget.play()
        self.reload_status_text()

    def reload_trigger(self):
        self.video_widget.reload()
        self.reload_status_text()
        self.video_widget.adjustSize()
        self.video_widget.set_info_event_handler(self.on_get_info)

    def reload_status_text(self):
        self.statusbar.showMessage("source: " + self.video_widget.get_url())

    def open_url_dialog(self):
        url_dialog = UrlDialog()
        url_dialog.open()
        ok, url = url_dialog.result()
        if ok:
            self.video_widget.set_url(url)
            if url:
                current_url = self.video_widget.get_url()
                self.statusbar.showMessage("source: " + current_url)

    def set_video_widget(self, VideoWidget):
        """
        Sets the video widget.
        Currently there is one video widget that streams RTSP streams.
        Using this API it can be replaced with other streaming widgets.

        VideoWidget: Type of video widget.
        """
        self.video_widget = VideoWidget(parent=self.video_frame_widget)
        self.video_widget.setObjectName("video_widget")
        self.gridLayout.addWidget(self.video_widget, 0, 0, 1, 1)
        self.statusbar.showMessage("source: " + self.video_widget.get_url())
        self.video_widget.set_info_event_handler(self.on_get_info)

    def on_get_info(self, name, value):
        info_string = str()
        self.info_dict[name] = value
        for key, value in self.info_dict.items():
            info_string += "{}: {}  ".format(key, value)
        self.info_label.setText(info_string)

    def exit_app(self):
        self.video_widget.stop()
        sys.exit()

class AppWindow():
    def __init__(self, VideoWidget):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.set_video_widget(VideoWidget)

    def show(self):
        self.MainWindow.showFullScreen()
        sys.exit(self.app.exec_())
