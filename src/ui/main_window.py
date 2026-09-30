from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QStackedWidget,
    QLabel,
)

from src.ui.dashboard_view import DashboardView
from src.ui.eleves_view import ElevesView
from src.ui.parametres_view import ParametresView


class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db

        self.setWindowTitle("EduPaie — Gestion des paiements scolaires")
        self.resize(1280, 720)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout_principal = QHBoxLayout(central_widget)

        menu = QVBoxLayout()
        titre = QLabel("EduPaie")
        titre.setStyleSheet("font-size: 24px; font-weight: bold; padding: 15px;")

        self.btn_dashboard = QPushButton("Tableau de bord")
        self.btn_eleves = QPushButton("Élèves")
        self.btn_parametres = QPushButton("Paramètres")

        menu.addWidget(titre)
        menu.addWidget(self.btn_dashboard)
        menu.addWidget(self.btn_eleves)
        menu.addStretch()
        menu.addWidget(self.btn_parametres)

        self.pages = QStackedWidget()
        self.dashboard_page = DashboardView(db)
        self.eleves_page = ElevesView(db)
        self.parametres_page = ParametresView(db)

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.eleves_page)
        self.pages.addWidget(self.parametres_page)

        self.btn_dashboard.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.dashboard_page)
        )
        self.btn_eleves.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.eleves_page)
        )
        self.btn_parametres.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.parametres_page)
        )

        layout_principal.addLayout(menu, 1)
        layout_principal.addWidget(self.pages, 5)