import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .components.modern_widgets import ModernButton, ModernGroupBox
from .tabs.impressao_tab import ImpressaoTab
from .tabs.cadastro_tab import CadastroTab
from .tabs.configuracoes_tab import ConfiguracoesTab
from .tabs.sobre_tab import SobreTab
from database.db_manager import DatabaseManager
from utils.settings_manager import SettingsManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Etiquetas v2.1")
        self.setGeometry(100, 100, 1400, 900)
        
        # Managers
        self.db_manager = DatabaseManager()
        self.settings_manager = SettingsManager()
        
        # Configurar estilo
        self.setStyleSheet(self.get_app_style())
        
        # Configurar interface
        self.setup_ui()
        
        # Carregar configurações
        self.settings_manager.load_settings()
    
    def setup_ui(self):
        """Configura a interface principal"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Abas
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #5dade2;
                color: white;
            }
        """)
        
        # Criar abas
        self.impressao_tab = ImpressaoTab(self.db_manager, self.settings_manager)
        self.cadastro_tab = CadastroTab(self.db_manager)
        self.configuracoes_tab = ConfiguracoesTab(self.settings_manager)
        self.sobre_tab = SobreTab()
        
        # Adicionar abas
        self.tab_widget.addTab(self.impressao_tab, "🖨️ Impressão")
        self.tab_widget.addTab(self.cadastro_tab, "📝 Cadastro")
        self.tab_widget.addTab(self.configuracoes_tab, "⚙️ Configurações")
        self.tab_widget.addTab(self.sobre_tab, "ℹ️ Sobre")
        
        layout.addWidget(self.tab_widget)
        
        # Conectar sinais
        self.connect_signals()
    
    def create_header(self):
        """Cria o cabeçalho da aplicação"""
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #3498db, stop:1 #2980b9);
                border-radius: 12px;
                padding: 20px;
            }
            QLabel {
                color: white;
                font-weight: bold;
                background: transparent;
            }
        """)
        
        layout = QHBoxLayout(header_widget)
        
        # Título
        title = QLabel("Sistema de Etiquetas")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        # Subtítulo
        subtitle = QLabel("Impressão inteligente com detecção automática de tipos")
        subtitle.setStyleSheet("font-size: 14px; opacity: 0.9;")
        
        # Layout do texto
        text_layout = QVBoxLayout()
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        
        return header_widget
    
    def connect_signals(self):
        """Conecta sinais entre componentes"""
        # Conectar configurações com preview
        self.configuracoes_tab.configuracoes_alteradas.connect(
            self.impressao_tab.atualizar_configuracoes_preview
        )
    
    def get_app_style(self):
        """Retorna o estilo da aplicação"""
        return """
            QMainWindow {
                background-color: #f8f9fa;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """
    
    def closeEvent(self, event):
        """Fecha a aplicação"""
        self.db_manager.close()
        event.accept()