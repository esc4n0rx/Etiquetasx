from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ..components.modern_widgets import ModernGroupBox

class SobreTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface"""
        layout = QVBoxLayout(self)
        
        grupo_sobre = ModernGroupBox("Sobre o Sistema")
        sobre_layout = QVBoxLayout(grupo_sobre)
        
        info_text = QLabel("""
        <h2 style="color: #2c3e50;">Sistema de Etiquetas v2.1</h2>
        <p><strong>🎯 Desenvolvido para:</strong> Impressão inteligente de etiquetas com detecção automática</p>
        
        <h3 style="color: #34495e;">✨ Novos Recursos v2.1:</h3>
        <ul>
            <li>🧠 <strong>Detecção Automática:</strong> Sistema identifica se é sopa ou material normal</li>
            <li>🍲 <strong>Gestão de Sopas:</strong> Campos automáticos para caldeirão, turno e lote</li>
            <li>🎯 <strong>Código Inteligente:</strong> Geração automática de códigos para sopas</li>
            <li>❄️ <strong>Informações de Conservação:</strong> Automáticas para sopas</li>
            <li>📊 <strong>Sopas Especiais:</strong> Validade estendida (90 dias) para sopas especiais</li>
            <li>🔧 <strong>Código Modular:</strong> Melhor organização e manutenção</li>
        </ul>
        
        <h3 style="color: #34495e;">🛠️ Recursos Existentes:</h3>
        <ul>
            <li>✅ Interface moderna e intuitiva</li>
            <li>✅ Preview em tempo real das etiquetas</li>
            <li>✅ Configurações visuais avançadas</li>
            <li>✅ Importação/Exportação de planilhas Excel</li>
            <li>✅ Banco de dados SQLite integrado</li>
            <li>✅ Configuração automática de impressora USB</li>
        </ul>
        
        <h3 style="color: #34495e;">🔧 Tecnologias:</h3>
        <ul>
            <li>Python 3.x + PyQt5</li>
            <li>SQLite para armazenamento</li>
            <li>Pandas para manipulação de dados</li>
            <li>ZPL (Zebra Programming Language)</li>
        </ul>
        
        <h3 style="color: #34495e;">📋 Como usar:</h3>
        <ol>
            <li><strong>Configurar:</strong> Configure sua impressora na aba "Configurações"</li>
            <li><strong>Cadastrar:</strong> Cadastre os materiais na aba "Cadastro"</li>
            <li><strong>Ajustar:</strong> Ajuste o layout das etiquetas conforme necessário</li>
            <li><strong>Imprimir:</strong> Digite o código na aba "Impressão" - o sistema detecta automaticamente o tipo!</li>
        </ol>
        
        <h3 style="color: #8e44ad;">🍲 Regras para Sopas:</h3>
        <ul>
            <li><strong>Detecção:</strong> Automática por categoria ou palavras-chave</li>
            <li><strong>Campos:</strong> Caldeirão + Turno (M/T/N) + Lote</li>
            <li><strong>Código:</strong> Gerado automaticamente (ex: 01M001)</li>
            <li><strong>Conservação:</strong> Informações automáticas de temperatura</li>
            <li><strong>Validade:</strong> Sopas especiais (SP=S) têm 90 dias em vez de 30</li>
        </ul>
        
        <p style="margin-top: 20px; color: #7f8c8d;"><em>🚀 Sistema otimizado para máxima eficiência e facilidade de uso!</em></p>
        """)
        
        info_text.setWordWrap(True)
        info_text.setStyleSheet("""
            QLabel {
                background-color: white;
                padding: 25px;
                border-radius: 12px;
                border: 1px solid #bdc3c7;
                line-height: 1.6;
            }
        """)
        
        sobre_layout.addWidget(info_text)
        layout.addWidget(grupo_sobre)