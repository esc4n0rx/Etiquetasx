from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ModernButton(QPushButton):
    """Botão moderno com estilos personalizados"""
    
    def __init__(self, text, style_type="primary", parent=None):
        super().__init__(text, parent)
        self.style_type = style_type
        self.setMinimumHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        self.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.apply_style()
    
    def apply_style(self):
        """Aplica estilo baseado no tipo"""
        styles = {
            "primary": {
                "background": "#3498db",
                "hover": "#2980b9",
                "pressed": "#21618c",
                "text": "white"
            },
            "success": {
                "background": "#27ae60",
                "hover": "#229954",
                "pressed": "#1e8449",
                "text": "white"
            },
            "warning": {
                "background": "#f39c12",
                "hover": "#e67e22",
                "pressed": "#d35400",
                "text": "white"
            },
            "danger": {
                "background": "#e74c3c",
                "hover": "#c0392b",
                "pressed": "#a93226",
                "text": "white"
            },
            "secondary": {
                "background": "#95a5a6",
                "hover": "#7f8c8d",
                "pressed": "#6c7b7d",
                "text": "white"
            }
        }
        
        style = styles.get(self.style_type, styles["primary"])
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {style['background']};
                color: {style['text']};
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {style['hover']};
                transform: translateY(-1px);
            }}
            QPushButton:pressed {{
                background-color: {style['pressed']};
                transform: translateY(1px);
            }}
            QPushButton:disabled {{
                background-color: #bdc3c7;
                color: #7f8c8d;
            }}
        """)

class ModernGroupBox(QGroupBox):
    """GroupBox moderno com estilo personalizado"""
    
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.apply_style()
    
    def apply_style(self):
        """Aplica estilo moderno ao GroupBox"""
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 12px;
                margin-top: 1ex;
                padding: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                background-color: white;
                color: #34495e;
            }
        """)

class ModernLineEdit(QLineEdit):
    """Campo de texto moderno"""
    
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        if placeholder:
            self.setPlaceholderText(placeholder)
        self.setMinimumHeight(35)
        self.apply_style()
    
    def apply_style(self):
        """Aplica estilo moderno"""
        self.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                font-size: 12px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background-color: white;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
            QLineEdit:hover {
                border-color: #85929e;
            }
        """)

class ModernComboBox(QComboBox):
    """ComboBox moderno"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(35)
        self.apply_style()
    
    def apply_style(self):
        """Aplica estilo moderno"""
        self.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                font-size: 12px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background-color: white;
                color: #2c3e50;
                selection-background-color: #3498db;
            }
            QComboBox:focus {
                border-color: #3498db;
            }
            QComboBox:hover {
                border-color: #85929e;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7f8c8d;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
                selection-background-color: #3498db;
                selection-color: white;
            }
        """)

class ModernSpinBox(QSpinBox):
    """SpinBox moderno"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(35)
        self.apply_style()
    
    def apply_style(self):
        """Aplica estilo moderno"""
        self.setStyleSheet("""
            QSpinBox {
                padding: 8px 12px;
                font-size: 12px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background-color: white;
                color: #2c3e50;
            }
            QSpinBox:focus {
                border-color: #3498db;
            }
            QSpinBox:hover {
                border-color: #85929e;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                border: none;
                background-color: #ecf0f1;
                width: 20px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #d5dbdb;
            }
        """)

class ModernCheckBox(QCheckBox):
    """CheckBox moderno"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.apply_style()
    
    def apply_style(self):
        """Aplica estilo moderno"""
        self.setStyleSheet("""
            QCheckBox {
                font-size: 12px;
                color: #2c3e50;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QCheckBox::indicator:hover {
                border-color: #3498db;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db;
                border-color: #3498db;
                image: none;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #2980b9;
            }
        """)

class ModernTextEdit(QTextEdit):
    """TextEdit moderno"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.apply_style()
    
    def apply_style(self):
        """Aplica estilo moderno"""
        self.setStyleSheet("""
            QTextEdit {
                padding: 12px;
                font-size: 12px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background-color: white;
                color: #2c3e50;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QTextEdit:focus {
                border-color: #3498db;
            }
            QTextEdit:hover {
                border-color: #85929e;
            }
        """)

class ModernTableWidget(QTableWidget):
    """TableWidget moderno"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.apply_style()
        self.setup_table()
    
    def apply_style(self):
        """Aplica estilo moderno"""
        self.setStyleSheet("""
            QTableWidget {
                gridline-color: #e8e8e8;
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e8e8e8;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QTableWidget::item:hover {
                background-color: #ebf3fd;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }
            QHeaderView::section:hover {
                background-color: #2c3e50;
            }
        """)
    
    def setup_table(self):
        """Configurações básicas da tabela"""
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSortingEnabled(True)
        self.verticalHeader().setVisible(False)

class ModernSlider(QSlider):
    """Slider moderno"""
    
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.apply_style()
    
    def apply_style(self):
        """Aplica estilo moderno"""
        self.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #bdc3c7;
                height: 6px;
                background: #ecf0f1;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                border: 2px solid #2980b9;
                width: 18px;
                height: 18px;
                margin: -7px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #5dade2;
                border-color: #3498db;
            }
            QSlider::handle:horizontal:pressed {
                background: #2980b9;
            }
            QSlider::sub-page:horizontal {
                background: #3498db;
                border: 1px solid #2980b9;
                height: 6px;
                border-radius: 3px;
            }
        """)

class StatusLabel(QLabel):
    """Label para status com cores automáticas"""
    
    def __init__(self, text="", status_type="info", parent=None):
        super().__init__(text, parent)
        self.status_type = status_type
        self.apply_style()
    
    def set_status(self, text, status_type="info"):
        """Define o status e aplica cor correspondente"""
        self.setText(text)
        self.status_type = status_type
        self.apply_style()
    
    def apply_style(self):
        """Aplica estilo baseado no tipo de status"""
        colors = {
            "success": "#27ae60",
            "error": "#e74c3c",
            "warning": "#f39c12",
            "info": "#3498db",
            "secondary": "#7f8c8d"
        }
        
        color = colors.get(self.status_type, colors["info"])
        
        self.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-weight: bold;
                font-size: 12px;
                padding: 5px;
            }}
        """)