import os

from PySide6 import (
    QtCore
)

from PySide6.QtGui import QAction

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QToolBar,
    QGroupBox
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

        self.addToolPage.save_button.clicked.connect(self._create_tool)
        self.addReferencePage.save_button.clicked.connect(self._create_reference)
        self.searchToolPage.item_edit.connect(self.tool_edit_trigger)
        self.searchReferencePage.item_edit.connect(self.reference_edit_trigger)

        self.__init__UI()
        self.addtool_click()

    def connect_actions(self, connect):
        self.action_addtool.blockSignals(not connect)
        self.action_searchtool.blockSignals(not connect)
        self.action_addreference.blockSignals(not connect)
        self.action_searchreference.blockSignals(not connect)

    def set_action_checked_all(self, checked):
        self.action_addtool.setChecked(checked)
        self.action_searchtool.setChecked(checked)
        self.action_addreference.setChecked(checked)
        self.action_searchreference.setChecked(checked)

    def __init__UI(self):

        toolbar = QToolBar('Main Toolbar')
        toolbar.setMovable(False)
        self.action_addtool = QAction('Add Tool', self)
        self.action_searchtool = QAction('Search Tool', self)
        self.action_addreference = QAction('Add Reference', self)
        self.action_searchreference = QAction('Search Reference', self)

        self.action_addtool.setCheckable(True)
        self.action_searchtool.setCheckable(True)
        self.action_addreference.setCheckable(True)
        self.action_searchreference.setCheckable(True)

        toolbar.addAction(self.action_addtool)
        toolbar.addAction(self.action_searchtool)
        toolbar.addAction(self.action_addreference)
        toolbar.addAction(self.action_searchreference)
        self.addToolBar(toolbar)

        self.action_addtool.triggered.connect(self.addtool_click)
        self.action_searchtool.triggered.connect(self.searchtool_click)
        self.action_addreference.triggered.connect(self.addreference_click)
        self.action_searchreference.triggered.connect(
            self.searchreference_click)

        # toolbarlayout = QHBoxLayout()
        # self.addtool = QPushButton('Add Tool', self)
        # self.addtool.setCheckable(True)
        # self.addtool.setObjectName('ToolButton')
        # self.searchtool = QPushButton('Search Tool', self)
        # self.searchtool.setCheckable(True)
        # self.searchtool.setObjectName('ToolButton')
        # self.addreference = QPushButton('Add Reference', self)
        # self.addreference.setCheckable(True)
        # self.addreference.setObjectName('ToolButton')
        # self.searchreference = QPushButton('Search Reference', self)
        # self.searchreference.setCheckable(True)
        # self.searchreference.setObjectName('ToolButton')

        # self.addtool.clicked.connect(self.addtool_click)
        # self.searchtool.clicked.connect(self.searchtool_click)
        # self.addreference.clicked.connect(self.addreference_click)
        # self.searchreference.clicked.connect(self.searchreference_click)

        # toolbarlayout.addItem(QSpacerItem(
        #     1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        # toolbarlayout.addWidget(self.addtool)
        # toolbarlayout.addWidget(self.searchtool)
        # toolbarlayout.addWidget(self.addreference)
        # toolbarlayout.addWidget(self.searchreference)
        # toolbarlayout.addItem(QSpacerItem(
        #     1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        pagelayout = QVBoxLayout()
        pagelayout.addWidget(self.addToolPage)
        pagelayout.addWidget(self.searchToolPage)
        pagelayout.addWidget(self.addReferencePage)
        pagelayout.addWidget(self.searchReferencePage)

        layout = QHBoxLayout()
        leftSpace = QGroupBox()
        leftSpace.setMinimumWidth(200)
        layout.addWidget(leftSpace)
        # layout.addLayout(toolbarlayout)
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
        # self.addtool.setChecked(key == 'addtool')
        self.searchToolPage.setVisible(key == 'searchtool')
        # self.searchtool.setChecked(key == 'searchtool')
        self.addReferencePage.setVisible(key == 'addreference')
        # self.addreference.setChecked(key == 'addreference')
        self.searchReferencePage.setVisible(key == 'searchreference')
        # self.searchreference.setChecked(key == 'searchreference')

    def addtool_click(self):
        self.connect_actions(False)
        self.showPage('addtool')
        self.set_action_checked_all(False)
        self.action_addtool.setChecked(True)
        self.connect_actions(True)

    def searchtool_click(self):
        self.connect_actions(False)
        self.showPage('searchtool')
        self.set_action_checked_all(False)
        self.action_searchtool.setChecked(True)
        self.connect_actions(True)

    def addreference_click(self):
        self.connect_actions(False)
        self.showPage('addreference')
        self.set_action_checked_all(False)
        self.action_addreference.setChecked(True)
        self.connect_actions(True)

    def searchreference_click(self):
        self.connect_actions(False)
        self.showPage('searchreference')
        self.set_action_checked_all(False)
        self.action_searchreference.setChecked(True)
        self.connect_actions(True)

    def _create_tool(self):
        if self.addToolPage._save():
            self.searchToolPage.update_data()
            self.addReferencePage._update_tool_list()

    def _create_reference(self):
        if self.addReferencePage._save():
            self.searchReferencePage.update_data()

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

    styles = open(os.getcwd() + "\\data\\styles.qss", 'r').read()
    app.setStyleSheet(styles)
    # app.setStyle('Fusion')

    window = MainWindow()
    window.show()
    app.exec()
