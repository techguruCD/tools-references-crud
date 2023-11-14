from PySide6 import (
    QtCore,
    QtGui,
    QtWidgets
)
from settings import colors
import datetime
from tools import get_utc_offset, calculate_date_with_offset
tr = QtCore.QCoreApplication.translate

class DateEditDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self) -> None:
        super().__init__()

    def createEditor(self, parent, option, index) -> QtWidgets.QWidget:
        date_edit = QtWidgets.QDateTimeEdit(parent=parent, displayFormat='dd/MM/yyyy hh:mm')
        date_edit.setFrame(False)
        date_edit.setObjectName('Input')

        return date_edit

    def setEditorData(self, editor, index) -> None:
        date_str = index.model().data(index, QtCore.Qt.ItemDataRole.EditRole)
        editor.setDateTime(QtCore.QDateTime.fromString(date_str, 'yyyy-MM-ddThh:mm:ss'))
    
    def setModelData(self, editor, model, index) -> None:
        date_str = editor.dateTime().toString('yyyy-MM-ddThh:mm:00') + get_utc_offset()
        model.setData(index, date_str, QtCore.Qt.ItemDataRole.EditRole)
    
    def updateEditorGeometry(self, editor, option, index) -> None:
        editor.setGeometry(option.rect)

class LineEditDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self) -> None:
        super().__init__()

    def createEditor(self, parent, option, index) -> QtWidgets.QWidget:
        line_edit = QtWidgets.QLineEdit(parent=parent)
        line_edit.setFrame(False)
        line_edit.setObjectName('Input')

        return line_edit

    def setEditorData(self, editor, index) -> None:
        text = index.model().data(index, QtCore.Qt.ItemDataRole.EditRole)
        editor.setText(text)
    
    def setModelData(self, editor, model, index) -> None:
        text = editor.text()
        model.setData(index, text, QtCore.Qt.ItemDataRole.EditRole)
    
    def updateEditorGeometry(self, editor, option, index) -> None:
        editor.setGeometry(option.rect)


class NamedDateTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data) -> None:
        super().__init__()
        self._data = data
    
    def flags(self, index):
        flags = super().flags(index)
        if index.column() in (1, 2):
            flags |= QtCore.Qt.ItemFlag.ItemIsEditable
        return flags

    def data(self, index, role):
        row = index.row()
        if role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            return QtCore.Qt.AlignmentFlag.AlignCenter

        match index.column():
            case 0: # button to delete:
                if role == QtCore.Qt.ItemDataRole.DisplayRole:
                    return '⊖'
            case 1: # name
                if role in (QtCore.Qt.ItemDataRole.DisplayRole, QtCore.Qt.ItemDataRole.EditRole):
                    return self._data[row]['name']
            case 2: # date
                if role == QtCore.Qt.ItemDataRole.DisplayRole:
                    return datetime.datetime.fromisoformat(calculate_date_with_offset(self._data[row]['date'])).strftime('%d/%m/%Y %H:%M')
                elif role == QtCore.Qt.ItemDataRole.EditRole:
                    date_str = calculate_date_with_offset(self._data[row]['date'])
                    if '+' in date_str:
                        date_str = date_str.split('+')[0]
                    return date_str
        
        if role == QtCore.Qt.ItemDataRole.ForegroundRole:
            if index.column() == 0:
                return QtGui.QColor('#FF0000')
        
        # change colors
        if role == QtCore.Qt.ItemDataRole.BackgroundRole:
            if index.row() % 2 != 0:
                return QtGui.QColor(colors['table_color_1'])
            else:
                return QtGui.QColor(colors['table_color_2'])

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                match section:
                    case 0:
                        return tr('NamedDateTableModel - Delete', 'Delete')
                    case 1:
                        return tr('NamedDateTableModel - Name', 'Name')
                    case 2:
                        return tr('NamedDateTableModel - Date', 'Date')
        
            if orientation == QtCore.Qt.Orientation.Vertical:
                return str(section + 1)

    def setData(self, index, value, role):
        row = index.row()

        if role == QtCore.Qt.ItemDataRole.EditRole:
            match index.column():
                case 1:
                    self._data[row]['name'] = value
                    return True
                case 2:
                    self._data[row]['date'] = value
                    return True

        return False

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 3
