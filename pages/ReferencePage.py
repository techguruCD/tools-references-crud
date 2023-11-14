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
from api import ToolApi, ReferenceApi

class ReferencePage(QWidget):
    def __init__(self, parent, SN: int = None):
        super().__init__(parent)
        
        self._SN = SN
        
        self.__init__UI()

        self._update_tool_list()
        if self._SN is not None:
            self.__load_reference()

    def __init__UI(self):

        self.name = QComboBox(self)
        self.type = QComboBox(self)
        self.type.addItem('tutorials')
        self.type.addItem('blogs')
        self.type.addItem('video')
        self.type.addItem('datasets')
        self.url = QLineEdit(self)
        self.summary = QLineEdit(self)

        layout = QVBoxLayout()

        layout.addWidget(InputWrapper('Name', self.name))
        layout.addWidget(InputWrapper('Type', self.type))
        layout.addWidget(InputWrapper('URL', self.url))
        layout.addWidget(InputWrapper('Summary', self.summary))

        layout.addItem(QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.setStretch(4, 1)

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

        layout.addLayout(control_layout)

        self.setLayout(layout)

    def _update_tool_list(self):
        success, data = ToolApi.tool_list()
        if success:
            while self.name.count():
                self.name.removeItem(0)
            for item in data:
                self.name.addItem(item['name'])

    def _delete(self):
        if self._SN is None:
            return False
        return ReferenceApi.delete_reference(self._SN)

    def _save(self):
        data = {
            'name': self.name.currentText(),
            'type': self.type.currentText(),
            'url': self.url.text(),
            'summary': self.summary.text()
        }    
        if self._SN != None:
            data['SN'] = self._SN
        success, reference = ReferenceApi.update_reference(data) if self._SN != None else ReferenceApi.create_reference(data)
        return success
    def __load_reference(self):
        success, reference = ReferenceApi.get_reference(self._SN)
        if success:
            self.name.setCurrentText(reference['name'])
            self.type.setCurrentText(str(reference['type']))
            self.url.setText(str(reference['url']))
            self.summary.setText(str(reference['summary']))