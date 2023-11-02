from datetime import datetime

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QGridLayout, QWidget, QSizePolicy, QSpacerItem)


def add_message(parent, name=None, time_stamp=None, text=None):
    message_widget = QWidget(parent.ui.chat_scroll_area)
    message_widget.setMinimumHeight(85)
    message_widget.setMaximumSize(16777215, 90)
    grid_layout = QGridLayout(message_widget)
    grid_layout.setContentsMargins(-1, 0, -1, 0)
    grid_layout.setHorizontalSpacing(4)
    grid_layout.setVerticalSpacing(0)

    label_msg_details = QLabel(message_widget)
    label_msg_details.setMaximumSize(QtCore.QSize(16777215, 30))
    label_msg_details.setStyleSheet("color: white;\n"
                                    "background-color: grey;\n"
                                    "padding-left: 5px;\n"
                                    "border: 1px solid black;\n"
                                    "border-radius: 5px;")
    grid_layout.addWidget(label_msg_details, 0, 0, 1, 1)
    spacerItem5 = QSpacerItem(40, 10, QSizePolicy.Preferred, QSizePolicy.Preferred)
    grid_layout.addItem(spacerItem5, 0, 1, 1, 1)
    label_text_message = QLabel(message_widget)
    label_text_message.setMaximumSize(QtCore.QSize(175, 50))
    label_text_message.setStyleSheet("background-color: black;\n"
                                     "color: white;\n"
                                     "border-radius: 7px;\n"
                                     "padding: 5px;")
    label_text_message.setWordWrap(True)
    grid_layout.addWidget(label_text_message, 1, 0, 1, 2)
    parent.ui.verticalLayout_7.addWidget(message_widget)
    parent.ui.chat_area.setWidget(parent.ui.chat_scroll_area)

    if None not in [name, time_stamp, text]:
        date_string = datetime.fromtimestamp(int(time_stamp)).strftime("%d-%b-%Y, %H:%M")
        details_string = f"{name}\n{date_string}"
        label_msg_details.setTextFormat(QtCore.Qt.PlainText)
        label_msg_details.setText(details_string)
        label_text_message.setTextFormat(QtCore.Qt.PlainText)
        label_text_message.setText(text)
    delete_message(parent)
    parent.update()


def delete_message(parent, clear_all=False):
    """
    if clear_all = True, all messages in the widget will be cleared before adding the new ones to avoid repetition
    """
    v_box_7 = parent.ui.verticalLayout_7
    v_box_7: QVBoxLayout
    if v_box_7.count() > 5 or clear_all:
        for item in range(v_box_7.count()-1, -1, -1):
            try:
                parent.ui.verticalLayout_7.itemAt(item).widget().setParent(None)
                if not clear_all:
                    break
            except Exception as e:
                print(v_box_7.count())
                print("Exception deleting widget:",e.__str__(), f"({item})")
