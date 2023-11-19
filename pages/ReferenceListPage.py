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
    QHBoxLayout
)

from widgets.elements import InputWrapper
from api import ReferenceApi
from tablemodels import ReferenceTableModel

# Reference List Page to show list by search result


class ReferenceListPage(QWidget):
    item_edit = Signal(int)  # signal emitted when clicking table

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
        self.tableview.hideColumn(0)
        self.tableview.doubleClicked.connect(self.table_click)

        layout = QVBoxLayout()
        layout.addLayout(searchLayout)
        layout.addWidget(self.tableview)
        layout.setStretch(1, 1)
        self.setLayout(layout)

    # get search result
    def update_data(self):
        search = self.name_search.text()
        if search == "":
            search = None
        success, data = ReferenceApi.reference_list(search)
        if success:
            table_model = ReferenceTableModel(data)
            self.tableview.setModel(table_model)

    def table_click(self, index: QModelIndex):
        self.item_edit.emit(self.tableview.model()._data[index.row()]['SN'])
