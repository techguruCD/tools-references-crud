from PySide6.QtCore import (
    QModelIndex,
    Signal
)
from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QHBoxLayout,
)

from widgets.elements import InputWrapper
from api import ToolApi
from tablemodels import ToolTableModel

# Tool List Page shows search result
class ToolListPage(QWidget):
    item_edit = Signal(int) # emitted when clicking table

    def __init__(self, parent):
        super().__init__(parent)
        self.__init__UI()
        self.update_data()
        self.tableview.resizeColumnsToContents()

    def __init__UI(self):
        self.name_search = QLineEdit()
        self.name_search.setPlaceholderText('🔍')
        search_button = QPushButton('Search')
        search_button.setObjectName('DialogButton')
        search_button.clicked.connect(self.update_data)

        searchLayout = QHBoxLayout()
        searchLayout.addWidget(InputWrapper('Name Search', self.name_search))
        searchLayout.addWidget(search_button)

        self.tableview = QTableView()
        self.tableview.setModel(ToolTableModel([]))
        self.tableview.hideColumn(0)
        self.tableview.hideColumn(4)
        self.tableview.hideColumn(6)
        self.tableview.hideColumn(7)
        self.tableview.hideColumn(8)
        self.tableview.hideColumn(9)
        self.tableview.hideColumn(12)
        self.tableview.hideColumn(13)
        self.tableview.hideColumn(14)
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