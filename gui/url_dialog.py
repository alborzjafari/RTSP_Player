from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 120)
        Dialog.setStyleSheet("background-color: rgb(2, 194, 139);")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.lineEdit.textChanged.connect(Dialog.set_url)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "New URL"))
        self.label.setText(_translate("Dialog", "Source:"))


class UrlDialog(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.ok = False
        self.url = None

    def result(self):
        """
        Returns result of the dialog.
        """
        return (self.ok, self.url)

    def set_url(self, url):
        self.url = url

    def accept(self):
        self.ok = True
        return super().accept()

    def reject(self):
        self.ok = False
        return super().reject()

    def open(self):
        ui = Ui_Dialog()
        ui.setupUi(self)
        self.exec_()
        self.show()
