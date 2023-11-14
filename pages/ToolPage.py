from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QWidget,
    QComboBox,
    QLineEdit,
    QTextEdit,
    QDateEdit,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy
)

import datetime

from widgets.elements import InputWrapper
from api import ToolApi


class ToolPage(QWidget):
    def __init__(self, parent, SN: int = None):
        super().__init__(parent)
        
        self._SN = SN

        self.__init__UI()

        if self._SN is not None:
            self.__load_tool()

    def __init__UI(self):

        mainLayout = QVBoxLayout()

        self.category = QComboBox(self)
        self.platform = QComboBox(self)
        self.platform.addItem('1')
        self.platform.addItem('2')
        self.platform.addItem('3')
        self.platform.addItem('4')
        layout = QHBoxLayout()
        layout.addWidget(InputWrapper('Category', self.category))
        layout.addWidget(InputWrapper('Platform', self.platform))
        mainLayout.addLayout(layout)

        self.license_type = QComboBox(self)
        self.license_type.addItem('1')
        self.license_type.addItem('2')
        self.license_type.addItem('3')
        self.api_support = QComboBox(self)
        self.api_support.addItem('0')
        self.api_support.addItem('1')
        layout = QHBoxLayout()
        layout.addWidget(InputWrapper('License Type', self.license_type))
        layout.addWidget(InputWrapper('Api Support', self.api_support))
        mainLayout.addLayout(layout)

        self.name = QLineEdit(self)
        self.uid = QLineEdit(self)
        layout = QHBoxLayout()
        layout.addWidget(InputWrapper('Name', self.name))
        layout.addWidget(InputWrapper('UID', self.uid))
        mainLayout.addLayout(layout)

        self.description = QLineEdit(self)
        mainLayout.addWidget(InputWrapper('Description', self.description))

        self.version = QLineEdit(self)
        self.release_date = QDateEdit(self)
        self.lastupdated_date = QDateEdit(self)
        layout = QHBoxLayout()
        layout.addWidget(InputWrapper('Version', self.version))
        layout.addWidget(InputWrapper('Release Date', self.release_date))
        layout.addWidget(InputWrapper(
            'Last Updated Date', self.lastupdated_date))
        mainLayout.addLayout(layout)

        self.producer = QLineEdit(self)
        self.rating = QComboBox(self)
        self.rating.addItem('1')
        self.rating.addItem('2')
        self.rating.addItem('3')
        self.rating.addItem('4')
        self.rating.addItem('5')
        self.rating.addItem('6')
        self.rating.addItem('7')
        self.rating.addItem('8')
        self.rating.addItem('9')
        self.rating.addItem('10')
        self.editor_choice = QComboBox(self)
        self.editor_choice.addItem('0')
        self.editor_choice.addItem('1')
        layout = QHBoxLayout()
        layout.addWidget(InputWrapper('Producer', self.producer))
        layout.addWidget(InputWrapper('Rating', self.rating))
        layout.addWidget(InputWrapper('Editor Choice', self.editor_choice))
        mainLayout.addLayout(layout)

        self.downloadlink = QLineEdit(self)
        mainLayout.addWidget(InputWrapper('Download Link', self.downloadlink))

        mainLayout.addItem(QSpacerItem(
            1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.save_button = QPushButton('Save', self)
        self.save_button.setObjectName('GreenButton')

        self.delete_button = QPushButton('Delete', self)
        self.delete_button.setObjectName('DialogButton')

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.setObjectName('LightBlueButton')

        if self._SN is None:
            self.delete_button.hide()
            self.cancel_button.hide()

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.save_button)
        control_layout.addWidget(self.delete_button)
        control_layout.addWidget(self.cancel_button)

        mainLayout.addLayout(control_layout)

        mainLayout.setStretch(7, 1)

        self.setLayout(mainLayout)

    def _delete(self):
        if self._SN is None:
            return False
        return ToolApi.delete_tool(self._SN)

    def _save(self):
        data = {
            'category': self.category.currentText(),
            'platform': int(self.platform.currentText()),
            'license_type': int(self.license_type.currentText()),
            'api_support': int(self.api_support.currentText()),
            'name': self.name.text(),
            'uid': self.uid.text(),
            'description': self.description.text(),
            'version': self.version.text(),
            'release_date': self.release_date.date().toString('yyyy-MM-dd'),
            'lastupdated_date': self.lastupdated_date.date().toString('yyyy-MM-dd'),
            'producer': self.producer.text(),
            'rating': int(self.rating.currentText()),
            'downloadlink': self.downloadlink.text(),
            'editor_choice': int(self.editor_choice.currentText()),
        }

        if self._SN != None:
            data['SN'] = self._SN
        success, tool = ToolApi.update_tool(
            data) if self._SN != None else ToolApi.create_tool(data)
        return success

    def __load_tool(self):
        success, tool = ToolApi.get_tool(self._SN)
        if success:
            self.category.setCurrentText(tool['category'])
            self.platform.setCurrentText(str(tool['platform']))
            self.license_type.setCurrentText(str(tool['license_type']))
            self.api_support.setCurrentText(str(tool['api_support']))
            self.name.setText(tool['name'])
            self.uid.setText(tool['uid'])
            self.description.setText(tool['description'])
            self.version.setText(tool['version'])
            release_date = datetime.date.fromisoformat(tool['release_date'])
            self.release_date.setDate(
                QDate(release_date.year, release_date.month, release_date.day))
            lastupdated_date = datetime.date.fromisoformat(
                tool['lastupdated_date'])
            self.lastupdated_date.setDate(
                QDate(lastupdated_date.year, lastupdated_date.month, lastupdated_date.day))
            self.producer.setText(tool['producer'])
            self.rating.setCurrentText(str(tool['rating']))
            self.downloadlink.setText(tool['downloadlink'])
            self.editor_choice.setCurrentText(str(tool['editor_choice']))