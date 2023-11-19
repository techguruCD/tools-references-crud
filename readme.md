## Getting Started

Install dependencies

```bash
pip install -r requirements.txt
```

Starting app
```bash
python main.py
```


## Add a new form widget
```bash
from widgets.elements import InputWrapper

class Page(QWidget):
    def __init__(self):
        InputWrapper('My Form', QLineEdit())
```

## Arranging form widgets
```bash
class Page(QWidget):
    def __init__(self):
        layout = QHBoxLayout()
        edit1 = QLineEdit()
        edit2 = QLineEdit()
        layout.addWidget(edit1)
        layout.addWidget(edit2)
        self.setLayout(layout)
```

## Adding toolbar
int __init__UI of MainWindow class
```bash
    toolbar = QToolBar('Main Toolbar')
    toolbar.setMovable(False)
    self.action_addtool = QAction('Add Tool', self)
    self.action_searchtool = QAction('Search Tool', self)
    self.action_addreference = QAction('Add Reference', self)
    self.action_searchreference = QAction('Search Reference', self)

    self.action_addtool.setCheckable(True)
    self.action_searchtool.setCheckable(True)
    self.action_addreference.setCheckable(True)
    self.action_searchreference.setCheckable(True)

    toolbar.addAction(self.action_addtool)
    toolbar.addAction(self.action_searchtool)
    toolbar.addAction(self.action_addreference)
    toolbar.addAction(self.action_searchreference)
    self.addToolBar(toolbar)
```

## Structure
```bash
├── api
│   ├── ReferenceApi.py => Api interface to access Reference Data
│   ├── ToolApi.py => Api interface to access Tool Data
├── data
│   ├── styles.qss => File with QSS style
├── dialogs
│   ├── ReferenceEditDialog.py => Dialog that shows Reference Form page for editing
│   ├── ToolEditDialog.py => Dialog that shows Tool Form page for editing
├── pages
│   ├── ReferenceListPage.py => Reference List Page to show list by search result
│   ├── ReferencePage.py => Reference Form page
│   ├── ToolListPage.py => Tool List Page shows search result
│   ├── ToolPage.py => Tool Form page
├── tablemodels
│   ├── ReferenceTableModel.py => Table Model to present reference data
│   ├── ToolTableModel.py => Table Model to present tool data
├── widgets
│   ├── elements.py => Group of classes that declares customized elements
├── models.py => DB Schema for data
├── main.py => MainWindow
└── settings.py => Common Settings
```