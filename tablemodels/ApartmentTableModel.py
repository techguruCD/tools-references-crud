from PySide6 import (
    QtCore,
    QtGui,
    QtWidgets
)
from settings import colors
tr = QtCore.QCoreApplication.translate

class ApartmentTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data) -> None:
        super().__init__()
        self._data = data
    
    def flags(self, index):
        flags = super().flags(index)
        if index.column() == 1:
            flags |= QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable
        return flags

    def data(self, index, role):
        row = index.row()
        if role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            return QtCore.Qt.AlignmentFlag.AlignCenter

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            match index.column():
                case 0: # id
                    return self._data[row]['id']
                case 1: # owner name
                    return self._data[row]['owner']['first_name'] + ' ' + self._data[row]['owner']['last_name']
                case 2: # address
                    return self._data[row]['address']
                case 3: # apartment name
                    return self._data[row]['name'],
                case 4: # unique identifier
                    return self._data[row]['unique_identifier']

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
                        return tr('ApartmentTableModel - Apartment owner name', 'Owner name')
                    case 2:
                        return tr('ApartmentTableModel - Address', 'Address')
                    case 3:
                        return tr('ApartmentTableModel - Apartment name', 'Apartment name')
                    case 4:
                        return tr('ApartmentTableModel - Unique identifier', 'Unique identifier')
        
            if orientation == QtCore.Qt.Vertical:
                return str(section + 1)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 5