from typing import Dict
from PyQt5 import QtCore
from ..connection import api



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
            resp = self.api_obj.api_call(*self.api_params)
            self.resp.emit([resp])
            self.complete.emit()
        except Exception as e:
            self.error_signal.emit()