from typing import List

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidget, QPushButton, QAbstractItemView

button_stylesheet = """QPushButton{
	background-color: qlineargradient(spread:pad, x1:1, y1:0.914, x2:1, y2:0, stop:0.00497512 rgba(69, 3, 3, 255), stop:0.174129 rgba(152, 0, 0, 255), stop:0.686567 rgba(188, 0, 0, 255));
	color: white;
	border: 1px solid maroon;
	padding: 1px;
	border-radius: 3px;
	font: 75 12pt "Serif";
}
QPushButton::hover{
	padding: 1px;
	border-radius: 3px;
}
QPushButton::pressed{
	padding: 1px;
	border-radius: 3px;
	margin-top: 3px;
	margin-bottom: 3px;
}"""


def add_row_all_table(table_widget):
    """
    Add empty table row
    """
    tot_rows = table_widget.rowCount()
    table_widget.insertRow(tot_rows)

    table_widget: QTableWidget
    table_widget.horizontalHeader().setStretchLastSection(True)
    table_widget.setWordWrap(True)
    table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))


def set_button_style(button: QPushButton):
    button.setIcon(QIcon("src/UI/images/khaw432.png"))
    button.setIconSize(QSize(16, 16))
    return button


def remove_row_all_table(table_widget: QTableWidget):
    """
    Select and Delete rows from table widget
    """
    selected_rows = table_widget.selectionModel().selectedRows()
    if selected_rows:
        row_indices = []
        for row_index in selected_rows:
            row_indices.append(row_index.row())
        row_indices.sort(key=lambda x: -1 * x)
        for row in row_indices:  # sorted in descending order
            table_widget.removeRow(row)


def setSel(selected: List[int], table_widget: QTableWidget):
    """
    Select all rows for the given index range
    """
    table_widget.setSelectionMode(QAbstractItemView.MultiSelection)
    for i in selected:
        table_widget.selectRow(i)


def delete_all_rows(table_widget: QTableWidget):
    """
    Just pass table_widget object, and all rows will be deleted
    """
    row_count = table_widget.rowCount()
    table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
    setSel(list(range(row_count)), table_widget)
    remove_row_all_table(table_widget)
    table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)


def set_cell_widget_all(table_widget: QTableWidget, row, column):
    item = QPushButton(table_widget)
    item.setText("JOIN")
    item.setMaximumSize(83, 35)
    item.setMinimumSize(83, 32)
    item.setStyleSheet(button_stylesheet)
    table_widget.setCellWidget(row, column, item)
    table_widget.repaint()
    table_widget.adjustSize()
    item = set_button_style(item)  # update button with icon
    return item


def update_table_size(table_widget: QTableWidget):
    width = table_widget.width()  # width of game table
    table_widget.setColumnWidth(0, width * 40 // 100)  # 40% size for Name columns
    table_widget.setColumnWidth(1, width * 25 // 100)  # 25% for sb/bb column
    table_widget.setColumnWidth(2, width * 20 // 100)  # 20% for seats
    table_widget.setColumnWidth(3, width * 15 // 100)  # 15% for join column
