from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime, timedelta

from ..components.modern_widgets import ModernButton, ModernGroupBox
from ..components.etiqueta_preview import EtiquetaPreview
from core.material_detector import MaterialDetector
from core.zpl_generator import ZPLGenerator
from core.printer_manager import PrinterManager

class ImpressaoTab(QWidget):
    def __init__(self, db_manager, settings_manager):
        super().__init__()
        self.db_manager = db_manager
        self.settings_manager = settings_manager
        
        # Componentes principais
        self.material_detector = MaterialDetector(db_manager)
        self.zpl_generator = ZPLGenerator(settings_manager)
        self.printer_manager = PrinterManager(settings_manager)
        
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Configura a interface da aba"""
        layout = QHBoxLayout(self)
        
        # Splitter principal
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Área de entrada (esquerda)
        self.create_input_area(splitter)
        
        # Área de preview (direita)
        self.create_preview_area(splitter)
        
        splitter.setSizes([600, 500])
    
    def create_input_area(self, parent):
        """Cria área de entrada de dados"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        
        # Grupo principal de entrada
        grupo_entrada = ModernGroupBox("📋 Dados do Material")
        form_layout = QFormLayout(grupo_entrada)
        
        # Campo código (sempre visível)
        self.codigo_input = QLineEdit()
        self.codigo_input.setPlaceholderText("Digite o código do material...")
        self.codigo_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                font-size: 14px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        form_layout.addRow("Código:", self.codigo_input)
        
        # Botão buscar
        self.btn_buscar = ModernButton("🔍 Buscar Material", "primary")
        self.btn_buscar.clicked.connect(self.buscar_material)
        form_layout.addRow(self.btn_buscar)
        
        # Área de informações do material
        self.info_widget = QWidget()
        self.info_layout = QVBoxLayout(self.info_widget)
        self.info_widget.hide()  # Oculto inicialmente
        
        # Labels de informação
        self.descricao_label = QLabel()
        self.descricao_label.setWordWrap(True)
        self.descricao_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 14px;")
        
        self.tipo_label = QLabel()
        self.tipo_label.setStyleSheet("font-weight: bold; color: #8e44ad; font-size: 12px;")
        
        self.validade_label = QLabel()
        self.validade_label.setStyleSheet("font-weight: bold; color: #27ae60; font-size: 12px;")
        
        self.info_layout.addWidget(QLabel("Descrição:"))
        self.info_layout.addWidget(self.descricao_label)
        self.info_layout.addWidget(self.tipo_label)
        self.info_layout.addWidget(self.validade_label)
        
        layout.addWidget(grupo_entrada)
        layout.addWidget(self.info_widget)
        
        # Grupo de campos específicos para sopas (oculto inicialmente)
        self.grupo_sopa = ModernGroupBox("🍲 Dados Específicos - Sopa")
        self.grupo_sopa.hide()
        form_sopa = QFormLayout(self.grupo_sopa)
        
        # Campo Caldeirão
        self.caldeira_input = QLineEdit()
        self.caldeira_input.setPlaceholderText("Ex: 01, 02, 03...")
        form_sopa.addRow("Caldeirão:", self.caldeira_input)
        
        # Campo Turno
        self.turno_combo = QComboBox()
        self.turno_combo.addItems(["M - Manhã", "T - Tarde", "N - Noite"])
        form_sopa.addRow("Turno:", self.turno_combo)
        
        # Campo Lote
        self.lote_input = QLineEdit()
        self.lote_input.setPlaceholderText("Ex: 001, 002, 003...")
        form_sopa.addRow("Lote:", self.lote_input)
        
        # Label do código gerado
        self.codigo_gerado_label = QLabel()
        self.codigo_gerado_label.setStyleSheet("font-weight: bold; color: #3498db; font-size: 12px;")
        form_sopa.addRow("Código Gerado:", self.codigo_gerado_label)
        
        layout.addWidget(self.grupo_sopa)
        
        # Botões de ação
        self.create_action_buttons(layout)
        
        layout.addStretch()
        scroll_area.setWidget(content)
        parent.addWidget(scroll_area)
    
    def create_action_buttons(self, layout):
        """Cria botões de ação"""
        btn_layout = QVBoxLayout()
        
        self.btn_imprimir = ModernButton("🖨️ Imprimir Etiqueta", "success")
        self.btn_imprimir.clicked.connect(self.imprimir_etiqueta)
        self.btn_imprimir.setEnabled(False)
        
        self.btn_preview = ModernButton("👁️ Atualizar Preview", "secondary")
        self.btn_preview.clicked.connect(self.atualizar_preview)
        self.btn_preview.setEnabled(False)
        
        btn_layout.addWidget(self.btn_imprimir)
        btn_layout.addWidget(self.btn_preview)
        
        layout.addLayout(btn_layout)
    
    def create_preview_area(self, parent):
        """Cria área de preview"""
        preview_widget = QWidget()
        layout = QVBoxLayout(preview_widget)
        
        grupo_preview = ModernGroupBox("👁️ Preview da Etiqueta")
        preview_layout = QVBoxLayout(grupo_preview)
        
        self.preview = EtiquetaPreview()
        preview_layout.addWidget(self.preview, 0, Qt.AlignCenter)
        
        layout.addWidget(grupo_preview)
        parent.addWidget(preview_widget)
    
    def connect_signals(self):
        """Conecta sinais"""
        self.codigo_input.returnPressed.connect(self.buscar_material)
        self.codigo_input.textChanged.connect(self.on_codigo_changed)
        
        # Sinais para campos de sopa
        self.caldeira_input.textChanged.connect(self.gerar_codigo_sopa)
        self.turno_combo.currentTextChanged.connect(self.gerar_codigo_sopa)
        self.lote_input.textChanged.connect(self.gerar_codigo_sopa)
    
    def on_codigo_changed(self):
        """Quando o código muda, limpa a interface"""
        self.limpar_interface()
    
    def limpar_interface(self):
        """Limpa a interface"""
        self.info_widget.hide()
        self.grupo_sopa.hide()
        self.btn_imprimir.setEnabled(False)
        self.btn_preview.setEnabled(False)
        self.preview.limpar()
    
    def buscar_material(self):
        """Busca material e detecta tipo automaticamente"""
        codigo = self.codigo_input.text().strip()
        if not codigo:
            QMessageBox.warning(self, "Aviso", "Digite um código de material!")
            return
        
        try:
            # Buscar material no banco
            material_info = self.material_detector.detectar_material(codigo)
            
            if not material_info:
                QMessageBox.warning(self, "Material não encontrado", 
                                  f"O material '{codigo}' não foi encontrado no banco de dados.")
                return
            
            # Mostrar informações básicas
            self.mostrar_info_material(material_info)
            
            # Configurar interface baseada no tipo
            if material_info['tipo'] == 'sopa':
                self.configurar_interface_sopa(material_info)
            else:
                self.configurar_interface_normal(material_info)
            
            # Atualizar preview inicial
            self.atualizar_preview()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao buscar material: {str(e)}")
    
    def mostrar_info_material(self, material_info):
        """Mostra informações do material"""
        self.material_info = material_info
        
        self.descricao_label.setText(material_info['descricao'])
        self.tipo_label.setText(f"Tipo: {material_info['tipo'].upper()}")
        self.validade_label.setText(f"Validade: {material_info['data_validade']}")
        
        self.info_widget.show()
        self.btn_preview.setEnabled(True)
        self.btn_imprimir.setEnabled(True)
    
    def configurar_interface_sopa(self, material_info):
        """Configura interface para sopas"""
        self.grupo_sopa.show()
        
        # Limpar campos
        self.caldeira_input.clear()
        self.lote_input.clear()
        self.turno_combo.setCurrentIndex(0)
        
        # Focar no primeiro campo
        self.caldeira_input.setFocus()
    
    def configurar_interface_normal(self, material_info):
        """Configura interface para materiais normais"""
        self.grupo_sopa.hide()
    
    def gerar_codigo_sopa(self):
        """Gera código automático para sopas"""
        if not hasattr(self, 'material_info') or self.material_info['tipo'] != 'sopa':
            return
        
        caldeira = self.caldeira_input.text().strip().zfill(2)  # Pad com zeros
        turno = self.turno_combo.currentText()[0]  # Primeira letra (M, T, N)
        lote = self.lote_input.text().strip().zfill(3)  # Pad com zeros
        
        if caldeira and lote:
            codigo_gerado = f"{caldeira}{turno}{lote}"
            self.codigo_gerado_label.setText(codigo_gerado)
            
            # Atualizar preview se todos os campos estão preenchidos
            if len(caldeira) >= 2 and len(lote) >= 3:
                self.atualizar_preview()
    
    def atualizar_preview(self):
        """Atualiza o preview da etiqueta"""
        if not hasattr(self, 'material_info'):
            return
        
        try:
            if self.material_info['tipo'] == 'sopa':
                # Validar campos obrigatórios para sopa
                if not self.caldeira_input.text().strip() or not self.lote_input.text().strip():
                    self.preview.mostrar_erro("Preencha caldeirão e lote")
                    return
                
                # Dados da sopa
                dados_preview = {
                    'codigo': self.codigo_input.text(),
                    'descricao': self.material_info['descricao'],
                    'validade': self.material_info['data_validade'],
                    'tipo': 'sopa',
                    'codigo_sopa': self.codigo_gerado_label.text(),
                    'conservacao': "Conservacao: -10 A -18\nou mais frio.\nValidade apos descongelamento: 5 dias"
                }
            else:
                # Dados normais
                dados_preview = {
                    'codigo': self.codigo_input.text(),
                    'descricao': self.material_info['descricao'],
                    'validade': self.material_info['data_validade'],
                    'tipo': 'normal'
                }
            
            self.preview.atualizar_dados(dados_preview)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar preview: {str(e)}")
    
    def imprimir_etiqueta(self):
        """Imprime a etiqueta"""
        if not hasattr(self, 'material_info'):
            return
        
        try:
            # Validar dados antes de imprimir
            if self.material_info['tipo'] == 'sopa':
                if not self.caldeira_input.text().strip() or not self.lote_input.text().strip():
                    QMessageBox.warning(self, "Aviso", "Preencha todos os campos obrigatórios!")
                    return
                
                # Dados para impressão de sopa
                dados_impressao = {
                    'codigo': self.codigo_input.text(),
                    'descricao': self.material_info['descricao'],
                    'validade': self.material_info['data_validade'],
                    'tipo': 'sopa',
                    'codigo_sopa': self.codigo_gerado_label.text(),
                    'conservacao': "Conservação: -10° À -18°\nou mais frio.\nValidade após descongelamento: 5 dias"
                }
            else:
                # Dados para impressão normal
                dados_impressao = {
                    'codigo': self.codigo_input.text(),
                    'descricao': self.material_info['descricao'],
                    'validade': self.material_info['data_validade'],
                    'tipo': 'normal'
                }
            
            # Gerar ZPL
            zpl_code = self.zpl_generator.gerar_zpl(dados_impressao)
            
            # Imprimir
            if self.printer_manager.imprimir(zpl_code):
                QMessageBox.information(self, "Sucesso", "Etiqueta enviada para impressão!")
                self.limpar_campos_apos_impressao()
            else:
                QMessageBox.warning(self, "Erro", "Falha ao enviar para impressora!")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao imprimir: {str(e)}")
    
    def limpar_campos_apos_impressao(self):
        """Limpa campos após impressão bem-sucedida"""
        if hasattr(self, 'material_info') and self.material_info['tipo'] == 'sopa':
            # Para sopas, limpa apenas os campos específicos
            self.caldeira_input.clear()
            self.lote_input.clear()
            self.codigo_gerado_label.clear()
            self.caldeira_input.setFocus()
        else:
            # Para normais, limpa tudo
            self.codigo_input.clear()
            self.limpar_interface()
            self.codigo_input.setFocus()
    
    def atualizar_configuracoes_preview(self):
        """Atualiza configurações do preview"""
        self.atualizar_preview()