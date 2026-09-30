from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ParametresView(QWidget):
    def __init__(self, db):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Paramètres"))