import os
import re
import sys




try:
    from PyQt5.QtWidgets import (QMainWindow, QApplication)
    from PyQt5.QtGui import QPixmap, QImage
    from PyQt5 import QtCore
except ImportError:
    sys.exit("PyQt5 has not been found. Setup process can be found on README")
from UI import home_page
from UI_Utils import JoinList, RequestThread

CARDS_DIRECTORY = 'UI/images/41x60/'
CARDS = {}


def load_card_images():
    global CARDS
    for card_name in os.listdir(CARDS_DIRECTORY):
        card_pixmap = QPixmap()
        card_pixmap.convertFromImage(
            QImage(os.path.join(CARDS_DIRECTORY, card_name)))  # load image data from file and load into
        # memory as pixmap
        CARDS[os.path.splitext(os.path.basename(card_name))[0]] = card_pixmap


class AppHome(QMainWindow):
    def __init__(self):
        super(AppHome, self).__init__()
        self.ui = home_page.Ui_MainWindow()
        self.ui.setupUi(self)
        self.toggle_activation(0)

        load_card_images()

        self.ui.checkBox_tls.setChecked(True)
        self.ui.checkBox_tls.setEnabled(False)

        self.ui.checkBox_socks5.stateChanged.connect(self.toggle_activation)
        self.thread_pool = []
        self.ui.pushButton_connect.clicked.connect(self.get_values)
        self.ui.lineEdit_address.setFocus()

    def toggle_activation(self, state):
        if state == 2:  # activated socks5
            for widget in [self.ui.lineEdit_proxy_ip, self.ui.lineEdit_proxy_port, self.ui.label_3, self.ui.label_4]:
                widget.setVisible(True)

            self.ui.lineEdit_proxy_ip.setText('127.0.0.1')
            self.ui.lineEdit_proxy_port.setText("9050")

            self.ui.checkBox_tls.setChecked(False)
            self.ui.checkBox_tls.setEnabled(True)
        else:
            for widget in [self.ui.lineEdit_proxy_ip, self.ui.lineEdit_proxy_port, self.ui.label_3, self.ui.label_4]:
                widget.setHidden(True)
            self.ui.checkBox_tls.setChecked(True)
            self.ui.checkBox_tls.setEnabled(False)

    def get_values(self):
        host = self.ui.lineEdit_address.text()
        port = self.ui.lineEdit_address_port.text()

        socks5 = self.ui.checkBox_socks5.isChecked()
        tls = self.ui.checkBox_tls.isChecked()

        socks5_ip = self.ui.lineEdit_proxy_ip.text()
        socks5_port = self.ui.lineEdit_proxy_port.text()
        can_connect = True
        if not port.isdigit():
            can_connect = False
            return 0
        if socks5 and (socks5_port.isdigit() and socks5_ip.strip() != ''):
            socks5_port = int(socks5_port)
            can_connect = True
        elif socks5 and not (socks5_port.isdigit() or socks5_ip.strip() != ''):
            can_connect = False
            return 0
        if can_connect and (('onion' in host and len(re.findall('onion', host)) == 1 and host.endswith('.onion')) or (
            'onion' not in host and ' ' not in host and len(host) > 1)):
            self.ui.statusbar.showMessage("Connecting...")
            self.show_join_list(host=host, port=port, tls=tls, socks5=socks5, socks5_ip=socks5_ip,
                                socks5_port=socks5_port)

    def show_join_list(self, host, port, tls=False, socks5=False, socks5_ip=None, socks5_port=None):
        """
        Opens the tables list window
        :param host:
        :param port:
        :param tls:
        :param socks5:
        :param socks5_ip:
        :param socks5_port:
        :return:
        """
        self.ui.pushButton_connect.setEnabled(False)
        self.params = dict(host=host, port=int(port), connect_ssl=tls, socks5=socks5, socks_ip=socks5_ip,
                           socks_port=socks5_port, cards=CARDS)
        self.table_list = JoinList.JoinList(**self.params)
        self.table_list.back_signal.connect(self.show_status)
        self.table_list.error_signal.connect(self.show_error_message)
        self.table_list.hide_parent.connect(self.hide)

        self.ui.pushButton_connect.setDisabled(True)
        self.establish_connection()
        # self.table_list.action_init()  # conditionally shows table_list or gets back to this class

    def establish_connection(self):
        self.request_ = RequestThread.RequestThread(params=("GET /json/account", None, None),
                                                    api_obj=self.table_list.api)
        if not hasattr(self, "request_thread"):
            self.request_thread = QtCore.QThread()
            self.thread_pool.append(self.request_thread)

        self.request_.resp.connect(self.connect_table)
        self.request_.error_signal.connect(self.show_error_message)
        self.request_.complete.connect(self.pass_hide)

        self.request_.moveToThread(self.request_thread)
        self.request_thread.started.connect(self.request_.run)
        self.request_thread.start()

    def pass_hide(self):
        """
This function was important to skip the hiding of this window on `self.request_.complete.connect(self.pass_hide)`
Instead it waits for checking the final connection status after the first connection is done.

if connection is success, this window gets hidden by the `hide_parent` slot, managed directly from the already opened window.
        """
        pass

    def show_error_message(self):
        try:
            self.request_thread.quit()
            self.request_thread.disconnect()
        except Exception as e:
            pass
        finally:
            self.ui.pushButton_connect.setEnabled(True)
            resp = JoinList.show_error_message()
            if resp:
                self.establish_connection()

    def connect_table(self, resp):
        try:
            self.request_thread.quit()
            self.request_thread.disconnect()
        except Exception as e:
            pass
        finally:
            self.table_list.recv_account_status(resp, True)

    def show_status(self, message):
        self.ui.statusbar.clearMessage()
        self.ui.statusbar.showMessage(message, 10 * 1000)
        self.ui.pushButton_connect.setEnabled(True)
        self.show()

    def closeEvent(self, event) -> None:
        for thread in self.thread_pool:
            try:
                thread.quit()
                thread.disconnect()
            except Exception as e:
                pass
        return super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppHome()
    w.show()
    sys.exit(app.exec_())
