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

import json

def read_file_as_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:

            content = file.read()
            # Optionally, remove the next line if you do not want to print the content.
            print(content)
            return json.loads(content)  # Converts the JSON formatted string into a Python object.
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"The file {file_path} could not be parsed as JSON.")
    except Exception as e:
        print(f"An error has occurred: {e}")


MOCKED_TABLES_RESPONSE = read_file_as_json('apiV1/mocked_tables_response.txt')

print(MOCKED_TABLES_RESPONSE)  # Zum Debuggen, um den Inhalt zu überprüfen




