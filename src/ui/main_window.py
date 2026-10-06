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
        central_widget.setObjectName("mainArea")
        self.setCentralWidget(central_widget)

        layout_principal = QHBoxLayout(central_widget)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        barre_laterale = QWidget()
        barre_laterale.setObjectName("sidebar")
        barre_laterale.setFixedWidth(210)
        menu = QVBoxLayout(barre_laterale)
        menu.setContentsMargins(0, 22, 0, 14)
        menu.setSpacing(4)

        titre = QLabel("EduPaie")
        titre.setObjectName("brandTitle")
        sous_titre = QLabel("Paiements scolaires")
        sous_titre.setObjectName("brandSubtitle")
        menu.addWidget(titre)
        menu.addWidget(sous_titre)
        menu.addSpacing(22)

        self.btn_dashboard = self.creer_bouton_navigation("▦   Tableau de bord")
        self.btn_eleves = self.creer_bouton_navigation("♙   Élèves")
        self.btn_parametres = self.creer_bouton_navigation("⚙   Paramètres")

        menu.addWidget(self.btn_dashboard)
        menu.addWidget(self.btn_eleves)
        menu.addStretch()
        menu.addWidget(self.btn_parametres)
        version = QLabel("EduPaie v0.1.0")
        version.setObjectName("sidebarFooter")
        menu.addSpacing(10)
        menu.addWidget(version)

        self.pages = QStackedWidget()
        self.pages.setObjectName("pages")
        self.dashboard_page = DashboardView(db)
        self.eleves_page = ElevesView(db)
        self.parametres_page = ParametresView(db)
        self.parametres_page.donnees_restaurees.connect(self.actualiser_apres_restauration)

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.eleves_page)
        self.pages.addWidget(self.parametres_page)

        self.btn_dashboard.clicked.connect(self.afficher_tableau_de_bord)
        self.btn_eleves.clicked.connect(
            lambda: self.afficher_page(self.eleves_page, self.btn_eleves)
        )
        self.btn_parametres.clicked.connect(
            lambda: self.afficher_page(self.parametres_page, self.btn_parametres)
        )

        layout_principal.addWidget(barre_laterale)
        layout_principal.addWidget(self.pages, 1)
        self.btn_dashboard.setChecked(True)

    @staticmethod
    def creer_bouton_navigation(texte):
        bouton = QPushButton(texte)
        bouton.setObjectName("navButton")
        bouton.setCheckable(True)
        return bouton

    def afficher_page(self, page, bouton_actif):
        self.pages.setCurrentWidget(page)
        for bouton in (self.btn_dashboard, self.btn_eleves, self.btn_parametres):
            bouton.setChecked(bouton is bouton_actif)

    def afficher_tableau_de_bord(self):
        self.dashboard_page.actualiser()
        self.afficher_page(self.dashboard_page, self.btn_dashboard)

    def actualiser_apres_restauration(self):
        self.dashboard_page.actualiser()
        self.eleves_page.charger_classes()
        self.eleves_page.charger_eleves()
        self.eleves_page.pages_eleves.setCurrentWidget(self.eleves_page.liste_page)
