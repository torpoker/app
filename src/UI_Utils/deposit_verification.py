from .JoinList import *
from src.connection import api
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from src.UI import btc_deposit_window


class BtcDeposit(QDialog):
    status = pyqtSignal(str)

    def __init__(self, api_obj: api.API, deposit_address, host, port, connect_ssl, min_deposit, currency, socks_ip=None, socks_port=None):
        super(BtcDeposit, self).__init__()
        self.api = api_obj
        self.socks_port = socks_port
        self.socks_ip = socks_ip
        self.connect_ssl = connect_ssl
        self.port = port
        self.override_close = True
        self.host = host

        self.ui = btc_deposit_window.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

        self.deposit_address = deposit_address

        # init view
        self.ui.lineEdit_deposit_address.setText(self.deposit_address)

        # sets currency and unit from API result
        label_text = self.ui.label_descr.text()
        label_text = label_text.replace('BTC', currency)
        self.ui.label_descr.setTextFormat(Qt.PlainText)
        self.ui.label_descr.setText(label_text)

        label_text = self.ui.label_header.text()
        label_text = label_text.replace('MINDEPOSIT', f"{min_deposit} {currency}")
        self.ui.label_header.setTextFormat(Qt.PlainText)
        self.ui.label_header.setText(label_text)

        # init thread
        self.request_thread = QtCore.QThread()

        # start 15 seconds time loop
        self.start_time_loop()

    def start_time_loop(self):
        """
        calls get/json/send every 15s until it gets status : complete
        :return:
        """
        self.s_15_timer = QtCore.QTimer()
        self.s_15_timer.timeout.connect(self.update_time)
        self.curr_time = 0
        self.override_close = False
        self.timer_pause = False
        self.s_15_timer.start(1000)
        global RETRY
        RETRY = 0

    def update_time(self):
        """
        gets called after each 1 second
        :return:
        """
        if not self.timer_pause:
            self.curr_time += 1
            self.ui.label_status.setText(f"refreshing in ({15 - self.curr_time})s")
        else:
            self.ui.label_status.setText(f"refreshing now...")
        if self.curr_time >= 15:  # counts upto 15 second before making another API request
            self.prepare_request()
            self.curr_time = 0

    def prepare_request(self):
        """
        Pause the timer and creates the API call using thread
        """
        self.curr_time = 0
        self.timer_pause = True
        self.request_ = RequestThread.RequestThread(('GET /json/send', None, None), self.api)
        self.request_.error_signal.connect(self.retry)
        self.request_.resp.connect(self.accept_data)
        self.request_.complete.connect(self.quit_thread)

        self.request_.moveToThread(self.request_thread)
        self.request_thread.started.connect(self.request_.run)
        self.request_thread.start()

    def quit_thread(self):
        try:
            self.request_thread.quit()
        except Exception as e:
            pass

    def close_thread(self):
        try:
            self.s_15_timer.stop()
            self.request_thread.quit()
        except Exception as e:
            pass

    def accept_data(self, res_list: list):
        resp = res_list[0]
        if resp and resp.get('status'):
            if resp['status'] == 'completed':
                self.curr_time = 0
                self.override_close = True
                self.close_thread()
                self.status.emit('complete')  # emit complete status to launch poker table
                self.close()
            else:
                self.curr_time = 0
                self.timer_pause = False
        else:
            self.curr_time = 0
            self.timer_pause = False

    def retry(self):
        self.timer_pause = True
        response = show_error_message()

        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(1500, loop.quit)  # wait 1.5 seconds before making the next requests
        loop.exec_()

        if response:
            self.quit_thread()
            self.timer_pause = False
            self.curr_time = 0
            self.prepare_request()
        else:
            self.override_close = True
            self.close_thread()
            self.status.emit('error')  # emit error to close dialog window in case of connection error
            self.close()

    def closeEvent(self, a0) -> None:
        if not self.override_close:
            message = QMessageBox(QMessageBox.Question, "Close Confirmation",
                                  "Are you sure you want to close this window?",
                                  QMessageBox.Yes | QMessageBox.Cancel)
            res = message.exec_()
            if res == QMessageBox.Yes:
                self.close_thread()
                self.status.emit('error')  # emit error to close dialog window in case of connection error
                self.close()
            else:
                a0.ignore()
        else:
            self.close_thread()
            self.close()
