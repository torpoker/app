import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QCoreApplication
from src.run_torpoker import AppHome
from PyQt5 import QtCore
from json_helpers import parse_json_file
from tests.qapplication_helpers import QApplicationHelper


@pytest.fixture(scope="session", autouse=True)
def app():
    # Initialize and return a QApplication instance for session-wide use
    application = QApplication([])
    yield application
    # Perform cleanup here if necessary
    application.quit()

@pytest.fixture(autouse=True)
def mock_api_calls(mocker):
    folder_path = 'tests/apiV1/'

    mocked_tables_response = parse_json_file(folder_path, 'mocked_tables_response.json')
    mocked_account_response = parse_json_file(folder_path, 'mocked_account_response.json')
    mocked_account_info_response = parse_json_file(folder_path, 'mocked_account_info_response.json')
    mocked_send_post_response = parse_json_file(folder_path, 'mocked_send_post_response.json')
    mocked_send_completed_response = parse_json_file(folder_path, 'mocked_send_completed_response.json')
    mocked_join_table_response = parse_json_file(folder_path, 'mocked_join_table_response.json')
    mocked_confirm_response = parse_json_file(folder_path, 'mocked_confirm_response.json')
    mocked_table_state_response = parse_json_file(folder_path, 'mocked_table_state_response.json')
    mocked_call_response = parse_json_file(folder_path, 'mocked_call_response.json')
    mocked_check_response = parse_json_file(folder_path, 'mocked_check_response.json')
    mocked_raise_response = parse_json_file(folder_path, 'mocked_check_response.json')

    mocked_quit_table = parse_json_file(folder_path, 'mocked_quit_table_response.json')
    mocked_after_leave = parse_json_file(folder_path, 'mocked_account_after_leave_response.json')

    mocked_table_state_after_call_response = parse_json_file(folder_path, 'mocked_table_state_after_flop_response.json')
    mocked_table_state_after_turn_response = parse_json_file(folder_path,'mocked_table_state_after_opponent_check_turn_response.json')
    mocked_table_state_after_call = parse_json_file(folder_path,'mocked_table_state_after_opponent_call.json')
    mocked_table_state_after_fold = parse_json_file(folder_path,'mocked_table_state_new_round.json')
    mocked_table_state_after_message = parse_json_file(folder_path, 'mocked_table_status_after_message_response.json')

    mocked_cashout_response = parse_json_file(folder_path, 'mocked_cashout_response.json')


    get_json_account_mock = mocker.patch(
        'src.connection.api.API.get_json_account',
        side_effect=[mocked_account_response, mocked_account_info_response, mocked_after_leave]
    )
    get_json_tables_mock = mocker.patch(
        'src.connection.api.API.get_json_tables',
        return_value=mocked_tables_response
    )

    post_json_send_mock = mocker.patch(
        'src.connection.api.API.post_json_send',
        return_value=mocked_send_post_response
    )

    get_json_send_mock = mocker.patch(
        'src.connection.api.API.get_json_send',
        return_value=mocked_send_completed_response
    )

    post_json_table_join_mock = mocker.patch(
        'src.connection.api.API.post_json_table_join',
        return_value=mocked_join_table_response
    )

    confirm_response_mock = mocker.patch(
        'src.connection.api.API.post_json_table_join_confirm',
        return_value=mocked_confirm_response
    )
    table_state_response_mock = mocker.patch(
        'src.connection.api.API.get_table_by_id',
        side_effect=[mocked_table_state_response, mocked_table_state_after_call_response, mocked_table_state_after_turn_response, mocked_table_state_after_call, mocked_table_state_after_fold, mocked_table_state_after_message]
    )

    post_table_call_mock = mocker.patch(
        'src.connection.api.API.post_table_call',
        return_value=mocked_call_response
    )
    post_table_check_mock = mocker.patch(
        'src.connection.api.API.post_table_check',
        return_value=mocked_check_response
    )

    post_table_raise_mock = mocker.patch(
        'src.connection.api.API.post_table_raise',
        return_value=mocked_raise_response
    )

    post_table_fold_mock = mocker.patch(
        'src.connection.api.API.post_table_fold',
        return_value=mocked_table_state_after_fold
    )

    post_table_message_mock = mocker.patch(
        'src.connection.api.API.post_message_to_table',  # Stelle sicher, dass dies der korrekte Methodenname ist
        return_value=mocked_table_state_after_message
    )

    quit_table_mock = mocker.patch(
        'src.connection.api.API.quit_table',
        return_value=mocked_quit_table
    )

    cashout_mock = mocker.patch(
        'src.connection.api.API.get_json_cashout',  # Ersetze 'cashout' durch den tatsächlichen Methodennamen
        return_value=mocked_cashout_response
    )




    return {
        'get_json_account': get_json_account_mock,
        'get_json_tables': get_json_tables_mock,
        'post_json_send': post_json_send_mock,
        'get_json_send': get_json_send_mock,
        'post_json_table_join': post_json_table_join_mock,
        'post_table_join_confirm': confirm_response_mock,
        'get_table_state': table_state_response_mock,
        'post_table_call': post_table_call_mock,
        'post_table_check': post_table_check_mock,
        'post_table_raise': post_table_raise_mock,
        'post_table_fold': post_table_fold_mock,
        'post_table_message': post_table_message_mock,
        'quit_table': quit_table_mock,
    }

def test_click_logging(qtbot, mock_api_calls):
    """Test the logging functionality triggered by the GUI's connect button."""
    window = AppHome()
    window.show()

    timer = QTimer()
    timer.timeout.connect(QCoreApplication.processEvents)
    timer.start(100)

    qtbot.wait(500)
    window.ui.lineEdit_address.setText("xmr.poker")
    qtbot.wait(500)
    window.ui.lineEdit_address_port.setText("443")

    qtbot.mouseClick(window.ui.pushButton_connect, QtCore.Qt.LeftButton)

    # Ensure there's enough time for the application to process events
    qtbot.wait(2500)

    # Verify that the API call was made once
    assert mock_api_calls['get_json_account'].call_count == 1, "get_json_account should be called once"
    assert mock_api_calls['get_json_tables'].call_count == 1, "get_json_tables should be called once"


    play_now_button = window.table_list.ui.pushButton_playnow
    qtbot.mouseClick(play_now_button, QtCore.Qt.LeftButton)
    qtbot.wait(1500)

    # Access the Captcha dialog
    captcha_dialog = window.table_list.captcha_dialog

    # Set the text in the input fields of the Captcha dialog
    captcha_dialog.ui.lineEdit_btc_address.setText("ADRESS")
    qtbot.wait(1500)
    captcha_dialog.ui.lineEdit_captcha.setText("CAPTCHA_Text")
    qtbot.wait(1500)

    # Get Account/ MOCKED_ACCOUNT_INFO_RESPONSE
    # post_json_send / MOCKED_SEND_POST_RESPONSE
    qtbot.mouseClick(captcha_dialog.ui.pushButton_submit, QtCore.Qt.LeftButton)
    qtbot.wait(1500)
    assert mock_api_calls['post_json_send'].call_count == 1, "post_json_send should be called once"

    qtbot.wait(16500)

    assert mock_api_calls['get_json_send'].call_count == 1, "get_json_send should be called to check send status"
    assert mock_api_calls['get_json_account'].call_count == 2, "get_json_account should be called again after captcha submit"

    # Greife auf das QTableWidget-Objekt zu
    table_widget = window.table_list.ui.tableWidget_game_tables

    # Wähle einen spezifischen Tisch aus (z.B. den ersten Tisch)
    first_table_row = 0
    join_button_column = 3  # Der "Join"-Button befindet sich in der vierten Spalte (Index 3).

    # Greife auf den "Join"-Button des ausgewählten Tisches zu und klicke darauf
    join_button = table_widget.cellWidget(first_table_row, join_button_column)
    qtbot.mouseClick(join_button, QtCore.Qt.LeftButton)
    qtbot.wait(500)


    # Überprüfe, ob der API-Aufruf für das Beitreten zum Tisch gemacht wurde
    assert mock_api_calls['post_json_table_join'].call_count == 1

    # This function searches for the opened dialog of type IPPop
    input_popup = QApplicationHelper.find_IPPop_dialog()

    # Set the value in the input widget
    input_value_widget = input_popup.ui.lineEdit_btc_amt
    qtbot.keyClicks(input_value_widget, "30")
    qtbot.wait(500)
    input_submit_button = input_popup.ui.pushButton_submit


    qtbot.mouseClick(input_submit_button, QtCore.Qt.LeftButton)
    qtbot.wait(500)

    assert mock_api_calls['post_table_join_confirm'].call_count == 1
    assert mock_api_calls['get_table_state'].call_count == 1

    qtbot.wait(5000)

    # Finde den Call-Button und klicke darauf
    call_button = QApplicationHelper.find_button_with_object_name("pushButton_call")
    qtbot.mouseClick(call_button, QtCore.Qt.LeftButton)
    qtbot.wait(5000)


    assert mock_api_calls['post_table_call'].call_count == 1
    assert mock_api_calls['get_table_state'].call_count > 0

    # find the checkbutton and click
    check_button = QApplicationHelper.find_button_with_text("CHECK")
    qtbot.mouseClick(check_button, QtCore.Qt.LeftButton)

    qtbot.wait(5000)
    assert mock_api_calls['post_table_check'].call_count == 1
    assert mock_api_calls['get_table_state'].call_count == 4

    # find the raise button and click it
    raise_button = QApplicationHelper.find_button_with_text("RAISE")
    qtbot.mouseClick(raise_button, QtCore.Qt.LeftButton)
    qtbot.wait(5000)

    assert mock_api_calls['post_table_raise'].call_count == 1
    assert mock_api_calls['get_table_state'].call_count == 5

    qtbot.wait(5500)

    raise_button = QApplicationHelper.find_button_with_text("FOLD")
    qtbot.mouseClick(raise_button, QtCore.Qt.LeftButton)
    qtbot.wait(4500)

    assert mock_api_calls['post_table_fold'].call_count == 1
    assert mock_api_calls['get_table_state'].call_count == 6


    # Find the "lineEdit_chat" widget and enter the message "in out".
    chat_input = QApplicationHelper.find_button_with_object_name("lineEdit_chat")
    qtbot.keyClicks(chat_input, "im out")
    qtbot.wait(1500)

    # Simulate the Enter key to send the message
    qtbot.keyPress(chat_input, QtCore.Qt.Key_Return)

    #assert mock_api_calls['post_table_message'].call_count == 1
    #assert mock_api_calls['get_table_state'].call_count == 7
    qtbot.wait(5000)

    # Finde den Quit-Button und klicke darauf
    quit_button = QApplicationHelper.find_button_with_object_name("pushButton_quit")
    qtbot.mouseClick(quit_button, QtCore.Qt.LeftButton)

    # Warte kurz, um sicherzustellen, dass die Aktion verarbeitet wird
    qtbot.wait(1500)

    # Überprüfe, ob die korrekten API-Aufrufe gemacht wurden
    assert mock_api_calls['quit_table'].call_count == 1
    assert mock_api_calls['get_json_account'].call_count == 3


    # Find and click the “pushButton_cashout” button
    cashout_button = QApplicationHelper.find_button_with_object_name("pushButton_cashout")
    qtbot.mouseClick(cashout_button, QtCore.Qt.LeftButton)
    qtbot.wait(1500)
    assert mock_api_calls['cashout'].call_count == 1


    qtbot.wait(5000)


