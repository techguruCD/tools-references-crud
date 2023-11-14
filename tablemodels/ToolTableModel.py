from PySide6 import (
    QtCore,
    QtGui,
    QtWidgets
)
from settings import colors
tr = QtCore.QCoreApplication.translate

# Name of the apartment, Phone number, First and Last name of the owner
class ToolTableModel(QtCore.QAbstractTableModel):
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
            # 'SN'
            # 'category'
            # 'platform'
            # 'license_type'
            # 'api_support'
            # 'name'
            # 'uid'
            # 'description'
            # 'version'
            # 'release_date'
            # 'lastupdated_date'
            # 'producer'
            # 'rating'
            # 'downloadlink'
            # 'editor_choice'
            match index.column():
                case 0: # SN
                    return self._data[row]['SN']
                case 1: # category
                    return self._data[row]['category']
                case 2: # platform
                    return self._data[row]['platform']
                case 3: # license_type
                    return self._data[row]['license_type']
                case 4: # api_support
                    return self._data[row]['api_support']
                case 5: # name
                    return self._data[row]['name']
                case 6: # uid
                    return self._data[row]['uid']
                case 7: # description
                    return self._data[row]['description']
                case 8: # version
                    return self._data[row]['version']
                case 9: # release_date
                    return self._data[row]['release_date']
                case 10: # lastupdated_date
                    return self._data[row]['lastupdated_date']
                case 11: # producer
                    return self._data[row]['producer']
                case 12: # rating
                    return self._data[row]['rating']
                case 13: # downloadlink
                    return self._data[row]['downloadlink']
                case 14: # editor_choice
                    return self._data[row]['editor_choice']

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
                    case 0: # SN
                        return 'SN'
                    case 1: # category
                        return 'Category'
                    case 2: # platform
                        return 'Platform'
                    case 3: # license_type
                        return 'License Type'
                    case 4: # api_support
                        return 'Api Support'
                    case 5: # name
                        return 'Name'
                    case 6: # uid
                        return 'UID'
                    case 7: # description
                        return 'Description'
                    case 8: # version
                        return 'Version'
                    case 9: # release_date
                        return 'Release Date'
                    case 10: # lastupdated_date
                        return 'Lastupdated Date'
                    case 11: # producer
                        return 'Producer'
                    case 12: # rating
                        return 'Rating'
                    case 13: # Download Link
                        return 'Downloadlink'
                    case 14: # Editor Choice
                        return 'Editor Choice'
        
            if orientation == QtCore.Qt.Vertical:
                return str(section + 1)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 15