from typing import Dict
from PyQt5 import QtCore
from connection import api
#New Imports
from test_files.logging_handler import log_api


class RequestThread(QtCore.QObject):
    """
    handles major API calls inside a thread and accept user response (retry/cancel) in case of a ConnectionError
    and perform accordingly
    """
    resp = QtCore.pyqtSignal(list)
    complete = QtCore.pyqtSignal()
    error_signal = QtCore.pyqtSignal()

    def __init__(self, params: tuple, api_obj: api.API = None, call_dict: Dict = None):
        super(RequestThread, self).__init__()
        self.call_dict = call_dict
        self.api_obj = api_obj
        self.api_params = params

    def run(self):
        self.fetch_response()

    def fetch_response(self):

        try:
            # Log the request
            log_api(f'Sending request with params: {self.api_params}')

            resp = self.api_obj.api_call(*self.api_params)

            # Log the response
            log_api(f'Received response: {resp}')


            # Emit the response
            self.resp.emit([resp])
            self.complete.emit()
        except Exception as e:
            # Log any exceptions
            log_api(f'Error in fetch_response: {e}')
            self.error_signal.emit()
