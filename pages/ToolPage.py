from PySide6 import QtCore
from PySide6.QtCore import QDate, QPoint
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
    QCalendarWidget,
    QMessageBox
)

import datetime
import hashlib

from widgets.elements import InputWrapper
from api import ToolApi, ReferenceApi
import settings

# Tool Form page
class ToolPage(QWidget):
    def __init__(self, parent, SN: int = None):
        super().__init__(parent)
        
        self._SN = SN # None -> new form, not None -> editing form

        self.__init__UI()

        if self._SN is not None:
            self.__load_tool()

    def __init__UI(self):
        mainLayout = QVBoxLayout()

        self.release_date_calendar = QCalendarWidget()
        self.lastupdated_date_calendar = QCalendarWidget(self)

        self.release_date_calendar.clicked.connect(self.release_date_calendar_click)
        self.lastupdated_date_calendar.clicked.connect(self.lastupdated_date_calendar_click)
        self.release_date_calendar.close()
        self.lastupdated_date_calendar.close()

        self.release_date_calendar.setWindowFlags(QtCore.Qt.Popup)
        self.lastupdated_date_calendar.setWindowFlags(QtCore.Qt.Popup)

        self.category = QComboBox(self)
        for category in settings.tool_categories:
            self.category.addItem(category)
        self.platform = QComboBox(self)
        for platform in settings.tool_platforms:
            self.platform.addItem(platform)
        layout = QHBoxLayout()
        layout.addWidget(InputWrapper('Category', self.category))
        layout.addWidget(InputWrapper('Platform', self.platform))
        mainLayout.addLayout(layout)

        self.license_type = QComboBox(self)
        for license_type in settings.tool_license_types:
            self.license_type.addItem(license_type)
        self.api_support = QComboBox(self)
        for api_support in settings.tool_api_supports:
            self.api_support.addItem(api_support)
        layout = QHBoxLayout()
        layout.addWidget(InputWrapper('License Type', self.license_type))
        layout.addWidget(InputWrapper('Api Support', self.api_support))
        mainLayout.addLayout(layout)

        self.name = QLineEdit(self)
        self.name.textEdited.connect(self.name_edited)
        self.uid = QLineEdit(self)
        self.uid.setReadOnly(True)
        layout = QHBoxLayout()
        layout.addWidget(InputWrapper('Name', self.name))
        layout.addWidget(InputWrapper('UID', self.uid))
        mainLayout.addLayout(layout)

        self.description = QTextEdit(self)
        mainLayout.addWidget(InputWrapper('Description', self.description))

        self.version = QLineEdit(self)
        self.release_date_button = QPushButton(QDate.currentDate().toString('yyyy-MM-dd'), self)
        self.release_date_button.clicked.connect(self.release_date_button_click)
        self.lastupdated_date_button = QPushButton(QDate.currentDate().toString('yyyy-MM-dd'), self)
        self.lastupdated_date_button.clicked.connect(self.lastupdated_date_button_click)
        layout = QHBoxLayout()
        layout.addWidget(InputWrapper('Version', self.version))
        wrapper = InputWrapper('Release Date', self.release_date_button)
        wrapper.setMinimumWidth(150)
        layout.addWidget(wrapper)
        wrapper = InputWrapper(
            'Last Updated Date', self.lastupdated_date_button)
        wrapper.setMinimumWidth(150)
        layout.addWidget(wrapper)
        mainLayout.addLayout(layout)

        self.producer = QLineEdit(self)
        self.rating = QComboBox(self)
        for rating in settings.tool_ratings:
            self.rating.addItem(rating)
        self.editor_choice = QComboBox(self)
        for editor_choice in settings.tool_editor_choices:
            self.editor_choice.addItem(editor_choice)
        layout = QHBoxLayout()
        layout.addWidget(InputWrapper('Producer', self.producer))
        wrapper = InputWrapper('Rating', self.rating)
        wrapper.setMinimumWidth(100)
        layout.addWidget(wrapper)
        wrapper = InputWrapper('Editor Choice', self.editor_choice)
        wrapper.setMinimumWidth(130)
        layout.addWidget(wrapper)
        mainLayout.addLayout(layout)

        self.downloadlink = QLineEdit(self)
        mainLayout.addWidget(InputWrapper('Download Link', self.downloadlink))

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
        spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        control_layout.addItem(spacer)
        control_layout.addWidget(self.save_button)
        control_layout.addWidget(self.delete_button)
        control_layout.addWidget(self.cancel_button)
        control_layout.setStretch(0, 1)

        mainLayout.addLayout(control_layout)

        mainLayout.setStretch(3, 1)

        self.setLayout(mainLayout)

    def release_date_button_click(self):
        release_date = datetime.date.fromisoformat(self.release_date_button.text())
        self.release_date_calendar.setSelectedDate(QDate(release_date.year, release_date.month, release_date.day))
        self.release_date_calendar.move(self.release_date_button.mapToGlobal(self.release_date_button.pos()) + QPoint(0, 10))
        self.release_date_calendar.show()
    
    def release_date_calendar_click(self, date: QDate):
        self.release_date_button.setText(date.toString('yyyy-MM-dd'))
        self.release_date_calendar.close()

    def lastupdated_date_button_click(self):
        self.lastupdated_date_calendar.setSelectedDate(QDate.fromString(self.lastupdated_date_button.text(), 'yyyy-MM-dd'))
        self.lastupdated_date_calendar.move(self.lastupdated_date_button.mapToGlobal(self.lastupdated_date_button.pos()) + QPoint(0, 10))
        self.lastupdated_date_calendar.show()

    def lastupdated_date_calendar_click(self, date: QDate):
        self.lastupdated_date_button.setText(date.toString('yyyy-MM-dd'))
        self.lastupdated_date_calendar.close()

    def name_edited(self, text):
        if text == '':
            self.uid.setText('')
        else:
            md5_hash = hashlib.md5()
            md5_hash.update(text.encode('utf-8'))
            self.uid.setText(md5_hash.hexdigest())

    def clear_fields(self):
        self.category.setCurrentIndex(0)
        self.platform.setCurrentIndex(0)
        self.license_type.setCurrentIndex(0)
        self.api_support.setCurrentIndex(0)
        self.name.setText('')
        self.name.textEdited.emit('')
        self.description.setText('')
        self.version.setText('')
        self.release_date_button.setText(QDate.currentDate().toString('yyyy-MM-dd'))
        self.lastupdated_date_button.setText(QDate.currentDate().toString('yyyy-MM-dd'))
        self.producer.setText('')
        self.rating.setCurrentIndex(0)
        self.editor_choice.setCurrentIndex(0)
        self.downloadlink.setText('')

    def _delete(self):
        if self._SN is None:
            return False
        success = ToolApi.delete_tool(self._SN)
        if success:
            QMessageBox.information(self, 'Success', "Deleted Successfully")
        else:
            QMessageBox.critical(self, 'Failed', "Deleting Failed")
        return success

    def _save(self):
        data = {
            'category': self.category.currentText(),
            'platform': self.platform.currentText(),
            'license_type': self.license_type.currentText(),
            'api_support': self.api_support.currentText(),
            'name': self.name.text(),
            'uid': self.uid.text(),
            'description': self.description.toPlainText(),
            'version': self.version.text(),
            'release_date': self.release_date_button.text(),
            'lastupdated_date': self.lastupdated_date_button.text(),
            'producer': self.producer.text(),
            'rating': self.rating.currentText(),
            'downloadlink': self.downloadlink.text(),
            'editor_choice': self.editor_choice.currentText(),
        }

        if (data['category'] == '' or
            data['platform'] == '' or
            data['license_type'] == '' or
            data['api_support'] == '' or
            data['name'] == '' or 
            data['description'] == '' or 
            data['version'] == '' or 
            data['producer'] == '' or 
            data['downloadlink'] == ''):
            QMessageBox.warning(self, 'Warning', 'Please check inputs')
            return
        
        duplicate = ToolApi.check_duplicate(data['name'], self._SN)
        if duplicate:
            QMessageBox.warning(self, 'Warning', 'Duplicated name')
            return
        data['platform'] = int(self.platform.currentText())
        data['license_type'] = int(self.license_type.currentText())
        data['api_support'] = int(self.api_support.currentText())
        if data['rating'] != '':
            data['rating'] = int(self.rating.currentText())
        else:
            data['rating'] = None
        if data['editor_choice'] != '':
            data['editor_choice'] = int(self.editor_choice.currentText())
        else:
            data['editor_choice'] = None

        if self._SN != None:
            data['SN'] = self._SN
        success, tool = ToolApi.update_tool(
            data) if self._SN != None else ToolApi.create_tool(data)
        if success:
            QMessageBox.information(self, 'Success', "Saved Successfully")
            self.clear_fields()
        else:
            QMessageBox.critical(self, 'Failed', "Saving Failed")
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
            self.description.setPlainText(tool['description'])
            self.version.setText(tool['version'])
            
            self.release_date_button.setText(tool['release_date'])
            self.lastupdated_date_button.setText(tool['lastupdated_date'])
            self.producer.setText(tool['producer'])
            self.rating.setCurrentText(str(tool['rating']))
            self.downloadlink.setText(tool['downloadlink'])
            self.editor_choice.setCurrentText(str(tool['editor_choice']))

            if ReferenceApi.check_duplicate(tool['name']):
                self.delete_button.hide()