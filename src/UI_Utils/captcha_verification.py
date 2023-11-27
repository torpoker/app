from .JoinList import *
from ..UI import captcha_dialog
from PyQt5.QtGui import QPixmap


class CaptchaDialog(QDialog):
    inputs = pyqtSignal(list)

    def __init__(self, image_data, currency):
        super(CaptchaDialog, self).__init__()
        self.image_data = image_data
        self.ui = captcha_dialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

        title_text = f"Type your {currency} address"
        self.setWindowTitle(title_text)

        label_text = self.ui.label.text()
        label_text = label_text.replace("bitcoin", currency)
        self.ui.label.setTextFormat(Qt.PlainText)
        self.ui.label.setText(label_text)

        self.ui.label_captcha.setAlignment(Qt.AlignCenter)
        captcha_pixmap = QPixmap()
        captcha_pixmap.loadFromData(image_data, 'png')
        self.ui.label_captcha.setPixmap(captcha_pixmap)
        self.ui.pushButton_submit.clicked.connect(self.validate_input)

    def validate_input(self):
        code = self.ui.lineEdit_captcha.text()
        btc_address = self.ui.lineEdit_btc_address.text()
        if code and btc_address:
            self.inputs.emit([btc_address, code])
