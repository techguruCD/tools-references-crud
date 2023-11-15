from PySide6 import QtCore
from PySide6.QtCore import QDate, QPoint
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
    QSizePolicy,
    QCalendarWidget,
    QMessageBox
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

        self.release_date_calendar = QCalendarWidget()
        self.lastupdated_date_calendar = QCalendarWidget(self)

        self.release_date_calendar.clicked.connect(self.release_date_calendar_click)
        self.lastupdated_date_calendar.clicked.connect(self.lastupdated_date_calendar_click)
        self.release_date_calendar.close()
        self.lastupdated_date_calendar.close()

        self.release_date_calendar.setWindowFlags(QtCore.Qt.Popup)
        self.lastupdated_date_calendar.setWindowFlags(QtCore.Qt.Popup)

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

        self.description = QTextEdit(self)
        mainLayout.addWidget(InputWrapper('Description', self.description))

        self.version = QLineEdit(self)
        self.release_date_button = QPushButton('2000-01-01', self)
        self.release_date_button.clicked.connect(self.release_date_button_click)
        self.lastupdated_date_button = QPushButton('2000-01-01', self)
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
        wrapper = InputWrapper('Rating', self.rating)
        wrapper.setMinimumWidth(100)
        layout.addWidget(wrapper)
        wrapper = InputWrapper('Editor Choice', self.editor_choice)
        wrapper.setMinimumWidth(130)
        layout.addWidget(wrapper)
        mainLayout.addLayout(layout)

        self.downloadlink = QLineEdit(self)
        mainLayout.addWidget(InputWrapper('Download Link', self.downloadlink))

        # mainLayout.addItem(QSpacerItem(
        #     1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

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
            'platform': int(self.platform.currentText()),
            'license_type': int(self.license_type.currentText()),
            'api_support': int(self.api_support.currentText()),
            'name': self.name.text(),
            'uid': self.uid.text(),
            'description': self.description.toPlainText(),
            'version': self.version.text(),
            'release_date': self.release_date_button.text(),
            'lastupdated_date': self.lastupdated_date_button.text(),
            'producer': self.producer.text(),
            'rating': int(self.rating.currentText()),
            'downloadlink': self.downloadlink.text(),
            'editor_choice': int(self.editor_choice.currentText()),
        }

        if self._SN != None:
            data['SN'] = self._SN
        success, tool = ToolApi.update_tool(
            data) if self._SN != None else ToolApi.create_tool(data)
        if success:
            QMessageBox.information(self, 'Success', "Saved Successfully")
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