"""
Qt StyleSheet definitions for modern green theme
"""
from utils.constants import COLORS


def get_stylesheet() -> str:
    """
    Get the main application stylesheet
    
    Returns:
        Qt stylesheet string
    """
    return f"""
    /* Main Window */
    QMainWindow {{
        background-color: {COLORS['background']};
    }}
    
    /* Sidebar */
    QListWidget {{
        background-color: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 8px;
        font-size: 14px;
    }}
    
    QListWidget::item {{
        padding: 12px;
        border-radius: 6px;
        margin: 4px 0px;
    }}
    
    QListWidget::item:selected {{
        background-color: {COLORS['primary']};
        color: white;
    }}
    
    QListWidget::item:hover {{
        background-color: {COLORS['primary_light']};
    }}
    
    /* Buttons */
    QPushButton {{
        background-color: {COLORS['primary']};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: bold;
    }}
    
    QPushButton:hover {{
        background-color: {COLORS['primary_dark']};
    }}
    
    QPushButton:pressed {{
        background-color: {COLORS['accent']};
    }}
    
    /* Input Fields */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: white;
        border: 2px solid {COLORS['border']};
        border-radius: 6px;
        padding: 8px;
        font-size: 13px;
    }}
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border-color: {COLORS['primary']};
    }}
    
    /* ComboBox */
    QComboBox {{
        background-color: white;
        border: 2px solid {COLORS['border']};
        border-radius: 6px;
        padding: 8px;
        font-size: 13px;
    }}
    
    QComboBox:hover {{
        border-color: {COLORS['primary']};
    }}
    
    QComboBox::drop-down {{
        border: none;
    }}
    
    /* Labels */
    QLabel {{
        color: {COLORS['text']};
        font-size: 13px;
    }}
    
    /* Group Boxes */
    QGroupBox {{
        background-color: {COLORS['surface']};
        border: 2px solid {COLORS['border']};
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 12px;
        font-weight: bold;
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 4px 8px;
        color: {COLORS['primary']};
    }}
    
    /* Scroll Bars */
    QScrollBar:vertical {{
        background-color: {COLORS['background']};
        width: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {COLORS['primary_light']};
        border-radius: 6px;
        min-height: 20px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {COLORS['primary']};
    }}
    
    /* Menu Bar */
    QMenuBar {{
        background-color: {COLORS['surface']};
        border-bottom: 1px solid {COLORS['border']};
    }}
    
    QMenuBar::item {{
        padding: 8px 12px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {COLORS['primary_light']};
    }}
    
    QMenu {{
        background-color: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
    }}
    
    QMenu::item {{
        padding: 8px 24px;
    }}
    
    QMenu::item:selected {{
        background-color: {COLORS['primary_light']};
    }}
    """
