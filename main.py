from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from qr_code_generator_ui import Ui_MainWindow

from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L

import os


basedir = os.path.dirname(__file__)


class QRCodeGeneratorApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QRCodeGeneratorApp, self).__init__()

        self.setupUi(self)
        self.loadQss()

        self.initDefaultValues()
        self.initSignalSlot()

    def loadQss(self) -> None:
        with open(os.path.join(basedir, "style.qss"), "r") as f:
            self.setStyleSheet(f.read())

    def initDefaultValues(self):
        self.versionValueSlider.setValue(1)
        self.boxSizeValueSlider.setValue(10)
        self.borderSizeValueSlider.setValue(4)

    def initSignalSlot(self) -> None:
        self.generateButton.clicked.connect(self.generateQRCode)
        self.saveButton.clicked.connect(self.saveButton_Clicked)

        sliders = [
            self.versionValueSlider,
            self.boxSizeValueSlider,
            self.borderSizeValueSlider
        ]
        for i in sliders:
            i.valueChanged.connect(lambda value: self.generateQRCode())

        self.fillColorButton.clicked.connect(self.fillColorButton_Clicked)
        self.backgroundColorButton.clicked.connect(
            self.backgroundColorButton_Clicked)

    def generateQRCode(self) -> None:
        data = self.contentText.toPlainText()
        if not data:
            self.outputLabel.clear()
            return

        version = self.versionValueSlider.value()
        if not version:
            version = None
        boxSize = self.boxSizeValueSlider.value()
        borderSize = self.borderSizeValueSlider.value()
        fillColor = self.fillColorText.text()
        backColor = self.backgroundColorText.text()

        qr = QRCode(
            version=version,
            error_correction=ERROR_CORRECT_L,
            box_size=boxSize,
            border=borderSize
        )
        qr.add_data(data)
        qr.make(fit=True)
        qrImage = qr.make_image(fill_color=fillColor, back_color=backColor)
        qrImage.save(os.path.join(basedir, "output.png"))

        self.outputLabel.setPixmap(QPixmap(os.path.join(basedir, "output.png")))

    def saveButton_Clicked(self):
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save QR Code", "qrcode.png", "Images (*.png)")
        if filePath:
            self.outputLabel.pixmap().save(filePath, "PNG")
            QMessageBox.information(
                self, "QR Code saved", "The QR Code has been saved successfully.")

    def fillColorButton_Clicked(self):
        color = self.selectColor()
        self.fillColorText.setText(color)
        self.fillColorDisplayFrame.setStyleSheet(f"background: {color}")
        self.generateQRCode()

    def backgroundColorButton_Clicked(self):
        color = self.selectColor()
        self.backgroundColorText.setText(color)
        self.backgroundColorDisplayFrame.setStyleSheet(f"background: {color}")
        self.generateQRCode()

    def selectColor(self) -> str:
        color = QColorDialog.getColor()
        if color.isValid():
            return color.name()
        return "#ffffff"

    def closeEvent(self, event: QCloseEvent):
        super().closeEvent(event)
        if os.path.exists(os.path.join(basedir, "output.png")):
            os.remove(os.path.join(basedir, "output.png"))


if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon(os.path.join(basedir, "qrcode.ico")))
    window = QRCodeGeneratorApp()
    window.show()
    app.exec()
