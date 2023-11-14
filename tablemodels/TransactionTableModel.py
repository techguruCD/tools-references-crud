from PySide6 import (
    QtCore,
    QtGui,
    QtWidgets
)
from settings import colors
tr = QtCore.QCoreApplication.translate

# (Amount, Transaction type + color by transaction type (income green, expense red), Description
class TransactionTableModel(QtCore.QAbstractTableModel):
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
                case 1: # amount
                    return self._data[row]['amount']
                case 2: # transaction category
                    return self._data[row]['category']
                case 3: # transaction type   income/expense
                    return self._data[row]['transaction_type']
                case 4: # description
                    return self._data[row]['description']


        # change colors
        if role == QtCore.Qt.ItemDataRole.BackgroundRole:
            if index.row() % 2 != 0:
                return QtGui.QColor(colors['table_color_1'])
            else:
                return QtGui.QColor(colors['table_color_2'])
            
        # text color
        if role == QtCore.Qt.ItemDataRole.ForegroundRole:
            if self._data[row]['transaction_type'] == 'income':
                return QtGui.QColor(colors['green_normal'])
            else:
                return QtGui.QColor(colors['red_normal'])

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                match section:
                    case 0:
                        return 'id'
                    case 1:
                        return tr('TransactionTableModel - Amount', 'Amount')
                    case 2:
                        return tr('TransactionTableModel - Category', 'Category')
                    case 3:
                        return tr('TransactionTableModel - Transaction type', 'Transaction type')
                    case 4:
                        return tr('TransactionTableModel - Description', 'Description')
        
            if orientation == QtCore.Qt.Vertical:
                return str(section + 1)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 4