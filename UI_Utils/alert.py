from PyQt5.QtWidgets import QMessageBox

ERROR_CONNECTION_MESSAGE = "Network Error"
ERROR_POPUP_TITLE = "ERROR"


def show_message(title, text, message_type):
    if message_type == 'info':
        message = QMessageBox(QMessageBox.Information, title, text, QMessageBox.Ok)
        message.exec_()
    elif message_type == 'warning':
        message = QMessageBox(QMessageBox.Warning, title, text, QMessageBox.Retry | QMessageBox.Cancel)
        message.setDefaultButton(QMessageBox.Cancel)
        res = message.exec_()
        if res == QMessageBox.Retry:
            return 1
        else:
            message.close()
            return None
    elif message_type == 'error':
        message = QMessageBox(QMessageBox.Critical, title, text, QMessageBox.Close)
        message.exec_()
    elif message_type == 'close_confirm':
        message = QMessageBox(QMessageBox.Question, title, text, QMessageBox.Yes | QMessageBox.No)
        message.setDefaultButton(QMessageBox.No)
        res = message.exec_()
        if res == QMessageBox.Yes:
            return True
        else:
            return False


def show_error_message():
    user_response = show_message(ERROR_POPUP_TITLE, ERROR_CONNECTION_MESSAGE, 'warning')
    return user_response


def show_request_status(parent):
    parent.ui.statusbar.showMessage("requesting...", 10 * 60 * 1000)
