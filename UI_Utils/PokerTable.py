import sys
from functools import partial
from typing import Dict

try:
    try:
        from PyQt5 import QtMultimedia

        MULTIMEDIA_PACKAGE = True
    except ImportError:
        MULTIMEDIA_PACKAGE = False
    from PyQt5 import QtCore
    from PyQt5.QtCore import Qt, pyqtSignal, QRegularExpression, QThread, QTimer, QUrl
    from PyQt5.QtGui import QPixmap, QImage, QIcon
    from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QLabel, QProgressBar, QFrame, QPushButton, QSpinBox, QSlider,
                                 QSpacerItem, QApplication)
    from .alert import show_error_message, show_message, show_request_status
except ImportError:
    sys.exit("PyQt5 has not been found. Setup process can be found on README")

from UI import table_window
from UI_Utils import chat_widget, RequestThread
from connection import api

CARDS = {}

CONTENT_TYPE_FORM = "application/x-www-form-urlencoded"
ERROR_MSG = "<h3>Error</h3>"
ERROR_POPUP_TITLE = "ERROR"
TABLE_REFRESH_TIME = 15
PROGRESS_BAR_MAX = 120

BEEP_SOUND_FILE = "UI/sounds/beep-26.wav"
MUTE_ICON = "UI/images/fkzfaalief3i.png"
UNMUTE_ICON = "UI/images/dhezhynokidy.png"


def beep_sound():
    if MULTIMEDIA_PACKAGE:
        sound_obj = QtMultimedia.QSound(BEEP_SOUND_FILE)
        sound_obj.play(BEEP_SOUND_FILE)


class PokerTable(QMainWindow):
    exit_table = pyqtSignal()

    def __init__(self, api_obj: api.API, connect_ssl, host, port, table_id, bb,
                 socks_ip, socks_port,
                 socks5, parent_window, cards, spectator: bool, currency_unit: str):
        """
        :type connect_ssl: bool
        :type socks5: bool
        :type cards: dict
        """
        super(PokerTable, self).__init__()
        self.spectator = spectator
        self.currency_unit = currency_unit
        self.parent_window = parent_window
        self.api = api_obj
        self.socks5 = socks5
        self.socks_port = socks_port
        self.socks_ip = socks_ip
        self.connect_ssl = connect_ssl
        self.bb = bb
        self.table_id = table_id
        self.port = port
        self.host = host
        self.cards = cards
        self.thread_pool = []  # used to store reference to all newly created threads
        self.close_overrider = False  # decides whether to show messsage box or not

        global CARDS
        CARDS = self.cards

        self.ui = table_window.Ui_MainWindow()
        self.ui.setupUi(self)
        self.curr_progress_bar = self.ui.progressBar_pl_1

        # signals
        self.ui.lineEdit_chat.returnPressed.connect(self.prepare_message_send)
        # [!] call, fold and raise request
        self.ui.pushButton_call.clicked.connect(partial(self.CRF, 'call'))
        self.ui.pushButton_fold.clicked.connect(partial(self.CRF, "fold"))
        self.ui.pushButton_raise.clicked.connect(partial(self.CRF, "raise"))
        self.ui.pushButton_quit.clicked.connect(self.prepare_quit_table)

        # change in input amt will be retained in the next turn
        self.ui.spinBox.valueChanged.connect(self.change_input_amt)

        # [!] set size policy for all other widgets
        self.set_size_retain_policy()

        # [!] HIDE buttons at start
        self.hide_action_buttons()
        # [!] Hide all Dealer buttons
        for label in self.findChildren(QLabel):
            label: QLabel
            if label.objectName().endswith('dealer'):
                label.setVisible(False)

        self.hide_show()

        # prepare sound file for sound at myturn=true
        self.sound_is_muted = False
        self.ui.pushButton_sound.setIcon(QIcon(UNMUTE_ICON))
        if MULTIMEDIA_PACKAGE:
            self.ui.pushButton_sound.clicked.connect(self.mute_sound)
        else:  # if multimedia package not found
            self.mute_sound()  # set button icon to mute
            self.ui.pushButton_sound.setDisabled(True)  # set button disabled

        # [!] initialize thread
        self.request_thread = QtCore.QThread()
        self.thread_pool.append(self.request_thread)

        if not self.spectator:
            self.ui.statusbar.clearMessage()
            self.ui.statusbar.showMessage("Joining table...", 20 * 60 * 1000)
        # [!] Sets plain text for all labels accepting API data
        self.set_plain_text_format()
        # [!] table update timer
        self.start_time_loop()

    def hide_action_buttons(self):
        self.ui.pushButton_raise.setVisible(False)
        self.ui.pushButton_fold.setVisible(False)
        self.ui.pushButton_call.setVisible(False)
        self.ui.spinBox.setVisible(False)
        self.ui.horizontalSlider_amt.setVisible(False)

    def mute_sound(self):
        try:
            if self.sound_is_muted:
                self.ui.pushButton_sound.setIcon(QIcon(UNMUTE_ICON))
                self.sound_is_muted = False
            else:
                self.ui.pushButton_sound.setIcon(QIcon(MUTE_ICON))
                self.sound_is_muted = True
        except (FileNotFoundError, FileExistsError):
            self.ui.pushButton_sound.setIcon(QIcon(MUTE_ICON))
            self.sound_is_muted = True

    def progress_bar_timer(self, progressbar: QProgressBar):
        self.m_2_countdown = QTimer()
        self.m_2_countdown.timeout.connect(partial(self.update_progress_bar_value, progressbar))
        self.m_2_countdown.start(1000)

    def update_progress_bar_value(self, progressbar: QProgressBar, set_value=None):
        if set_value is not None:
            self.progress_curr_time = set_value  # after each 15 sec this function called from API results and the
            # current timer countdown gets corrected
        if self.progress_curr_time > 0:
            self.progress_curr_time -= 1  # update after each 1 sec and decrease the time count from 2 mins to 0 sec gradually
        else:
            self.progress_curr_time = 0
            self.m_2_countdown.stop()
        progressbar.setValue(self.progress_curr_time)
        self.update()

    def set_plain_text_format(self):
        # format for name labels
        regex_label_name = QRegularExpression("label_pl_[1-6]_name")
        for label_name in self.findChildren(QLabel, regex_label_name, Qt.FindChildrenRecursively):
            label_name: QLabel
            label_name.setTextFormat(Qt.PlainText)

        # format for stack of each player
        regex_label_btc = QRegularExpression("label_pl_[1-6]_btc")
        for label_btc in self.findChildren(QLabel, regex_label_btc, Qt.FindChildrenRecursively):
            label_name: QLabel
            label_btc.setTextFormat(Qt.PlainText)

        # format for bet amount of each player
        regex_label_bet = QRegularExpression("label_pl_[1-6]_bet_amt")
        for label_bet in self.findChildren(QLabel, regex_label_bet, Qt.FindChildrenRecursively):
            label_name: QLabel
            label_bet.setTextFormat(Qt.PlainText)

        # for pot and result label
        self.ui.label_result.setTextFormat(Qt.PlainText)
        self.ui.label_pot.setTextFormat(Qt.PlainText)

    def set_size_retain_policy(self):
        """
        retain size for all widgets that may need to be hidden
        :return: None
        """
        widget_types = [QLabel, QProgressBar, QFrame, QPushButton, QSpinBox, QSlider, QSpacerItem]
        for widget in widget_types:
            for parent_widgets in self.findChildren(widget, options=Qt.FindChildrenRecursively):
                size_policy = parent_widgets.sizePolicy()
                size_policy.setRetainSizeWhenHidden(True)
                parent_widgets.setSizePolicy(size_policy)

    def prepare_quit_table(self):
        params = ('GET /json/table/{table_id}/quit', None, {'table_id': self.table_id})
        self.request_ = RequestThread.RequestThread(params, self.api)
        self.request_.moveToThread(self.request_thread)
        self.request_.resp.connect(self.quit_table)
        self.request_.error_signal.connect(partial(self.user_retry, 'quit_table'))
        self.request_.complete.connect(self.close_request_thread)
        self.request_thread.started.connect(self.request_.run)
        self.request_thread.start()
        show_request_status(self)

    def quit_table(self, res_list: list):
        self.ui.statusbar.clearMessage()
        res = res_list[0]
        if res is not None and res == {}:
            self.close_timers()
            self.close_all_threads()
            self.close_overrider = True
            self.close()
            self.exit_table.emit()  # signal to close this window and show the join list
        else:
            show_message(ERROR_POPUP_TITLE, ERROR_MSG, 'error')

    # hide/display specific widgets for player
    def hide_show(self, show=False, pos=None):
        for i in range(1, 7):
            pl_frame = self.findChildren(QFrame, f"frame_pl_{i}")[0]
            try:
                if show and pos == i:
                    pl_frame.setVisible(True)
                elif (not show and not pos) or (not show and pos == i):
                    pl_frame.setVisible(False)
                if i in [1, 4]:  # hide/show progress bar for player 1 and player 4, rest of the progress bars get
                    # hidden with the frame_pl_{n}
                    progress_bar = self.findChild(QProgressBar, f'progressBar_pl_{i}')
                    clock_icon = self.findChild(QLabel, f"clock_label_{i}", Qt.FindChildrenRecursively)
                    if show and pos == i:
                        progress_bar.setVisible(True)
                        clock_icon.setVisible(True)
                    elif (not show and not pos) or (not show and pos == i):
                        progress_bar.setVisible(False)
                        clock_icon.setVisible(False)
                frame_map = {2: 16, 3: 19, 5: 17, 6: 15}  # hides all frames for players [2,3,5,6]
                if i in frame_map:
                    frame = self.findChild(QFrame, f"frame_{frame_map[i]}")
                    if show and pos == i:
                        frame.setVisible(True)
                    elif not show and not pos:
                        frame.setVisible(False)
                    elif not show and pos == i:
                        frame.setVisible(False)
            except (AttributeError, KeyError):
                if show_message(ERROR_POPUP_TITLE, ERROR_MSG, 'warning'):
                    self.hide_show(show, pos)
        if show is False and pos is None:
            self.ui.frame_table_top.setVisible(False)

    def update_player_view(self, players):
        frame = self.findChild(QFrame, f'frame_pl_{players[0]}', options=Qt.FindChildrenRecursively)
        frame.setVisible(False)
        self.hide_show(pos=int(players[0]))

    def update_progressbar(self, players, mode='hide'):
        for player_index, player in enumerate(players, 1):
            progress_bar = self.findChild(QProgressBar, f"progressBar_pl_{player}", Qt.FindChildrenRecursively)
            clock_icon = self.findChild(QLabel, f"clock_label_{player}", Qt.FindChildrenRecursively)
            if mode == 'show':
                progress_bar.setVisible(True)
                clock_icon.setVisible(True)
            else:
                progress_bar.setHidden(True)
                clock_icon.setHidden(True)

    def update_player_cards(self, players, mode='hide'):
        label_card_1 = self.findChild(QLabel, f"label_p{players[0]}c{1}", options=Qt.FindChildrenRecursively)
        label_card_2 = self.findChild(QLabel, f"label_p{players[0]}c{2}", options=Qt.FindChildrenRecursively)
        avatar = self.findChild(QLabel, f"pl_{players[0]}_avatar")
        visibility = True if mode == 'show' else False
        label_card_1.setVisible(visibility)
        label_card_2.setVisible(visibility)
        avatar.setVisible(not visibility)

    def close_request_thread(self):
        try:
            self.request_thread.quit()
            self.request_thread.disconnect()
        except Exception as e:
            pass

    def start_time_loop(self):
        """
        calls: get /json/table/:id
        :return:
        """
        self.s_15_timer = QTimer()
        self.s_15_timer.timeout.connect(self.update_time)
        self.curr_time = 0
        self.timer_pause = False
        self.prepare_update()
        self.s_15_timer.start(1000)

    def update_time(self):
        """
        gets called after each 1 second
        :return:
        """
        if not self.timer_pause:
            self.curr_time += 1
            if self.curr_time == TABLE_REFRESH_TIME:
                self.curr_time = 0
                self.prepare_update()
                self.update()

    def update_players(self, players):
        def player_details():
            if player.get('name'):
                label_name = self.findChild(QLabel, f"label_pl_{position}_name", options=Qt.FindChildrenRecursively)
                label_name.setText(str(player['name']))
            if 'stack' in player:
                label_stack = self.findChild(QLabel, f"label_pl_{position}_btc", options=Qt.FindChildrenRecursively)
                label_stack.setText(f"{player['stack']}{self.currency_unit}")

        def player_cards():
            if player.get('card1') and player.get("card2"):
                # [!] card 1
                self.update_player_cards([position], mode='show')
                label_card_1 = self.findChild(QLabel, f"label_p{position}c{1}", options=Qt.FindChildrenRecursively)
                card_1_name = player['card1']
                if card_1_name and card_1_name in CARDS:
                    label_card_1.setPixmap(CARDS[card_1_name])
                else:  # if some invalid card name is received then card image is hidden
                    label_card_1.setVisible(False)

                # [!] card 2
                label_card_2 = self.findChild(QLabel, f"label_p{position}c{2}", options=Qt.FindChildrenRecursively)
                card_2_name = player['card2']
                if card_2_name and card_2_name in CARDS:
                    label_card_2.setPixmap(CARDS[card_2_name])
                else:  # if some invalid card name is received then card image is hidden
                    label_card_2.setVisible(False)
            else:
                self.update_player_cards([position], mode='hide')

        def players_turn():
            progress_bar = self.findChild(QProgressBar, f"progressBar_pl_{position}", options=Qt.FindChildrenRecursively)
            progress_bar: QProgressBar
            if player.get('timeleft'):
                self.update_progressbar([position], mode='show')  # show progress bar + clock icon
                progress_bar.setMaximum(PROGRESS_BAR_MAX)  # since using time left parameter, so setting it to calculate in percentage
                if player.get("timeleft") and str(player.get("timeleft")).isdigit():
                    value = int(int(player['timeleft']) / 100 * PROGRESS_BAR_MAX)
                    try:
                        if self.m_2_countdown.isActive() and self.curr_progress_bar != progress_bar:
                            self.m_2_countdown.stop()
                            self.m_2_countdown.disconnect()
                            self.curr_progress_bar = progress_bar
                            self.progress_bar_timer(progress_bar)
                            self.progress_curr_time = value
                        else:
                            self.m_2_countdown.stop()
                            self.m_2_countdown.timeout.disconnect()
                            self.progress_bar_timer(progress_bar)  # after stop activation
                            self.curr_progress_bar = progress_bar
                            self.progress_curr_time = value
                    except AttributeError:
                        self.progress_bar_timer(progress_bar)  # first activation
                        self.progress_curr_time = value
            else:
                progress_bar.setVisible(False)
                self.update_progressbar([position], 'hide')

        def player_is_dealer():
            label_dealer = self.findChild(QLabel, f"label_pl_{position}_dealer", options=Qt.FindChildrenRecursively)
            if player.get('button'):
                # [!] need to display or hide the "Dealer" sign
                if player.get('button') is True:
                    label_dealer.setVisible(True)
                else:
                    label_dealer.setVisible(False)
            else:
                label_dealer.setVisible(False)

        def players_bet():
            label_bet = self.findChild(QLabel, f"label_pl_{position}_bet")
            label_bet_amt = self.findChild(QLabel, f"label_pl_{position}_bet_amt")

            if player.get('bet') and str(player.get('bet')).isdigit():  # shows bet amt when bet is not null and
                # don't show if bet isn't greater than 0, and if it's an integer
                label_bet.setVisible(True)
                label_bet_amt.setVisible(True)
                label_bet_amt.setText(str(player.get('bet')))
            else:
                label_bet.setVisible(False)
                label_bet_amt.setVisible(False)

        for player_index in range(1, 7):
            if str(player_index) in players:
                player = players[str(player_index)]
            else:
                self.update_player_view([player_index])
                continue
            player: Dict
            position = player['position']
            self.hide_show(show=True, pos=int(position))  # displays the frame and the players attributes

            # player view initializations
            player_details()
            player_is_dealer()
            players_bet()
            player_cards()
            players_turn()

    def update_action_buttons(self, table_data: Dict):
        try:
            self.ui.pushButton_fold.setVisible(True)  # display fold button
            mybet = int(table_data['mybet'])
            max_bet = int(table_data['maxbet'])
            mystack = int(table_data['mystack'])
            bb = int(self.bb)  # table.bb from /json/tables
            if mybet >= max_bet:
                self.ui.pushButton_call.setVisible(True)
                self.ui.pushButton_call.setText("CHECK")
            if mybet < max_bet:
                self.ui.pushButton_call.setVisible(True)
                self.ui.pushButton_call.setText("CALL")
            if mystack >= (max_bet - mybet + bb):  # display raise button with slider and input number
                self.ui.horizontalSlider_amt.setVisible(True)  # show slider
                self.ui.spinBox.setVisible(True)  # show input number
                self.ui.pushButton_raise.setVisible(True)  # show raise button

                # set minimum
                if (2 * max_bet) > bb:
                    self.ui.spinBox.setMinimum(2 * max_bet)

                    self.ui.horizontalSlider_amt.setMinimum(2 * max_bet)
                else:
                    self.ui.spinBox.setMinimum(bb)
                    self.ui.horizontalSlider_amt.setMinimum(bb)
                # set maximum
                self.ui.spinBox.setMaximum(mystack + mybet)
                self.ui.horizontalSlider_amt.setMaximum(mystack + mybet)
                self.ui.spinBox.setValue(self.ui.spinBox.minimum())

            if not self.sound_is_muted and MULTIMEDIA_PACKAGE:
                beep_sound()  # play the beep sound
        except Exception as e:
            show_message(ERROR_POPUP_TITLE, ERROR_MSG, 'error')

    def change_input_amt(self, value):
        """
        called when value in input amt box is changed
        """
        self.last_input_amt = value

    def update_board(self, table_data: Dict):
        if 'board' in table_data:
            # [!] data:{board:[...]} --> Table top 5 cards list
            # [!] Show/hide 5 card images
            board = table_data['board']
            self.ui.frame_table_top.setVisible(
                True)  # this will display 5 card images with result and pot label, unavailable data will
            # set corresponding label to hide (For example: if there's no result, label_result will be hidden)
            for card_index, card in enumerate(board):
                label = self.findChild(QLabel, f"label_c{card_index + 1}", options=Qt.FindChildrenRecursively)
                if card and card in CARDS:
                    label.setVisible(True)
                    label.setPixmap(CARDS[card])  # CARDS[card] returns QPixmap object, loaded at the start from Image files
                else:
                    label.setVisible(False)
        else:
            self.ui.frame_table_top.setVisible(False)

        if table_data.get('result') and table_data.get('result'):
            # [!] shows the result
            self.ui.label_result.setVisible(True)
            result = str(table_data.get('result'))
            self.ui.label_result.setText(result)
        else:
            self.ui.label_result.setVisible(False)

        if 'pot' in table_data and str(table_data.get('pot')).isdigit():
            self.ui.label_pot.setVisible(True)
            self.ui.label_pot.setText(f"{table_data['pot']}{self.currency_unit}")
        else:
            self.ui.label_pot.setVisible(False)

    def update_messages(self, res: Dict):
        chat_widget.delete_message(self, clear_all=True)
        messages = res.get("messages")
        if len(messages) > 5:
            chat_widget.delete_message(self, clear_all=True)
            del messages[0]
        for message in messages:
            name = message['name']
            content = message['message']
            timer = message['timer']
            if timer and str(timer).isdigit():
                chat_widget.add_message(self, name, timer, content)

    def user_retry(self, call_name):
        response = show_error_message()

        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(1500, loop.quit)  # wait 1.5 seconds before making the next requests
        loop.exec_()

        if call_name != 'update_table':
            self.close_request_thread()

        if call_name == 'update_table':
            self.close_table_thread()
            if response:
                self.prepare_update()
            else:
                self.timer_pause = False
        elif call_name == 'message' and response:
            self.prepare_message_send()
        elif call_name == 'quit_table' and response:
            self.prepare_quit_table()
        elif call_name == 'call' and response:
            self.prepare_call_action()
        elif call_name == 'check' and response:
            self.prepare_check_action()
        elif call_name == 'fold' and response:
            self.prepare_fold_action()
        elif call_name == 'raise' and response:
            self.prepare_raise_action()

    def prepare_update(self):
        if not self.spectator:
            self.ui.statusbar.showMessage("Joining table...", 20 * 60 * 1000)

        self.timer_pause = True  # set timer pause, so that countdown pauses during table update
        params = tuple(['GET /json/table/{table_id}', None, {'table_id': self.table_id}])
        if not hasattr(self, 'table_thread'):
            self.table_thread = QtCore.QThread()
            self.thread_pool.append(self.table_thread)
        self.request_ = RequestThread.RequestThread(params, self.api)
        self.request_.moveToThread(self.table_thread)
        self.request_.resp.connect(self.update_table)
        self.request_.error_signal.connect(partial(self.user_retry, 'update_table'))
        self.request_.complete.connect(self.close_table_thread)
        self.table_thread.started.connect(self.request_.run)
        self.table_thread.start()
        show_request_status(self)

    def close_table_thread(self):
        try:
            self.table_thread.quit()
            self.table_thread.disconnect()
        except Exception as e:
            pass

    def update_table(self, res_list: list):  # updates table view and messages
        """
        This function will basically refresh the table and update the message box
        :return:
        """
        self.ui.statusbar.clearMessage()
        self.timer_pause = False
        res = res_list[0]
        if res is not None and 'error' not in res and type(res) == dict:
            if 'data' in res:
                res: Dict
                table_data = res['data']
                self.update_board(table_data)

                if table_data.get('players') and table_data.get('players') != 'null':
                    players = table_data.get('players')
                    players: Dict[Dict]
                    self.update_players(players)

                if table_data.get('myturn') and 'mybet' in table_data and 'maxbet' in table_data and 'mystack' in table_data:
                    self.ui.statusbar.clearMessage()  # clear "joining table..." status when mystack > 0
                    self.update_action_buttons(table_data)
                else:
                    if not self.spectator:
                        self.ui.statusbar.showMessage("Joining table...", 20 * 60 * 1000)
                        self.spectator = False
                    if table_data.get('mystack') is not None:
                        self.spectator = True
                        self.ui.statusbar.clearMessage()

                    self.ui.pushButton_call.setVisible(False)  # hide call button
                    self.ui.horizontalSlider_amt.setVisible(False)  # hide slider
                    self.ui.spinBox.setVisible(False)  # hide input number
                    self.ui.pushButton_raise.setVisible(False)  # hide raise button
                    self.ui.pushButton_fold.setVisible(False)  # hide fold button
            if res.get('messages'):
                self.update_messages(res)

    def prepare_call_action(self):
        self.request_ = RequestThread.RequestThread(
            params=('POST /json/table/{table_id}/call', None, {'table_id': self.table_id}), api_obj=self.api)
        self.request_.resp.connect(self.do_call_action)
        self.request_.error_signal.connect(partial(self.user_retry, 'call'))
        self.request_.complete.connect(self.close_request_thread)

        self.request_.moveToThread(self.request_thread)
        self.request_thread.started.connect(self.request_.run)
        self.request_thread.start()
        show_request_status(self)

    def do_call_action(self, res_list: list):
        self.ui.statusbar.clearMessage()
        res = res_list[0]
        if (res and "error" in res) or (res is None):
            show_message(ERROR_POPUP_TITLE, ERROR_MSG, 'error')
        elif res and res.get('table'):
            self.prepare_update()
            return 0

    def prepare_check_action(self):
        self.request_ = RequestThread.RequestThread(
            params=('POST /json/table/{table_id}/check', None, {'table_id': self.table_id}), api_obj=self.api)
        self.request_.resp.connect(self.do_check_action)
        self.request_.error_signal.connect(partial(self.user_retry, 'check'))
        self.request_.complete.connect(self.close_request_thread)

        self.request_.moveToThread(self.request_thread)
        self.request_thread.started.connect(self.request_.run)
        self.request_thread.start()
        show_request_status(self)

    def do_check_action(self, res_list: list):
        self.ui.statusbar.clearMessage()
        res = res_list[0]
        if res is None or 'error' in res:
            show_message(ERROR_POPUP_TITLE, ERROR_MSG, 'error')
        elif res and res.get('table'):
            self.prepare_update()
            return 0

    def prepare_fold_action(self):
        self.request_ = RequestThread.RequestThread(
            ('POST /json/table/{table_id}/fold', None, {'table_id': self.table_id}), api_obj=self.api)

        self.request_.resp.connect(self.do_fold_action)
        self.request_.error_signal.connect(partial(self.user_retry, 'fold'))
        self.request_.complete.connect(self.close_request_thread)
        self.request_.moveToThread(self.request_thread)

        self.request_thread.started.connect(self.request_.run)
        self.request_thread.start()
        show_request_status(self)

    def do_fold_action(self, res_list: list):
        self.ui.statusbar.clearMessage()
        res = res_list[0]
        if res and res.get('table'):  # res['table'] will be table_id here
            self.prepare_update()
            return 0
        elif res is None:
            show_message(ERROR_POPUP_TITLE, ERROR_MSG, 'error')

    def prepare_raise_action(self):
        amt_raise = self.ui.horizontalSlider_amt.value()
        body_bytes = f"amount={amt_raise}".encode('iso-8859-1')
        self.request_ = RequestThread.RequestThread(
            ('POST /json/table/{table_id}/raise', body_bytes, {'table_id': self.table_id}), api_obj=self.api)
        self.request_.resp.connect(self.do_raise_action)
        self.request_.error_signal.connect(partial(self.user_retry, 'raise'))
        self.request_.complete.connect(self.close_request_thread)

        self.request_.moveToThread(self.request_thread)
        self.request_thread.started.connect(self.request_.run)
        self.request_thread.start()
        show_request_status(self)

    def do_raise_action(self, res_list: list):
        self.ui.statusbar.clearMessage()
        res = res_list[0]
        if res and res.get('table'):
            self.prepare_update()
            return 0
        else:
            show_message(ERROR_POPUP_TITLE, ERROR_MSG, 'error')

    def CRF(self, request):
        """
        Handles the CALL, RAISE AND FOLD button action
        :param request: alias for button action performed
        :return:
        """
        self.hide_action_buttons()  # hide all action button, if any one is pressed
        if request == 'call' and self.ui.pushButton_call.text().lower() == 'check':
            request = 'check'
        if request == 'call':
            self.prepare_call_action()
        elif request == 'check':
            self.prepare_check_action()
        elif request == 'fold':
            self.prepare_fold_action()
        elif request == 'raise':
            self.prepare_raise_action()

    def prepare_message_send(self):
        content = self.ui.lineEdit_chat.text()
        if content and content.replace(' ', ''):
            content = content.strip()
            if len(content) < 50:  # length of each message is less than 50 (49 chars)
                # post message content
                body_bytes = f"message={content}".encode('iso-8859-1')
                if not hasattr(self, 'message_thread'):
                    self.message_thread = QtCore.QThread()
                    self.thread_pool.append(self.message_thread)
                self.request_ = RequestThread.RequestThread(
                    ('POST /json/table/{table_id}/message', body_bytes, {'table_id': self.table_id}),
                    self.api)

                self.request_.resp.connect(self.send_message)
                self.request_.error_signal.connect(partial(self.user_retry, 'message'))
                self.request_.complete.connect(self.close_message_thread)

                self.request_.moveToThread(self.message_thread)
                self.message_thread.started.connect(self.request_.run)
                self.message_thread.start()
                show_request_status(self)

                self.ui.lineEdit_chat.clear()  # clear line after message send request posted

    def send_message(self, res_list):
        self.ui.statusbar.clearMessage()
        res = res_list[0]
        if res is None:
            show_message(ERROR_POPUP_TITLE, ERROR_MSG, 'error')
        elif res is not None and 'table' in res:
            pass
        else:
            show_message(ERROR_POPUP_TITLE, ERROR_MSG, 'error')
        self.prepare_update()  # update table after sending message
        self.update()

    def close_message_thread(self):
        try:
            self.message_thread.quit()
            self.message_thread.disconnect()
        except Exception as e:
            pass

    def close_all_threads(self):
        for thread in self.thread_pool:
            try:
                thread.quit()
                thread.disconnect()
            except Exception as e:
                pass

    def close_timers(self):
        try:
            self.s_15_timer.stop()
            if hasattr(self, 'm_2_countdown'):
                self.m_2_countdown.stop()
        except Exception as e:
            pass


    def closeEvent(self, event: 'QtCore.QEvent') -> None:
        if event.spontaneous():
            message = QMessageBox(QMessageBox.Question, "Close Confirmation - Torpoker",
                                  "Are you sure you want to close this window?",
                                  QMessageBox.Yes | QMessageBox.Cancel)
            res = message.exec_()
            if res == QMessageBox.Yes:
                self.s_15_timer.stop()
                self.close_timers()
                self.close_all_threads()
                self.exit_table.emit()  # emit signal to go back to the tables list window
                self.close()
            else:
                event.ignore()
        else:
            self.close_timers()
            self.close_all_threads()
            self.s_15_timer.stop()
            self.close()
