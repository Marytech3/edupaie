"""EduPaie palette and shared Qt style sheet (QSS)."""


STYLE_SHEET = r"""
QWidget {
    color: #28232b;
    font-family: "Segoe UI";
    font-size: 10pt;
}

QMainWindow, QWidget#mainArea, QWidget#page {
    background-color: #f7f8fa;
}

QWidget#sidebar {
    background-color: #285b8f;
    min-width: 210px;
    max-width: 210px;
}

QLabel#brandTitle {
    color: #ffffff;
    font-size: 21pt;
    font-weight: 700;
}

QLabel#brandSubtitle, QLabel#sidebarFooter {
    color: #d7e5f3;
    font-size: 9pt;
}

QPushButton#navButton {
    color: #eef5fc;
    background: transparent;
    border: 0;
    border-left: 3px solid transparent;
    border-radius: 0;
    text-align: left;
    padding: 11px 15px;
    min-height: 22px;
}

QPushButton#navButton:hover {
    background-color: #346a9f;
}

QPushButton#navButton:checked {
    color: #ffffff;
    background-color: #1e456d;
    border-left: 3px solid #70b7f4;
    font-weight: 600;
}

QLabel#pageTitle {
    color: #302637;
    font-size: 18pt;
    font-weight: 650;
}

QLabel#pageSubtitle, QLabel#mutedText {
    color: #817783;
    font-size: 9pt;
}

QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
    background-color: #ffffff;
    color: #28232b;
    border: 1px solid #d9dce2;
    border-radius: 4px;
    padding: 7px 10px;
    min-height: 22px;
    selection-background-color: #2e6fae;
}

QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDoubleSpinBox:focus {
    border: 1px solid #337fbd;
}

QComboBox::drop-down, QDateEdit::drop-down {
    border: 0;
    width: 24px;
}

QPushButton {
    color: #405266;
    background-color: #ffffff;
    border: 1px solid #d9dce2;
    border-radius: 4px;
    padding: 7px 12px;
    min-height: 20px;
}

QPushButton:hover {
    background-color: #eef4fa;
    border-color: #b8c8d8;
}

QPushButton:pressed {
    background-color: #e0eaf4;
}

QPushButton#primaryButton {
    color: #ffffff;
    background-color: #2e6fae;
    border: 1px solid #2e6fae;
    font-weight: 600;
}

QPushButton#primaryButton:hover {
    background-color: #245a91;
    border-color: #245a91;
}

QPushButton#backButton {
    color: #337fbd;
    background: transparent;
    border: 0;
    padding: 3px 0;
    text-align: left;
}

QPushButton#backButton:hover {
    color: #245a91;
    background: transparent;
    border: 0;
}

QPushButton:disabled {
    color: #a8a2ab;
    background-color: #f0f1f3;
    border-color: #e2e4e8;
}

QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #fbfbfc;
    color: #302a33;
    border: 1px solid #eceef1;
    border-radius: 4px;
    gridline-color: #edf0f3;
    selection-background-color: #e5effa;
    selection-color: #20364d;
    outline: 0;
}

QTableWidget::item {
    padding: 7px 8px;
    border-bottom: 1px solid #edf0f3;
}

QHeaderView::section {
    color: #52667b;
    background-color: #ffffff;
    border: 0;
    border-bottom: 2px solid #dfe3e7;
    padding: 9px 8px;
    font-weight: 600;
}

QGroupBox {
    background-color: #ffffff;
    border: 1px solid #e2e8ef;
    border-radius: 6px;
    margin-top: 10px;
    padding: 12px 10px 10px 10px;
    color: #52677d;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 4px;
}

QFrame#metricCard {
    background-color: #ffffff;
    border: 1px solid #dbe2ea;
    border-top: 3px solid #2e6fae;
    border-radius: 5px;
}

QFrame#backupCard {
    background-color: #ffffff;
    border: 1px solid #dbe2ea;
    border-radius: 6px;
}

QLabel#metricLabel {
    color: #52677d;
    font-size: 8pt;
}

QLabel#metricDue, QLabel#metricBalance {
    color: #315b8a;
    font-size: 15pt;
    font-weight: 700;
}

QLabel#metricPaid {
    color: #16803d;
    font-size: 15pt;
    font-weight: 700;
}

QLabel#sectionTitle {
    color: #52677d;
    font-size: 10pt;
    font-weight: 600;
}

QDialog {
    background-color: #f7f8fa;
}

QScrollBar:vertical {
    background: #f7f8fa;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #c9c2cb;
    border-radius: 4px;
    min-height: 24px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""
