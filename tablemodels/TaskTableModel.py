from PySide6 import (
    QtCore,
    QtGui,
    QtWidgets
)
from settings import colors
tr = QtCore.QCoreApplication.translate

class TaskTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data) -> None:
        super().__init__()
        self._data = data
    
    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            return QtCore.Qt.AlignmentFlag.AlignCenter

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            row = index.row()
            match index.column():
                case 0: # id
                    return self._data[row]['id']
                case 1: # nearest date
                    return self._data[row]['nearest_date']
                case 2: # creation date
                    return self._data[row]['date']
                case 3: # text
                    return self._data[row]['text']
                case 4: # apartment name
                    return self._data[row]['lease_contract']['apartment']['name'] + ' ' + self._data[row]['lease_contract']['apartment']['unique_identifier']

        # change colors
        if role == QtCore.Qt.ItemDataRole.BackgroundRole:
            if index.row() % 2 != 0:
                return QtGui.QColor(colors['table_color_1'])
            else:
                return QtGui.QColor(colors['table_color_2'])

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                match section:
                    case 0:
                        return 'id'
                    case 1:
                        return tr('TaskTableModel - Nearest date', 'Nearest date')
                    case 2:
                        return tr('TaskTableModel - Creation date', 'Creation date')
                    case 3:
                        return tr('TaskTableModel - Text', 'Text')
                    case 4:
                        return tr('TaskTableModel - Apartment name', 'Apartment name')
        
            if orientation == QtCore.Qt.Vertical:
                return str(section + 1)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 5
