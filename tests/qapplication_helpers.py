import json
import os
from PyQt5.QtWidgets import QPushButton, QApplication
from src.UI_Utils.JoinList import IPPop

class QApplicationHelper:
    @staticmethod
    def find_button_with_object_name(object_name):
        for widget in QApplication.allWidgets():
            if isinstance(widget, QPushButton) and widget.objectName() == object_name:
                return widget
        return None

    @staticmethod
    def find_button_with_text(text):
        for widget in QApplication.allWidgets():
            if isinstance(widget, QPushButton) and widget.text() == text:
                return widget
        return None

    @staticmethod
    def find_IPPop_dialog():
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, IPPop):
                return widget
        return None





