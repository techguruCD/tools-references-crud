from PySide6.QtWidgets import (
    QWidget,
    QComboBox,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QMessageBox
)


from widgets.elements import InputWrapper
from api import ToolApi, ReferenceApi

import settings

# Reference Form page
class ReferencePage(QWidget):
    def __init__(self, parent, SN: int = None):
        super().__init__(parent)

        self._SN = SN   # None -> new form, not None -> editing form

        self.__init__UI()

        self._update_tool_list()
        if self._SN is not None:
            self.__load_reference()

    def __init__UI(self):

        self.name = QComboBox(self)
        self.type = QComboBox(self)
        for type in settings.reference_types:
            self.type.addItem(type)
        self.url = QLineEdit(self)
        self.summary = QTextEdit(self)

        layout = QVBoxLayout()

        layout.addWidget(InputWrapper('Name', self.name))
        layout.addWidget(InputWrapper('Type', self.type))
        layout.addWidget(InputWrapper('URL', self.url))
        layout.addWidget(InputWrapper('Summary', self.summary))

        layout.setStretch(3, 1)

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
        spacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        control_layout.addItem(spacer)
        control_layout.addWidget(self.save_button)
        control_layout.addWidget(self.delete_button)
        control_layout.addWidget(self.cancel_button)
        control_layout.setStretch(0, 1)

        layout.addLayout(control_layout)

        self.setLayout(layout)

    def clear_fields(self):
        self.name.setCurrentIndex(0)
        self.type.setCurrentIndex(0)
        self.url.setText('')
        self.summary.setText('')

    def _update_tool_list(self):
        success, data = ToolApi.tool_list()
        if success:
            while self.name.count():
                self.name.removeItem(0)
            self.name.addItem('')
            for item in data:
                self.name.addItem(item['name'])

    def _delete(self):
        if self._SN is None:
            return False
        success = ReferenceApi.delete_reference(self._SN)
        if success:
            QMessageBox.information(self, 'Success', "Deleted Successfully")
        else:
            QMessageBox.critical(self, 'Failed', "Deleting Failed")
        return success

    def _save(self):
        data = {
            'name': self.name.currentText(),
            'type': self.type.currentText(),
            'url': self.url.text(),
            'summary': self.summary.toPlainText()
        }
        if (data['name'] == '' or
            data['type'] == '' or
            data['url'] == '' or
                data['summary'] == ''):
            QMessageBox.warning(self, 'Warning', 'Please check inputs')
            return

        duplicate = ReferenceApi.check_duplicate(data['name'], self._SN)
        if duplicate:
            QMessageBox.warning(self, 'Warning', 'Duplicated name')
            return

        if self._SN != None:
            data['SN'] = self._SN
        success, reference = ReferenceApi.update_reference(
            data) if self._SN != None else ReferenceApi.create_reference(data)
        if success:
            QMessageBox.information(self, 'Success', "Saving Successfully")
            self.clear_fields()
        else:
            QMessageBox.critical(self, 'Failed', "Saving Failed")
        return success

    def __load_reference(self):
        success, reference = ReferenceApi.get_reference(self._SN)
        if success:
            self.name.setCurrentText(reference['name'])
            self.type.setCurrentText(str(reference['type']))
            self.url.setText(str(reference['url']))
            self.summary.setPlainText(str(reference['summary']))
