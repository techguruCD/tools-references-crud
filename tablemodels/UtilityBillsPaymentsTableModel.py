from PySide6 import (
    QtCore,
    QtGui,
    QtWidgets
)
from settings import colors
import datetime
tr = QtCore.QCoreApplication.translate

class UtilityBillsPaymentsTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data) -> None:
        super().__init__()
        self._data = data

        for row in self._data:
            row['changed'] = False
    
    def flags(self, index):
        flags = super().flags(index)
        if index.column() == 1:
            flags |= QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsUserCheckable
        return flags

    def data(self, index, role):
        row = index.row()
        if role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            return QtCore.Qt.AlignmentFlag.AlignCenter

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            match index.column():
                case 0: # id
                    return self._data[row]['id']
                case 1: # paid [checkbox]
                    return 'Paid'
                case 2: # month
                    return datetime.datetime.fromisoformat(self._data[row]['date']).strftime('%m')
                case 3: # amount
                    return self._data[row]['amount']
                case 4: # Tenant's first and last name
                    return self._data[row]['lease_contract']['tenant']['first_name'] + ' ' + self._data[row]['lease_contract']['tenant']['last_name']
                case 5: # apartment name
                    return self._data[row]['lease_contract']['apartment']['name'] + ' ' + self._data[row]['lease_contract']['apartment']['unique_identifier']
        
        if role == QtCore.Qt.ItemDataRole.CheckStateRole:
            if index.column() == 1:
                if self._data[row]['paid']:
                    return QtCore.Qt.CheckState.Checked
                else:
                    return QtCore.Qt.CheckState.Unchecked

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
                        return 'id'
                    case 1:
                        return tr('UtilityPaymentTableModel - Paid', 'Paid')
                    case 2:
                        return tr('UtilityPaymentTableModel - Month', 'Month')
                    case 3:
                        return tr('UtilityPaymentTableModel - Amount', 'Amount')
                    case 4:
                        return tr('UtilityPaymentTableModel - Tenant', 'Tenant')
                    case 5:
                        return tr('UtilityPaymentTableModel - Apartment name', 'Apartment name')
        
            if orientation == QtCore.Qt.Orientation.Vertical:
                return str(section + 1)

    def setData(self, index, value, role):
        row = index.row()
        column = index.column()
        if role == QtCore.Qt.ItemDataRole.CheckStateRole and column == 1:
            self._data[row]['changed'] = True
            
            if value == 2:
                self._data[row]['paid'] = True
                self.dataChanged.emit(index, index)
            elif value == 0:
                self._data[row]['paid'] = False
                self.dataChanged.emit(index, index)
            
            return True

        return False

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 6