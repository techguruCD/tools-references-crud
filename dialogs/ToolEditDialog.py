from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout
)

from pages import ToolPage

# Dialog class to show tool editing form
class ToolEditDialog(QDialog):
    def __init__(self, parent, SN):
        super().__init__(parent)
        self._SN = SN
        self.setWindowTitle('Tool Edit: SN(' + str(SN) + ')')
        self.__init__UI()

    def __init__UI(self):

        self.page = ToolPage(self, self._SN)
        self.page.save_button.clicked.connect(self._save)
        self.page.cancel_button.clicked.connect(self.reject)
        self.page.delete_button.clicked.connect(self._delete)

        layout = QVBoxLayout()
        layout.addWidget(self.page)

        self.setLayout(layout)

    def _save(self):
        success = self.page._save()
        if success:
            self.accept()

    def _delete(self):
        success = self.page._delete()
        if success:
            self.accept()
