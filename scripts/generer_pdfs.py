"""Génère la documentation technique et le manuel utilisateur en PDF."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable, Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SORTIE = ROOT / "output" / "pdf"
ASSETS = ROOT / "docs" / "assets"
BLEU = colors.HexColor("#285b8f")
BLEU_FONCE = colors.HexColor("#1e456d")
BLEU_CLAIR = colors.HexColor("#e8f0f8")
TEXTE = colors.HexColor("#302637")
GRIS = colors.HexColor("#64748b")


def enregistrer_polices():
    normal = Path("C:/Windows/Fonts/segoeui.ttf")
    gras = Path("C:/Windows/Fonts/segoeuib.ttf")
    if normal.exists() and gras.exists():
        pdfmetrics.registerFont(TTFont("Segoe", str(normal)))
        pdfmetrics.registerFont(TTFont("Segoe-Bold", str(gras)))
        return "Segoe", "Segoe-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = enregistrer_polices()


def creer_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("DocTitle", parent=base["Title"], fontName=FONT_BOLD,
                                fontSize=23, leading=27, textColor=BLEU_FONCE,
                                alignment=TA_LEFT, spaceAfter=5),
        "subtitle": ParagraphStyle("DocSubtitle", parent=base["Normal"], fontName=FONT,
                                   fontSize=10, leading=14, textColor=GRIS, spaceAfter=12),
        "h1": ParagraphStyle("SectionHeading", parent=base["Heading1"], fontName=FONT_BOLD,
                             fontSize=15, leading=19, textColor=BLEU_FONCE,
                             spaceBefore=5, spaceAfter=7),
        "h2": ParagraphStyle("SubHeading", parent=base["Heading2"], fontName=FONT_BOLD,
                             fontSize=10.5, leading=14, textColor=BLEU,
                             spaceBefore=5, spaceAfter=4),
        "body": ParagraphStyle("BodyTextEdu", parent=base["BodyText"], fontName=FONT,
                               fontSize=8.8, leading=12.2, textColor=TEXTE, spaceAfter=5),
        "small": ParagraphStyle("SmallTextEdu", parent=base["BodyText"], fontName=FONT,
                                fontSize=7.6, leading=10, textColor=GRIS, spaceAfter=3),
        "table": ParagraphStyle("TableTextEdu", parent=base["BodyText"], fontName=FONT,
                                fontSize=7.7, leading=10, textColor=TEXTE),
        "table_head": ParagraphStyle("TableHeadEdu", parent=base["BodyText"], fontName=FONT_BOLD,
                                     fontSize=7.8, leading=10, textColor=colors.white),
        "center": ParagraphStyle("CenterEdu", parent=base["BodyText"], fontName=FONT,
                                 fontSize=8.8, leading=12, textColor=TEXTE, alignment=TA_CENTER),
    }


S = creer_styles()


def para(texte, style="body"):
    return Paragraph(texte, S[style])


def tableau(lignes, largeurs, entete=True):
    contenu = []
    for i, ligne in enumerate(lignes):
        style = "table_head" if entete and i == 0 else "table"
        contenu.append([para(str(cellule), style) for cellule in ligne])
    t = Table(contenu, colWidths=largeurs, repeatRows=1 if entete else 0, hAlign="LEFT")
    commandes = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#dbe2ea")),
    ]
    if entete:
        commandes.append(("BACKGROUND", (0, 0), (-1, 0), BLEU))
        commandes.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f8fb")]))
    else:
        commandes.append(("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f6f8fb")]))
    t.setStyle(TableStyle(commandes))
    return t


class DiagrammeMCD(Flowable):
    def __init__(self, width=17.1 * cm, height=7.1 * cm):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        boxes = {
            "classes": (0.2 * cm, 4.7 * cm, 4.3 * cm, 1.55 * cm,
                        "CLASSES", "id (PK)\nnom (unique)"),
            "annees": (0.2 * cm, 1.8 * cm, 4.3 * cm, 1.55 * cm,
                       "ANNEES_SCOLAIRES", "id (PK)\nlibelle (unique)"),
            "eleves": (6.1 * cm, 3.2 * cm, 4.7 * cm, 2.0 * cm,
                       "ELEVES", "id (PK), nom, prenom\nclasse_id (FK), annee_scolaire_id (FK)\ntotal_du, cree_le"),
            "paiements": (12.4 * cm, 4.7 * cm, 4.4 * cm, 1.8 * cm,
                          "PAIEMENTS", "id (PK), eleve_id (FK)\nmontant, date, mode\nrecu_id (FK, unique)"),
            "recus": (12.4 * cm, 1.8 * cm, 4.4 * cm, 1.8 * cm,
                      "RECUS", "id (PK), numero (unique)\ndate_emission, contenu_json"),
            "parametres": (6.1 * cm, 0.25 * cm, 4.7 * cm, 1.15 * cm,
                           "PARAMETRES", "cle (PK), valeur"),
        }
        for x, y, w, h, titre, champs in boxes.values():
            c.setFillColor(colors.white)
            c.setStrokeColor(BLEU)
            c.roundRect(x, y, w, h, 5, stroke=1, fill=1)
            c.setFillColor(BLEU)
            c.roundRect(x, y + h - 0.42 * cm, w, 0.42 * cm, 5, stroke=0, fill=1)
            c.rect(x, y + h - 0.42 * cm, w, 0.18 * cm, stroke=0, fill=1)
            c.setFillColor(colors.white)
            c.setFont(FONT_BOLD, 8)
            c.drawString(x + 0.16 * cm, y + h - 0.29 * cm, titre)
            c.setFillColor(TEXTE)
            c.setFont(FONT, 7.3)
            text = c.beginText(x + 0.16 * cm, y + h - 0.68 * cm)
            text.setLeading(0.32 * cm)
            for ligne in champs.split("\n"):
                text.textLine(ligne)
            c.drawText(text)

        def fleche(x1, y1, x2, y2, label):
            c.setStrokeColor(GRIS)
            c.setFillColor(GRIS)
            c.setLineWidth(1)
            c.line(x1, y1, x2, y2)
            c.line(x2 - 0.12 * cm, y2 + 0.08 * cm, x2, y2)
            c.line(x2 - 0.12 * cm, y2 - 0.08 * cm, x2, y2)
            c.setFont(FONT, 6.8)
            c.drawCentredString((x1 + x2) / 2, (y1 + y2) / 2 + 0.13 * cm, label)

        fleche(4.5 * cm, 5.4 * cm, 6.1 * cm, 4.65 * cm, "1 - n")
        fleche(4.5 * cm, 2.55 * cm, 6.1 * cm, 3.65 * cm, "1 - n")
        fleche(10.8 * cm, 4.45 * cm, 12.4 * cm, 5.25 * cm, "1 - n")
        fleche(14.6 * cm, 4.7 * cm, 14.6 * cm, 3.6 * cm, "1 - 1")


def pied_de_page(canvas, doc):
    canvas.saveState()
    page_w, _ = A4
    canvas.setStrokeColor(colors.HexColor("#dbe2ea"))
    canvas.line(1.8 * cm, 1.25 * cm, page_w - 1.8 * cm, 1.25 * cm)
    canvas.setFont(FONT, 7.4)
    canvas.setFillColor(GRIS)
    canvas.drawString(1.8 * cm, 0.85 * cm, "EduPaie | Documentation du projet")
    canvas.drawRightString(page_w - 1.8 * cm, 0.85 * cm, f"Page {doc.page}")
    canvas.restoreState()


def technique():
    SORTIE.mkdir(parents=True, exist_ok=True)
    chemin = SORTIE / "Documentation_technique.pdf"
    doc = SimpleDocTemplate(
        str(chemin), pagesize=A4, rightMargin=1.8 * cm, leftMargin=1.8 * cm,
        topMargin=1.55 * cm, bottomMargin=1.7 * cm,
        title="Documentation technique EduPaie", author="Projet EduPaie",
    )
    story = []

    story += [para("EDUPAIE", "title"),
              para("Documentation technique | Gestion locale des paiements scolaires", "subtitle"),
              para("1. Objectif et périmètre", "h1"),
              para("EduPaie aide un établissement à tenir les fiches d'élèves, les frais dus, les paiements successifs et les reçus. L'interface met en évidence les soldes et les trois statuts de règlement. La solution est une application Windows monoposte avec stockage SQLite local."),
              tableau([
                  ["Besoins couverts", "Réponse d'EduPaie"],
                  ["Suivre un élève", "Classe, année, frais annuels et statut calculé."],
                  ["Tracer les versements", "Paiements datés, mode de règlement, historique et numéro de reçu."],
                  ["Suivre l'établissement", "Tableau de bord des encaissements et soldes restants."],
              ], [5.1 * cm, 11.1 * cm]),
              Spacer(1, 8),
              para("Écran principal - tableau de bord", "h2"),
              Image(str(ASSETS / "tableau_de_bord.png"), width=16.2 * cm, height=10.13 * cm),
              para("Les chiffres et noms visibles proviennent exclusivement de la base fictive de démonstration.", "small"),
              PageBreak()]

    story += [para("2. Architecture logicielle", "h1"),
              para("Le code sépare l'affichage, les règles métier et l'accès aux données. Cette organisation évite de concentrer les requêtes et règles de paiement dans les widgets."),
              tableau([
                  ["Couche", "Modules", "Responsabilité"],
                  ["Interface", "src/ui/", "Fenêtre principale, liste/fiche, formulaires, filtres et style PySide6."],
                  ["Services", "src/services/", "Validation des paiements, indicateurs du tableau de bord et reçus PDF."],
                  ["Données", "src/data1/", "Connexion SQLite et requêtes regroupées dans les dépôts."],
                  ["Ressources", "database/, data/", "Schéma SQL et jeu de démonstration."],
              ], [2.5 * cm, 3.2 * cm, 10.5 * cm]),
              para("Flux d'un paiement", "h2"),
              tableau([
                  ["Étape", "Traitement"],
                  ["1", "Le formulaire reçoit l'élève, le montant, la date et le mode."],
                  ["2", "PaiementService valide le montant positif, le mode autorisé et le solde."],
                  ["3", "Paiement et contenu du reçu sont écrits en transaction SQLite."],
                  ["4", "RecuService génère le PDF correspondant."],
                  ["5", "L'interface actualise la liste et l'historique."],
              ], [2.0 * cm, 14.2 * cm]),
              Spacer(1, 7), para("Écran Élèves - recherche, filtres et statuts", "h2"),
              Image(str(ASSETS / "liste_eleves.png"), width=16.2 * cm, height=10.13 * cm),
              PageBreak()]

    story += [para("3. Modèle de données", "h1"),
              para("Le schéma de création complet est livré dans database/schema.sql. Les relations utilisent des clés étrangères; le solde est calculé à partir du total dû moins la somme des paiements."),
              DiagrammeMCD(),
              tableau([
                  ["Relation", "Cardinalité et règle"],
                  ["classes - eleves", "Une classe peut contenir plusieurs élèves; un élève référence une classe."],
                  ["annees_scolaires - eleves", "Une année regroupe plusieurs fiches; chaque élève référence une année."],
                  ["eleves - paiements", "Un élève peut avoir zéro à plusieurs paiements."],
                  ["paiements - recus", "Chaque paiement utilise un reçu unique; le reçu conserve les valeurs au moment de l'encaissement."],
                  ["parametres", "Table indépendante de configuration clé-valeur."],
              ], [4.3 * cm, 11.9 * cm]),
              Spacer(1, 6),
              para("La base impose des montants dus non négatifs, des paiements strictement positifs, des modes limités à Espèces, Chèque, Virement ou Mobile Money, et l'unicité du numéro de reçu. Les référentiels de classe et d'année évitent la répétition des libellés dans chaque fiche."),
              PageBreak()]

    story += [para("4. Choix techniques, limites et suite", "h1"),
              tableau([
                  ["Choix", "Justification"],
                  ["PySide6", "Interface de bureau native, formulaires et tableaux sans serveur Web."],
                  ["SQLite", "Base locale embarquée adaptée à un usage monoposte et simple à sauvegarder."],
                  ["FPDF2", "Création de reçus PDF A5 avec les données figées du paiement."],
                  ["PyInstaller ou Nuitka", "Empaquetage autonome; l'ordinateur cible n'a pas besoin de Python."],
              ], [4.0 * cm, 12.2 * cm]),
              para("Limites connues", "h2"),
              para("• Pas de comptes, rôles ou journal d'audit.<br/>• Pas de synchronisation multi-poste; chaque ordinateur a sa propre base locale.<br/>• Les frais sont saisis par élève et ne sont pas calculés automatiquement par classe.<br/>• Les sauvegardes doivent être déclenchées manuellement et stockées sur un autre support.<br/>• Les reçus utilisent une identité générique EduPaie; les coordonnées et le logo de l'école ne sont pas configurables."),
              para("Fiche élève et historique chronologique", "h2"),
              Image(str(ASSETS / "fiche_eleve.png"), width=16.2 * cm, height=10.13 * cm),
              para("Les données présentes sur cette capture sont fictives. Le jeu de démonstration comprend 15 élèves (5 non payés, 5 partiellement payés, 5 soldés) et 15 paiements associés.", "small"),
              para("La version autonome de test du 6 octobre 2026 précède les dernières fonctions de sauvegarde/restauration présentes dans les sources.", "small")]
    doc.build(story, onFirstPage=pied_de_page, onLaterPages=pied_de_page)
    return chemin


def manuel():
    chemin = SORTIE / "Manuel_utilisateur.pdf"
    doc = SimpleDocTemplate(
        str(chemin), pagesize=A4, rightMargin=2.0 * cm, leftMargin=2.0 * cm,
        topMargin=1.8 * cm, bottomMargin=1.65 * cm,
        title="Manuel utilisateur EduPaie", author="Projet EduPaie",
    )
    story = [
        para("EDUPAIE", "title"),
        para("Manuel utilisateur | Ajouter un élève, encaisser et imprimer", "subtitle"),
        para("1. Ajouter un élève", "h1"),
        para("Dans <b>Élèves</b>, cliquez sur <b>Ajouter un élève</b>. Renseignez le nom, le prénom, la classe, l'année scolaire et le total des frais dus, puis cliquez sur <b>Enregistrer</b>. Les champs marqués d'un astérisque sont obligatoires."),
        para("2. Enregistrer un paiement", "h1"),
        para("Sélectionnez l'élève dans la liste et cliquez sur <b>Encaisser un paiement</b>. Saisissez le montant, la date et le mode (espèces, chèque, virement ou Mobile Money). Le montant doit être positif et ne peut dépasser le solde restant. Cliquez sur <b>Enregistrer</b> pour créer le paiement et son reçu."),
        tableau([
            ["Statut", "Signification"],
            ["Non payé", "Aucun paiement enregistré."],
            ["Partiellement payé", "Le total payé est inférieur aux frais dus."],
            ["Soldé", "Le solde restant est nul."],
        ], [4.0 * cm, 12.0 * cm]),
        para("3. Ouvrir ou réimprimer le reçu", "h1"),
        para("Double-cliquez sur l'élève pour afficher sa fiche et l'historique chronologique. Sélectionnez le paiement concerné, puis cliquez sur <b>Réimprimer le reçu sélectionné</b>. Le bouton <b>Ouvrir le dernier reçu</b> affiche le reçu le plus récent. Le PDF est conservé dans le dossier des reçus d'EduPaie."),
        para("4. Sauvegarder les données", "h1"),
        para("Ouvrez <b>Paramètres</b> et cliquez sur <b>Créer une sauvegarde</b>. Enregistrez le ZIP dans Documents ou sur une clé USB. Pour restaurer, choisissez <b>Restaurer une sauvegarde</b>, sélectionnez le ZIP puis confirmez : les données actuelles seront remplacées par celles de l'archive."),
        para("Données locales : %LOCALAPPDATA%\\EduPaie\\. Ne déplacez pas la base pendant que l'application est ouverte.", "small"),
        Spacer(1, 8),
        Image(str(ASSETS / "liste_eleves.png"), width=16.0 * cm, height=10.0 * cm),
        para("Liste et statuts des élèves | Les données d'exemple sont fictives.", "small"),
    ]
    doc.build(story, onFirstPage=pied_de_page, onLaterPages=pied_de_page)
    return chemin


if __name__ == "__main__":
    print(technique())
    print(manuel())
