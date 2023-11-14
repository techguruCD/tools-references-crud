from PySide6 import (
    QtCore
)

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy
)

from pages import *
from dialogs import *
from models import create_tables

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.addToolPage = ToolPage(self)
        self.searchToolPage = ToolListPage(self)
        self.addReferencePage = ReferencePage(self)
        self.searchReferencePage = ReferenceListPage(self)

        self.addToolPage.save_button.clicked.connect(self.addToolPage._save)
        self.addReferencePage.save_button.clicked.connect(self.addReferencePage._save)
        self.searchToolPage.item_edit.connect(self.tool_edit_trigger)
        self.searchReferencePage.item_edit.connect(self.reference_edit_trigger)

        self.__init__UI()
        self.showPage('addtool')

    def __init__UI(self):
        toolbarlayout = QHBoxLayout()
        self.addtool = QPushButton('Add Tool', self)
        self.addtool.setCheckable(True)
        self.addtool.setObjectName('ToolButton')
        self.searchtool = QPushButton('Search Tool', self)
        self.searchtool.setCheckable(True)
        self.searchtool.setObjectName('ToolButton')
        self.addreference = QPushButton('Add Reference', self)
        self.addreference.setCheckable(True)
        self.addreference.setObjectName('ToolButton')
        self.searchreference = QPushButton('Search Reference', self)
        self.searchreference.setCheckable(True)
        self.searchreference.setObjectName('ToolButton')

        self.addtool.clicked.connect(self.addtool_click)
        self.searchtool.clicked.connect(self.searchtool_click)
        self.addreference.clicked.connect(self.addreference_click)
        self.searchreference.clicked.connect(self.searchreference_click)

        toolbarlayout.addItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        toolbarlayout.addWidget(self.addtool)
        toolbarlayout.addWidget(self.searchtool)
        toolbarlayout.addWidget(self.addreference)
        toolbarlayout.addWidget(self.searchreference)
        toolbarlayout.addItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        pagelayout = QVBoxLayout()
        pagelayout.addWidget(self.addToolPage)
        pagelayout.addWidget(self.searchToolPage)
        pagelayout.addWidget(self.addReferencePage)
        pagelayout.addWidget(self.searchReferencePage)

        layout = QVBoxLayout()
        layout.addLayout(toolbarlayout)
        layout.addLayout(pagelayout)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def showPage(self, key):
        self.addToolPage.hide()
        self.searchToolPage.hide()
        self.addReferencePage.hide()
        self.searchReferencePage.hide()

        self.addToolPage.setVisible(key == 'addtool')
        self.addtool.setChecked(key == 'addtool')
        self.searchToolPage.setVisible(key == 'searchtool')
        self.searchtool.setChecked(key == 'searchtool')
        self.addReferencePage.setVisible(key == 'addreference')
        self.addreference.setChecked(key == 'addreference')
        self.searchReferencePage.setVisible(key == 'searchreference')
        self.searchreference.setChecked(key == 'searchreference')

    def addtool_click(self):
        self.showPage('addtool')

    def searchtool_click(self):
        self.showPage('searchtool')

    def addreference_click(self):
        self.showPage('addreference')

    def searchreference_click(self):
        self.showPage('searchreference')

    def tool_edit_trigger(self, SN):
        if ToolEditDialog(self, SN).exec():
            self.searchToolPage.update_data()
            self.addReferencePage._update_tool_list()
    def reference_edit_trigger(self, SN):
        if ReferenceEditDialog(self, SN).exec():
            self.searchReferencePage.update_data()


if __name__ == '__main__':
    app = QApplication()
    create_tables()

    styles = open("data/styles.qss", 'r').read()
    app.setStyleSheet(styles)
    # app.setStyle('Fusion')

    window = MainWindow()
    window.show()
    app.exec()
