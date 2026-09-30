from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class DashboardView(QWidget):
    def __init__(self, db):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Tableau de bord"))