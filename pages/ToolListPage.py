from PySide6.QtCore import (
    QModelIndex,
    Signal
)
from PySide6.QtWidgets import (
    QWidget,
    QComboBox,
    QLineEdit,
    QTextEdit,
    QDateEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QHBoxLayout,
)

from widgets.elements import InputWrapper
from api import ToolApi
from tablemodels import ToolTableModel

class ToolListPage(QWidget):
    item_edit = Signal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.__init__UI()
        self.update_data()

    def __init__UI(self):

        self.name_search = QLineEdit()
        self.name_search.setPlaceholderText('🔍')
        search_button = QPushButton('Search')
        search_button.setObjectName('DialogButton')
        search_button.clicked.connect(self.update_data)

        searchLayout = QHBoxLayout()
        searchLayout.addWidget(InputWrapper('Search', self.name_search))
        searchLayout.addWidget(search_button)

        self.tableview = QTableView()
        self.tableview.setModel(ToolTableModel([]))
        self.tableview.doubleClicked.connect(self.table_click)

        layout = QVBoxLayout()
        layout.addLayout(searchLayout)
        layout.addWidget(self.tableview)
        layout.setStretch(1, 1)
        self.setLayout(layout)

    def update_data(self):
        search = self.name_search.text()
        if search == "":
            search = None
        success, data = ToolApi.tool_list(search)
        if success:
            table_model = ToolTableModel(data)
            self.tableview.setModel(table_model)

    def table_click(self, index: QModelIndex):
        self.item_edit.emit(self.tableview.model()._data[index.row()]['SN'])