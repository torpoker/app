import os
import json

from PyQt5.QtWidgets import QPushButton, QApplication

from src.UI_Utils.JoinList import IPPop


def find_button_with_object_name(object_name):
    for widget in QApplication.allWidgets():
        if isinstance(widget, QPushButton) and widget.objectName() == object_name:
            return widget
    return None



def find_button_with_text(text):
    for widget in QApplication.allWidgets():
        if isinstance(widget, QPushButton) and widget.text() == text:
            return widget
    return None


def find_IPPop_dialog():
    for widget in QApplication.topLevelWidgets():
        if isinstance(widget, IPPop):
            return widget
    return None



folder_path = 'test_files/apiV1/'
#function to load the mocks
def load_mock_data(filename):
    with open(os.path.join(folder_path, filename), 'r') as file:
        return json.loads(file.read())






