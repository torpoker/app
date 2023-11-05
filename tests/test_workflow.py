import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QCoreApplication

from src.run_torpoker import AppHome
from PyQt5 import QtCore
from unittest.mock import patch
from qapplication_helpers import QApplicationHelper
from json_helpers import parse_json_file








@pytest.fixture(scope="session", autouse=True)
def app():
    return QApplication([])

def test_click_logging(qtbot, app):
    folder_path = 'tests/apiV1/'
    # Create an instance of your application window
    window = AppHome()
    window.show()

    # Create a QTimer to regularly call QCoreApplication.processEvents
    timer = QTimer()
    timer.timeout.connect(QCoreApplication.processEvents)
    timer.start(100)  # Update every 100 milliseconds

    # Set the text in the input fields
    qtbot.wait(1500)
    window.ui.lineEdit_address.setText("xmr.poker")
    qtbot.wait(1500)
    window.ui.lineEdit_address_port.setText("443")

    MOCKED_CONFIRM_RESPONSE = parse_json_file(folder_path,'mocked_confirm_response.json')
    MOCKED_TABLE_STATE_RESPONSE = parse_json_file(folder_path,'mocked_table_state_response.json')
    MOCKED_CALL_RESPONSE = parse_json_file(folder_path,'mocked_call_response.json')
    MOCKED_TABLE_STATE_AFTER_CALL_RESPONSE = parse_json_file(folder_path,'mocked_table_state_after_call_response.json')
    MOCKED_CHECK_RESPONSE = parse_json_file(folder_path,'mocked_check_response.json')
    MOCKED_TABLE_STATE_AFTER_TURN_RESPONSE = parse_json_file(folder_path,'mocked_table_state_after_turn_response.json')
    MOCKED_TABLE_STATE_AFTER_RAISE = parse_json_file(folder_path,'mocked_table_state_after_raise.json')
    MOCKED_TABLE_STATE_NEW_ROUND = parse_json_file(folder_path,'mocked_table_state_new_round.json')
    MOCKED_CASHOUT_RESPONSE = parse_json_file(folder_path,'mocked_cashout_response.json')
    MOCKED_TABLE_STATUS_AFTER_MESSAGE = parse_json_file(folder_path,'mocked_table_status_after_message_response.json')


    MOCKED_ACCOUNT_RESPONSE = parse_json_file(folder_path,'mocked_account_response.json')
    MOCKED_TABLES_RESPONSE = parse_json_file(folder_path,'mocked_tables_response.json')



    # Start the mocking for API calls
    with patch('src.connection.api.API.api_call', side_effect=[MOCKED_ACCOUNT_RESPONSE, MOCKED_TABLES_RESPONSE]):
        # Click on the connect button
        qtbot.mouseClick(window.ui.pushButton_connect, QtCore.Qt.LeftButton)  # Click on the button
        qtbot.wait(1500)  # Wait a moment for the Captcha dialog to load

    play_now_button = window.table_list.ui.pushButton_playnow
    qtbot.mouseClick(play_now_button, QtCore.Qt.LeftButton)
    qtbot.wait(1500)  # Wait a moment for the Captcha dialog to load


    # Access the Captcha dialog
    captcha_dialog = window.table_list.captcha_dialog  # Assuming that table_list holds a reference to the Captcha dialog

    # Set the text in the input fields of the Captcha dialog
    qtbot.wait(1500)
    captcha_dialog.ui.lineEdit_btc_address.setText("ADRESS")
    qtbot.wait(1500)
    captcha_dialog.ui.lineEdit_captcha.setText("CAPTCHA_Text")

    MOCKED_SEND_POST_RESPONSE = parse_json_file(folder_path,'mocked_send_post_response.json')
    MOCKED_SEND_COMPLETED_RESPONSE = parse_json_file(folder_path,'mocked_send_completed_response.json')
    MOCKED_ACCOUNT_INFO_RESPONSE = parse_json_file(folder_path,'mocked_account_info_response.json')

    with patch('src.connection.api.API.api_call') as mocked_api_call:
        # Mock responses for the POST request and subsequent GET requests
        mocked_api_call.side_effect = [
            MOCKED_SEND_POST_RESPONSE,
            MOCKED_SEND_COMPLETED_RESPONSE,
            MOCKED_ACCOUNT_INFO_RESPONSE
        ]

        # click the "Submit"-Button in the Captcha-Dialog
        qtbot.wait(1500)
        qtbot.mouseClick(captcha_dialog.ui.pushButton_submit, QtCore.Qt.LeftButton)


        qtbot.wait(16500)

    MOCKED_JOIN_TABLE_RESPONSE = parse_json_file(folder_path,'mocked_join_table_response.json')

    with patch('src.connection.api.API.api_call') as mocked_api_call:
        mocked_api_call.side_effect = [
            MOCKED_JOIN_TABLE_RESPONSE
        ]

        # access the QTableWidget-Object
        table_widget = window.table_list.ui.tableWidget_game_tables

        # Selection of a specific table (e.g. the first table)
        first_table_row = 0
        join_button_column = 3  # Since the join button is added in the 4th column (index 3).

        # Access the "Join" button of the selected table and click on it
        join_button = table_widget.cellWidget(first_table_row, join_button_column)
        qtbot.mouseClick(join_button, QtCore.Qt.LeftButton)

        qtbot.wait(1500)

    # This function searches for the opened dialog of type IPPop
    input_popup = QApplicationHelper.find_IPPop_dialog()

    # Set the value in the input widget
    input_value_widget = input_popup.ui.lineEdit_btc_amt
    qtbot.keyClicks(input_value_widget, "30")

    qtbot.wait(1500)


    input_submit_button = input_popup.ui.pushButton_submit
    qtbot.mouseClick(input_submit_button, QtCore.Qt.LeftButton)



    # After clicking the "Join" button, we simulate the joining process
    with patch('src.connection.api.API.api_call') as mocked_api_call:
        mocked_api_call.side_effect = [
            MOCKED_CONFIRM_RESPONSE,
            MOCKED_TABLE_STATE_RESPONSE
        ]


        qtbot.wait(5000)

    # -------------------------Table--------------------------------

    # find the callbutton and click
    call_button = QApplicationHelper.find_button_with_object_name("pushButton_call")
    qtbot.mouseClick(call_button, QtCore.Qt.LeftButton)




    with patch('src.connection.api.API.api_call') as mocked_api_call:
        mocked_api_call.side_effect = [
            MOCKED_CALL_RESPONSE,
            MOCKED_TABLE_STATE_AFTER_CALL_RESPONSE

        ]

        qtbot.wait(5000)

    MOCKED_TABLE_STATE_AFTER_ENEMY_CHECK_RESPONSE = parse_json_file(folder_path,'mocked_table_state_after_enemy_check_response.json')

    # after opponent check
    with patch('src.connection.api.API.api_call') as mocked_api_call:
        mocked_api_call.side_effect = [
            MOCKED_TABLE_STATE_AFTER_ENEMY_CHECK_RESPONSE
        ]

        qtbot.wait(5000)

#----------------------------------Flop----------------------------------

    MOCKED_TABLE_STATE_AFTER_FLOP_RESPONSE = parse_json_file(folder_path,'mocked_table_state_after_flop_response.json')
    # Opponent check
    with patch('src.connection.api.API.api_call') as mocked_api_call:
        mocked_api_call.side_effect = [
            MOCKED_TABLE_STATE_AFTER_FLOP_RESPONSE
        ]

        qtbot.wait(5000)

    # find the callbutton and click
    check_button = QApplicationHelper.find_button_with_text("CHECK")
    qtbot.mouseClick(check_button, QtCore.Qt.LeftButton)



    with patch('src.connection.api.API.api_call') as mocked_api_call:
        mocked_api_call.side_effect = [
            MOCKED_CHECK_RESPONSE,
            MOCKED_TABLE_STATE_AFTER_TURN_RESPONSE
        ]

        qtbot.wait(1500)

    # ----------------------------------Turn----------------------------------
    MOCKED_TABLE_STATE_AFTER_OPPONENT_CHECK_TURN = parse_json_file(folder_path,'mocked_table_state_after_opponent_check_turn_response.json')

    with patch('src.connection.api.API.api_call') as mocked_api_call:
        mocked_api_call.return_value = MOCKED_TABLE_STATE_AFTER_OPPONENT_CHECK_TURN

    qtbot.wait(5000)

    # find the raise button and click it
    raise_button = QApplicationHelper.find_button_with_text("RAISE")
    qtbot.mouseClick(raise_button, QtCore.Qt.LeftButton)



    with patch('src.connection.api.API.api_call') as mocked_api_call:
        mocked_api_call.side_effect = [MOCKED_CONFIRM_RESPONSE, MOCKED_TABLE_STATE_AFTER_RAISE]
        qtbot.wait(1500)

    MOCKED_TABLE_STATE_AFTER_OPPONENT_CALL = parse_json_file(folder_path,'mocked_table_state_after_opponent_call.json')

    #Opponent calls the Raise
    with patch('src.connection.api.API.api_call') as mocked_api_call:
        mocked_api_call.return_value = MOCKED_TABLE_STATE_AFTER_OPPONENT_CALL

        qtbot.wait(5000)


    # find the fold button and click
    fold_button = QApplicationHelper.find_button_with_text("FOLD")
    qtbot.mouseClick(fold_button, QtCore.Qt.LeftButton)




    with patch('src.connection.api.API.api_call') as mocked_api_call:
        mocked_api_call.side_effect = [MOCKED_CONFIRM_RESPONSE,  MOCKED_TABLE_STATE_NEW_ROUND]
        qtbot.wait(1500)



    # Find the "lineEdit_chat" widget and enter the message "in out".
    chat_input = QApplicationHelper.find_button_with_object_name("lineEdit_chat")
    qtbot.keyClicks(chat_input, "im out")

    qtbot.wait(1500)

    # Simulate the Enter key to send the message
    qtbot.keyPress(chat_input, QtCore.Qt.Key_Return)



    with patch('src.connection.api.API.api_call') as mocked_api_call:
        mocked_api_call.side_effect = [MOCKED_CONFIRM_RESPONSE, MOCKED_TABLE_STATUS_AFTER_MESSAGE]

        qtbot.wait(1500)

        # -----------------------------------

    # Find and click the “pushButton_quit” button
    quit_button = QApplicationHelper.find_button_with_object_name("pushButton_quit")
    qtbot.mouseClick(quit_button, QtCore.Qt.LeftButton)

    MOCKED_QUIT_TABLE_RESPONSE = parse_json_file(folder_path,'mocked_quit_table_response.json')
    MOCKED_ACCOUNT_RESPONSE_AFTER_LEAVE = parse_json_file(folder_path,'mocked_account_after_leave_response.json')


    with patch('src.connection.api.API.api_call') as mocked_api_call:
        mocked_api_call.side_effect = [MOCKED_QUIT_TABLE_RESPONSE,
                                        MOCKED_ACCOUNT_RESPONSE_AFTER_LEAVE,
                                        MOCKED_TABLES_RESPONSE]
        qtbot.wait(1500)



    # Find and click the “pushButton_cashout” button
    cashout_button = QApplicationHelper.find_button_with_object_name("pushButton_cashout")
    qtbot.mouseClick(cashout_button, QtCore.Qt.LeftButton)

    with patch('src.connection.api.API.api_call') as mocked_api_call:
        mocked_api_call.return_value = MOCKED_CASHOUT_RESPONSE

        qtbot.wait(10000)


    app.exit()




