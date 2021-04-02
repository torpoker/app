import inspect
from functools import partial

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt, QSize, QObject, QEvent
from PyQt5.QtGui import QFont, QResizeEvent
from PyQt5.QtWidgets import (QMainWindow, QTableWidgetItem, QDialog, QLabel, QPushButton, QShortcut,
                             QPlainTextEdit,
                             QVBoxLayout)

from UI import tables_list, popup
from UI_Utils import table_handling, PokerTable, RequestThread
from UI_Utils.alert import show_message, show_error_message, show_request_status
from UI_Utils.captcha_verification import CaptchaDialog
from UI_Utils.deposit_verification import BtcDeposit
from connection import api

ERROR_MSG = "<h3>Error</h3>"
ERROR_POPUP_TITLE = "ERROR"


class IPPop(QDialog):
    value = pyqtSignal(int)

    def __init__(self, max_amt, min_amt):
        super(IPPop, self).__init__()
        self.ui = popup.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

        self.setMinimumSize(QSize(350, 180))
        self.setMaximumSize(QSize(350, 180))

        self.min_amt = int(min_amt)
        self.max_amt = int(max_amt)

        label_text = self.ui.label.text()
        label_text = label_text.replace('min', str(self.min_amt)).replace('max', str(self.max_amt))
        self.ui.label.setText(label_text)

        self.close_override = False

        self.ui.pushButton_submit.clicked.connect(self.validate)

    def validate(self):
        amt = self.ui.lineEdit_btc_amt.text()
        if amt.isdigit():
            amt = int(amt)
            if self.min_amt <= amt <= self.max_amt:
                self.close_override = True
                self.value.emit(amt)
                self.close()
            else:
                show_message("Invalid input", f"Enter value  between {self.min_amt} and {self.max_amt}", 'info')
        else:
            show_message("Invalid input", f"Enter value  between {self.min_amt} and {self.max_amt}", 'info')

    def closeEvent(self, ev: 'QEvent') -> None:
        if self.close_override:
            usr_res = True
        else:
            usr_res = show_message("Close Confirmation", "Are you sure you want to close this window?", 'close_confirm')
        if usr_res:
            self.close()
        else:
            ev.ignore()


class CookiesManager(QDialog):
    return_cookie = pyqtSignal(str)

    def __init__(self, cookie_value='', mode='get'):
        super(CookiesManager, self).__init__()
        self.setWindowTitle("Copy Cookie!")
        self.setWindowModality(Qt.ApplicationModal)

        self.cookie_value = cookie_value
        self.vertical_layout = QVBoxLayout(self)
        self.mode = mode
        if mode == 'get':
            self.label_header = QLabel("Your current session cookie is as follows:", self)
        else:
            self.label_header = QLabel("Set Cookie Value:\n(close the window after complete)", self)
        self.label_header.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_header.setFont(font)
        self.label_header.setStyleSheet("color: white;")
        self.label_header.setWordWrap(True)
        self.vertical_layout.addWidget(self.label_header)

        self.plain_text_edit = QPlainTextEdit(self)
        self.vertical_layout.addWidget(self.plain_text_edit)
        self.plain_text_edit.setFont(font)
        self.setObjectName("Dialog")
        self.setMaximumSize(QSize(360, 250))
        self.setStyleSheet(
            "#Dialog{\nbackground-color: qlineargradient(spread:pad, x1:0.489, y1:0.0113636, x2:0.506, y2:1, "
            "stop:0 rgba(72, 72, 72, "
            "255), stop:1 rgba(30, 30, 30, 255));\n}")

        self.show_cookieValue()

    def show_cookieValue(self):
        self.plain_text_edit.setPlainText(self.cookie_value)

    def closeEvent(self, event) -> None:
        if self.mode == 'get':
            self.close()
        else:  # when mode = set
            cookie = self.plain_text_edit.toPlainText()
            if cookie:
                self.return_cookie.emit(cookie)
            else:
                event.accept()
                self.close()


class JoinList(QMainWindow):
    back_signal = pyqtSignal(str)
    hide_parent = pyqtSignal(str)
    error_signal = pyqtSignal()

    def __init__(self, host, port, connect_ssl, socks_ip=None, socks_port=None, socks5=None, cards: dict = None):
        super(JoinList, self).__init__()

        self.ui = tables_list.Ui_MainWindow()
        self.ui.setupUi(self)

        self.to_close = False
        self.socks5 = socks5
        self.socks_port = socks_port
        self.socks_ip = socks_ip
        self.port = port
        self.host = host
        self.connect_ssl = connect_ssl
        self.CARDS = cards
        self.thread_pool = []

        # hide tables widget as long as there's no table [retain table size even if it is hidden]
        size_policy = self.ui.tableWidget_game_tables.sizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        self.ui.tableWidget_game_tables.setSizePolicy(size_policy)
        self.ui.tableWidget_game_tables.setVisible(False)
        self.ui.pushButton_refresh_account.clicked.connect(self.refresh_account)
        self.ui.pushButton_cashout.clicked.connect(self.cash_out)

        self.unit = ""  # to be filled after successful call of /json/tables

        # creating short-cut to manually save RUNTIME cookie and get RUNTIME cookie
        self.cookie_getter = QShortcut('Ctrl+T', self)
        self.cookie_getter.activated.connect(self.get_cookie)
        self.cookie_setter = QShortcut('Ctrl+N', self)
        self.cookie_setter.activated.connect(self.set_cookie)
        self.api = api.API(RUNTIME_COOKIE='', host=self.host, port=self.port, tls=self.connect_ssl,
                           socks5_ip=self.socks_ip, socks5=self.socks5,
                           socks5_port=self.socks_port)
        if hasattr(self, 'ui'):
            self.ui.tableWidget_game_tables.installEventFilter(self)

    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a1.__class__ == QResizeEvent and hasattr(self, 'ui'):
            table_handling.update_table_size(self.ui.tableWidget_game_tables)
        return super(JoinList, self).eventFilter(a0, a1)

    def user_retry(self, call_name, params=None):
        try:
            if call_name == 'tables':
                self.tables_thread.quit()
                self.tables_thread.disconnect()
            else:
                self.request_thread.quit()
                self.request_thread.disconnect()
        except Exception as e:
            pass
        response = show_error_message()

        if call_name == 'tables':
            if response:
                self.available_display_tables()
            else:
                self.go_back()
        elif call_name == 'cashout':
            if response:
                self.cash_out()
            else:
                self.go_back()
        elif call_name == 'get_account' and response:
            self.prepare_account_check()
        elif call_name == 'join_table' and response:
            self.join_table(*params)
        elif call_name == 'get_captcha' and response:
            self.request_captcha()
        elif call_name == 'post_captcha' and response:
            self.prepare_captcha_post_data(*params)
        elif call_name == 'confirm_join' and response:
            self.prepare_accept_amount_value(*params)

    def action_init(self, res='call', value=None):
        # window initialization for initial request
        if res == 'call':
            self.prepare_account_check()
            return 0
        elif res == 'get':
            res = value
        if res is None:
            self.error_signal.emit()
        else:
            try:
                self.available_display_tables()
                self.hide_parent.emit("")
                self.ui.pushButton_playnow.clicked.connect(self.request_captcha)
                self.show()
                self.update()
            except Exception as e:
                self.go_back()

    def go_back(self):
        """
        takes back control to Home window
        """
        self.close_all_thread()
        self.back_signal.emit("")
        self.close()

    def set_cookie(self):
        """
        functions dually for showing cookie window and for setting the cookie for the next connection
        :return:
        """
        self.cookie_window = CookiesManager(mode='set')
        self.cookie_window.return_cookie.connect(self.update_cookie)
        self.cookie_window.show()

    def update_cookie(self, cookie_value):
        self.api.set_cookie(cookie_value)
        self.ui.statusbar.showMessage("New cookie loaded", 2 * 1000)
        self.prepare_account_check()

    def get_cookie(self):
        """
        If RUNTIME_COOKIE is not empty string literal, then only it show a little popup to copy paste cookies
        else, it'll not show any pop-up
        :return:
        """
        RUNTIME_COOKIE = self.api.get_cookie()
        if RUNTIME_COOKIE:
            self.cookie_dialog = CookiesManager(RUNTIME_COOKIE)
            self.cookie_dialog.show()

    def close_thread(self):
        try:
            self.request_thread.quit()
            self.request_thread.disconnect()
        except Exception as e:
            pass

    def prepare_account_check(self):
        """
        Refresh user account status
        """
        self.request_acc = RequestThread.RequestThread(params=('GET /json/account', None, None), call_dict=None,
                                                    api_obj=self.api)
        if not hasattr(self, 'request_thread'):  # don't spawn new thread if there's already one
            self.request_thread = QtCore.QThread()
            self.thread_pool.append(self.request_thread)
        self.request_acc.resp.connect(self.recv_account_status)
        self.request_acc.error_signal.connect(partial(self.user_retry, 'get_account'))
        self.request_acc.complete.connect(self.close_thread)
        self.request_acc.moveToThread(self.request_thread)
        self.request_thread.started.connect(self.request_acc.run)
        self.request_thread.start()
        self.ui.statusbar.showMessage("refreshing account...", 10*60*1000)  # show refreshing status for max 10
        # minutes (can be cleared before)

    def recv_account_status(self, resp_list, first_call=False):
        self.ui.statusbar.clearMessage()  # clear refreshing status
        resp = resp_list[0]
        if resp and resp.get('account'):
            self.ui.pushButton_playnow.setVisible(False)
            self.ui.frame_my_acc.setVisible(True)
            self.no_account = False
            self.user_has_account(resp['account'])  # shows user name, stack and cashout button
        elif not resp:  # if resp is {} or None
            self.no_account = True
            if resp is None:
                self.action_init('get', None)
            else:
                self.ui.frame_my_acc.setVisible(False)
                self.ui.pushButton_playnow.setVisible(True)
                if first_call:
                    self.action_init('get', 1)

    def refresh_account(self):
        """
        called when user press the refresh account icon
        """
        self.prepare_account_check()

    def user_has_account(self, acc_details):
        """
        If there's a good response from /json/account
        {'account':{"name":"...", stack:"..."}} considered as good response
        :return:
        """
        self.ui.pushButton_playnow.setVisible(False)  # hide play now button
        stack_value = str(acc_details['stack']) if str(acc_details['stack']).isdigit() else '0'
        name = acc_details['name']

        self.ui.label_stack.setTextFormat(Qt.PlainText)
        self.ui.label_stack.setText(stack_value + self.unit)  # show stack value + currency unit (empty string when blank)
        self.ui.label_username.setTextFormat(Qt.PlainText)
        self.ui.label_username.setText(name)

        if int(stack_value) >= 100:  # cash out when stack value more than or equal to 100
            self.ui.pushButton_cashout.setText("Cashout")
        else:
            self.ui.pushButton_cashout.setText("Logout")

        self.ui.pushButton_cashout.setStatusTip(self.ui.pushButton_cashout.text())

    def cash_out(self):
        """
        To logout or cashout and get back to home window
        :return:
        """
        self.request_ = RequestThread.RequestThread(('GET /json/cashout', None, None), self.api)
        self.request_.resp.connect(self.do_cashout)
        self.request_.error_signal.connect(partial(self.user_retry, 'cashout'))
        self.request_.complete.connect(self.close_thread)
        self.request_.moveToThread(self.request_thread)
        self.request_thread.started.connect(self.request_.run)
        self.request_thread.start()
        show_request_status(self)

    def do_cashout(self, value_list):
        self.ui.statusbar.clearMessage()
        resp = value_list[0]
        if resp == {}:
            # redirect to main window after cashout
            self.go_back()

    def close_table_thread(self):
        try:
            self.tables_thread.quit()
            self.tables_thread.disconnect()
        except Exception:
            pass

    def available_display_tables(self):
        """
        First connection making for the application to the host provided in the Home window
        Get tables to join and display them with blinds and seats
        :return:
        """
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)

        if not hasattr(self, 'request_thread'):
            self.tables_thread = QtCore.QThread()
            self.thread_pool.append(self.tables_thread)
        self.request_ = RequestThread.RequestThread(('GET /json/tables', None, None), self.api)
        self.request_.moveToThread(self.tables_thread)
        if calframe[1][3] == 'action_init':  # to get the caller function (action_init for first call from home screen)
            self.request_.resp.connect(partial(self.display_tables, True))
        else:
            self.request_.resp.connect(partial(self.display_tables, False))
        self.request_.error_signal.connect(partial(self.user_retry, 'tables'))
        self.request_.complete.connect(self.close_table_thread)
        self.tables_thread.started.connect(self.request_.run)
        self.tables_thread.start()
        self.ui.statusbar.showMessage("refreshing tables...", 10*60*1000)  # show refreshing status for max 10 minutes (can be cleared before)

    def display_tables(self, first_call, resp):
        table_ = resp[0]
        if table_ and 'tables' in table_:
            self.ui.statusbar.clearMessage()  # clear refreshing status
            self.ui.tableWidget_game_tables.setVisible(True)  # initially (at start of application) table kept hidden, statement to show table again
            table_handling.delete_all_rows(self.ui.tableWidget_game_tables)  # delete all rows before adding new ones [prevents duplication]
            table_handling.update_table_size(self.ui.tableWidget_game_tables)  # update table size and make it's adjust with window size
            table_: dict
            tables_to_join = table_['tables']

            self.unit = table_.get('unit') if table_.get('unit') else ''
            self.currency = table_.get('currency') if table_.get('currency') else ''
            self.min_deposit = table_.get('mindeposit') if table_.get('mindeposit') else ''

            for tables in tables_to_join:
                tables: dict
                table_handling.add_row_all_table(self.ui.tableWidget_game_tables)  # add an empty row
                row_count = self.ui.tableWidget_game_tables.rowCount()
                self.ui.tableWidget_game_tables.setItem(row_count - 1, 0, QTableWidgetItem(str(tables['name'])))  # Name

                sb = tables['sb']
                bb = tables['bb']  # used in PokerTable
                table_id = tables['id']
                if None in [sb, bb, table_id] or not (
                        all(True if str(item).isdigit() else False for item in [sb, bb, table_id])):
                    continue
                blind = f"{tables['sb']}/{tables['bb']}"
                online = tables.get('online') if tables.get('online') else '0'

                self.ui.tableWidget_game_tables.setItem(row_count - 1, 1,
                                                        QTableWidgetItem(f"{blind}{self.unit}"))  # Blind
                self.ui.tableWidget_game_tables.setItem(row_count - 1, 2,
                                                        QTableWidgetItem(f"{online}/{tables['seats']}"))  # Seat

                button = table_handling.set_cell_widget_all(self.ui.tableWidget_game_tables, row_count - 1, 3)
                button: QPushButton

                button.clicked.connect(partial(self.join_table, table_id, bb))
        else:
            if first_call:
                self.go_back()  # go back to home screen when there's no tables to display (error)

    def join_table(self, table_id, bb):
        """
        Called when pressed "Join" button on table

        redirect to table as spectator when there's no account , but if not,
        display a popup/window (see attached) with min/max amount to join the table and an input number to type the amount
        :param bb:
        :param table_id: table id to join (int)
        :return:
        """
        self.ui.statusbar.clearMessage()
        self.bb = bb
        self.table_id = table_id
        if self.no_account:
            # if there's no account so user joins directly as spectator
            self.launch_poker_table(spectator=True)
        else:
            self.request_ = RequestThread.RequestThread(
                params=('POST /json/table/{table_id}/join', None, {'table_id': self.table_id}),
                api_obj=self.api)
            self.request_.resp.connect(self.do_join_table)
            self.request_.complete.connect(self.close_thread)
            self.request_.error_signal.connect(partial(self.user_retry, 'join_table', (table_id, bb)))
            self.request_.moveToThread(self.request_thread)
            self.request_thread.started.connect(self.request_.run)
            self.request_thread.start()
            show_request_status(self)

    def do_join_table(self, value_list):
        self.ui.statusbar.clearMessage()
        res = value_list[0]
        if res:
            if res.get('redirect'):
                self.launch_poker_table(spectator=False)  # player is already on table, redirecting directly
            elif not res.get('redirect'):
                min_amt = str(res['min'])
                max_amt = str(res['max'])
                if min_amt.isdigit() and max_amt.isdigit():  # checks if boundary limits are integers
                    self.input_popup = IPPop(max_amt, min_amt)
                    self.input_popup.value.connect(self.prepare_accept_amount_value)
                    self.input_popup.show()
        else:
            self.ui.statusbar.showMessage("Cannot join table", 4 * 1000)  # show this for 4 secs

    def prepare_accept_amount_value(self, value: int):
        """
        If user did not have an account and user pressed Join button on table.
        And has entered an amount to join the table
        :param value:
        :return:
        """
        body_bytes = f"amount={value}".encode('ascii')
        self.request_ = RequestThread.RequestThread(
            ('POST /json/table/{table_id}/join/confirm', body_bytes, {'table_id': self.table_id}),
            api_obj=self.api)
        self.request_.resp.connect(self.confirm_join)
        self.request_.complete.connect(self.close_thread)
        self.request_.error_signal.connect(partial(self.user_retry, 'confirm_join', (value,)))

        self.request_.moveToThread(self.request_thread)
        self.request_thread.started.connect(self.request_.run)
        self.request_thread.start()

        show_request_status(self)

    def confirm_join(self, res_list: list):
        self.ui.statusbar.clearMessage()
        res = res_list[0]
        if res is not None and res.get('table'):
            if res.get('table') == self.table_id:  # self.table_id from join_table
                self.launch_poker_table(spectator=False)  # self.bb = bb from join_table
            else:
                show_message(ERROR_POPUP_TITLE, ERROR_MSG, 'error')
        elif res is None:
            show_message(ERROR_POPUP_TITLE, ERROR_MSG, 'error')

    def request_captcha(self):
        """
        called when user do not have an account, and user presses the PlayNow button
        :return:
        """
        params = ('GET /json/join', None, None)
        if not hasattr(self, 'request_thread'):  # don't spawn new thread if there's already one
            self.request_thread = QtCore.QThread()
            self.thread_pool.append(self.request_thread)
        self.request_ = RequestThread.RequestThread(params, self.api)
        self.request_.resp.connect(self.open_captcha_window)
        self.request_.error_signal.connect(partial(self.user_retry, 'get_captcha'))
        self.request_.complete.connect(self.close_thread)
        self.request_.moveToThread(self.request_thread)
        self.request_thread.started.connect(self.request_.run)
        self.request_thread.start()

        show_request_status(self)

    def open_captcha_window(self, image_data_list: list):
        self.ui.statusbar.clearMessage()
        image_data = image_data_list[0]
        if image_data is not None:
            self.captcha_dialog = CaptchaDialog(image_data,self.currency)
            self.captcha_dialog.inputs.connect(self.prepare_captcha_post_data)
            self.captcha_dialog.show()

    def prepare_captcha_post_data(self, input_args):
        self.captcha_dialog.close()
        btc_address = input_args[0]
        captcha_code = input_args[1]
        body_bytes = f"address={btc_address}&captcha={captcha_code}".encode('ascii')
        self.request_ = RequestThread.RequestThread(('POST /json/send', body_bytes, None), api_obj=self.api)

        self.request_.resp.connect(self.post_captcha)
        self.request_.error_signal.connect(partial(self.user_retry, 'post_captcha', (input_args,)))
        self.request_.complete.connect(self.close_thread)

        self.request_.moveToThread(self.request_thread)
        self.request_thread.started.connect(self.request_.run)
        self.request_thread.start()
        show_request_status(self)

    def post_captcha(self, res_list: list):
        self.ui.statusbar.clearMessage()
        res = res_list[0]
        if res and res.get('address'):
            address_for_deposit = res['address']
            self.launch_btc_deposit_window(address_for_deposit)
        else:
            show_message(ERROR_POPUP_TITLE, ERROR_MSG, 'error')

    def launch_btc_deposit_window(self, deposit_address):
        """
        launch dialog to show deposit address and incase of error, user can retry to re-launch this dialog
        by pressing retry on error message, pressing cancel will redirect control to
        """
        self.btc_deposit = BtcDeposit(api_obj=self.api, deposit_address=deposit_address, host=self.host, port=self.port, connect_ssl=self.connect_ssl,
                                      socks_ip=self.socks_ip,
                                      socks_port=self.socks_port, currency=self.currency, min_deposit=self.min_deposit)
        self.btc_deposit.status.connect(self.recv_verification_status)
        self.btc_deposit.show()

    def recv_verification_status(self, status):
        if status == 'complete':
            self.prepare_account_check()
        self.ui.pushButton_playnow.setEnabled(True)

    def launch_poker_table(self, spectator=True):
        if not hasattr(self, 'table_id'):
            self.table_id = None
        self.poker_table = PokerTable.PokerTable(api_obj=self.api, connect_ssl=True, host=self.host, port=self.port,
                                                 table_id=self.table_id,
                                                 bb=self.bb, socks5=self.socks5, socks_ip=self.socks_ip,
                                                 socks_port=self.socks_port,
                                                 parent_window=self, cards=self.CARDS, currency_unit=self.unit, spectator=spectator)
        self.poker_table.exit_table.connect(self.quit_table)
        self.close_all_thread()
        self.hide()
        self.poker_table.showNormal()

    def close_all_thread(self):
        for thread in self.thread_pool:
            try:
                thread.quit()
                thread.disconnect()
            except Exception as e:
                pass

    def quit_table(self):
        """
        slot to quit poker table and open tables list, refreshes account
        """
        try:
            self.poker_table.close()
            self.prepare_account_check()  # refresh accounts
            self.available_display_tables()  # refresh tables
        except Exception as e:
            pass
        finally:
            self.show()

    def closeEvent(self, event: 'QEvent') -> None:
        if event.spontaneous():
            res = show_message("Close Confirmation", "Are you sure you want to quit torpoker?", 'close_confirm')
            if res:
                self.close_all_thread()
                self.close()
            else:
                event.ignore()
        else:
            self.close_all_thread()
            self.close()
