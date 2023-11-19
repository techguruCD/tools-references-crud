from PySide6 import (
    QtCore,
    QtGui
)
from settings import colors
tr = QtCore.QCoreApplication.translate

# Table Model to present reference data
class ReferenceTableModel(QtCore.QAbstractTableModel):
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
                case 0: # SN
                    return self._data[row]['SN']
                case 1: # name
                    return self._data[row]['name']
                case 2: # type
                    return self._data[row]['type']
                case 3: # url
                    return self._data[row]['url']
                case 4: # summary
                    return self._data[row]['summary']

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
                        return 'SN'
                    case 1:
                        return 'Name'
                    case 2:
                        return 'Type'
                    case 3:
                        return 'URL'
                    case 4:
                        return 'Summary'
        
            if orientation == QtCore.Qt.Vertical:
                return str(section + 1)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 5