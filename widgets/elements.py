from PySide6 import(
    QtCore,
    QtWidgets
)

class InputWrapper(QtWidgets.QGroupBox):
    def __init__(self, text: str, widget: QtWidgets.QWidget):
        super().__init__()
        self.setObjectName('InputWrapper')
        widget.setObjectName('Input')

        self.setTitle(text)
        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(5, 15, 5, 5)
        layout.setSpacing(0)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(widget)
        self.setLayout(layout)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
