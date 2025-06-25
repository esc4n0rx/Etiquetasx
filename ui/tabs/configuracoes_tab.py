from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ..components.modern_widgets import ModernButton, ModernGroupBox
from ..components.etiqueta_preview import EtiquetaPreview
from core.printer_manager import PrinterManager

class ConfiguracoesTab(QWidget):
    configuracoes_alteradas = pyqtSignal()
    
    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager
        self.printer_manager = PrinterManager(settings_manager)
        self.setup_ui()
        self.carregar_configuracoes()
    
    def setup_ui(self):
        """Configura a interface"""
        layout = QHBoxLayout(self)
        
        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Área de configurações (esquerda)
        self.create_config_area(splitter)
        
        # Área de preview (direita)
        self.create_preview_area(splitter)
        
        splitter.setSizes([600, 400])
    
    def create_config_area(self, parent):
        """Cria área de configurações"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        
        # Grupo impressora
        grupo_impressora = ModernGroupBox("🖨️ Configurações da Impressora")
        form_impressora = QFormLayout(grupo_impressora)
        
        self.impressora_combo = QComboBox()
        self.impressora_combo.addItems(self.printer_manager.impressoras_disponiveis)
        self.impressora_combo.currentTextChanged.connect(self.salvar_impressora)
        form_impressora.addRow("Impressora:", self.impressora_combo)
        
        btn_testar = ModernButton("🧪 Testar Impressora", "warning")
        btn_testar.clicked.connect(self.testar_impressora)
        form_impressora.addRow(btn_testar)
        
        layout.addWidget(grupo_impressora)
        
        # Grupo layout
        grupo_layout = ModernGroupBox("🎨 Layout da Etiqueta")
        form_layout = QFormLayout(grupo_layout)
        
        # Sliders com valores
        self.create_slider_config(form_layout, "Fonte Título:", "fonte_titulo", 10, 30, 18)
        self.create_slider_config(form_layout, "Fonte Subtítulo:", "fonte_subtitulo", 8, 20, 14)
        self.create_slider_config(form_layout, "Fonte Texto:", "fonte_texto", 6, 16, 12)
        self.create_slider_config(form_layout, "Espaçamento:", "espacamento", 5, 50, 25)
        self.create_slider_config(form_layout, "Margem Horizontal:", "margem_x", 5, 50, 20)
        self.create_slider_config(form_layout, "Margem Vertical:", "margem_y", 5, 50, 20)
        
        # Checkbox centralizar
        self.centralizar_checkbox = QCheckBox("Centralizar conteúdo na etiqueta")
        self.centralizar_checkbox.setChecked(True)
        self.centralizar_checkbox.stateChanged.connect(self.on_config_changed)
        form_layout.addRow(self.centralizar_checkbox)
        
        layout.addWidget(grupo_layout)
        
        # Botões
        btn_layout = QHBoxLayout()
        
        btn_salvar = ModernButton("💾 Salvar Configurações", "success")
        btn_salvar.clicked.connect(self.salvar_configuracoes)
        
        btn_resetar = ModernButton("🔄 Resetar Padrões", "warning")
        btn_resetar.clicked.connect(self.resetar_configuracoes)
        
        btn_layout.addWidget(btn_salvar)
        btn_layout.addWidget(btn_resetar)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        scroll_area.setWidget(content)
        parent.addWidget(scroll_area)
    
    def create_slider_config(self, form_layout, label, attr_name, min_val, max_val, default_val):
        """Cria configuração com slider"""
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default_val)
        slider.valueChanged.connect(self.on_config_changed)
        
        value_label = QLabel(str(default_val))
        slider.valueChanged.connect(lambda v: value_label.setText(str(v)))
        
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(slider)
        slider_layout.addWidget(value_label)
        
        form_layout.addRow(label, slider_layout)
        
        # Armazenar referências
        setattr(self, f"{attr_name}_slider", slider)
        setattr(self, f"{attr_name}_label", value_label)
    
    def create_preview_area(self, parent):
        """Cria área de preview"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        grupo_preview = ModernGroupBox("👁️ Preview em Tempo Real")
        preview_layout = QVBoxLayout(grupo_preview)
        
        self.preview = EtiquetaPreview()
        preview_layout.addWidget(self.preview, 0, Qt.AlignCenter)
        
        # Botões de tipo de preview
        btn_layout = QHBoxLayout()
        
        btn_normal = ModernButton("Preview Normal", "secondary")
        btn_normal.clicked.connect(lambda: self.mudar_preview("normal"))
        
        btn_sopa = ModernButton("Preview Sopa", "secondary")
        btn_sopa.clicked.connect(lambda: self.mudar_preview("sopa"))
        
        btn_layout.addWidget(btn_normal)
        btn_layout.addWidget(btn_sopa)
        
        preview_layout.addLayout(btn_layout)
        layout.addWidget(grupo_preview)
        
        parent.addWidget(widget)
    
    def on_config_changed(self):
        """Quando configuração muda"""
        config = self.get_current_config()
        self.settings_manager.update_layout_config(config)
        self.preview.atualizar_configuracoes(config)
        self.configuracoes_alteradas.emit()
    
    def get_current_config(self):
        """Obtém configuração atual"""
        return {
            'fonte_titulo': self.fonte_titulo_slider.value(),
            'fonte_subtitulo': self.fonte_subtitulo_slider.value(),
            'fonte_texto': self.fonte_texto_slider.value(),
            'centralizar': self.centralizar_checkbox.isChecked(),
            'espacamento': self.espacamento_slider.value(),
            'margem_x': self.margem_x_slider.value(),
            'margem_y': self.margem_y_slider.value()
        }
    
    def carregar_configuracoes(self):
        """Carrega configurações salvas"""
        config = self.settings_manager.get_layout_config()
        
        self.fonte_titulo_slider.setValue(config['fonte_titulo'])
        self.fonte_subtitulo_slider.setValue(config['fonte_subtitulo'])
        self.fonte_texto_slider.setValue(config['fonte_texto'])
        self.centralizar_checkbox.setChecked(config['centralizar'])
        self.espacamento_slider.setValue(config['espacamento'])
        self.margem_x_slider.setValue(config['margem_x'])
        self.margem_y_slider.setValue(config['margem_y'])
        
        # Carregar impressora
        impressora_salva = self.settings_manager.get_printer_name()
        if impressora_salva:
            index = self.impressora_combo.findText(impressora_salva)
            if index >= 0:
                self.impressora_combo.setCurrentIndex(index)
        
        self.atualizar_preview_inicial()
    
    def atualizar_preview_inicial(self):
        """Atualiza preview inicial"""
        self.mudar_preview("normal")
    
    def mudar_preview(self, tipo):
        """Muda tipo de preview"""
        if tipo == "normal":
            dados = {
                'codigo': 'MAT001',
                'descricao': 'Arroz Branco Temperado com Legumes',
                'validade': '30/06/2025',
                'tipo': 'normal'
            }
        else:
            dados = {
                'codigo': 'SOP001',
                'descricao': 'Sopa de Legumes com Frango e Batata Doce',
                'validade': '28/06/2025',
                'tipo': 'sopa',
                'codigo_sopa': '01M001',
                'conservacao': 'Conservação: -10° À -18°\nou mais frio.\nValidade após descongelamento: 5 dias'
            }
        
        self.preview.atualizar_dados(dados)
    
    def salvar_configuracoes(self):
        """Salva todas as configurações"""
        config = self.get_current_config()
        self.settings_manager.save_settings(config)
        QMessageBox.information(self, "Sucesso", "Configurações salvas com sucesso!")
    
    def resetar_configuracoes(self):
        """Reseta configurações para padrão"""
        default_config = self.settings_manager.get_default_config()
        
        self.fonte_titulo_slider.setValue(default_config['fonte_titulo'])
        self.fonte_subtitulo_slider.setValue(default_config['fonte_subtitulo'])
        self.fonte_texto_slider.setValue(default_config['fonte_texto'])
        self.centralizar_checkbox.setChecked(default_config['centralizar'])
        self.espacamento_slider.setValue(default_config['espacamento'])
        self.margem_x_slider.setValue(default_config['margem_x'])
        self.margem_y_slider.setValue(default_config['margem_y'])
        
        QMessageBox.information(self, "Sucesso", "Configurações resetadas para os valores padrão!")
    
    def salvar_impressora(self):
        """Salva impressora selecionada"""
        impressora = self.impressora_combo.currentText()
        self.settings_manager.save_printer_name(impressora)
    
    def testar_impressora(self):
        """Testa a impressora"""
        impressora = self.impressora_combo.currentText()
        
        if not impressora or impressora == "Nenhuma impressora encontrada":
            QMessageBox.warning(self, "Aviso", "Selecione uma impressora válida!")
            return
        
        try:
            if self.printer_manager.testar_impressora(impressora):
                QMessageBox.information(self, "Sucesso", "Teste de impressão enviado!")
            else:
                QMessageBox.warning(self, "Erro", "Falha no teste de impressão!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao testar impressora: {str(e)}")