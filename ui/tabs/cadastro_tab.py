from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd

from ..components.modern_widgets import ModernButton, ModernGroupBox

class CadastroTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        self.atualizar_tabela()
    
    def setup_ui(self):
        """Configura a interface"""
        layout = QHBoxLayout(self)
        
        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Área de cadastro (esquerda)
        self.create_form_area(splitter)
        
        # Área de tabela (direita)
        self.create_table_area(splitter)
        
        splitter.setSizes([400, 800])
    
    def create_form_area(self, parent):
        """Cria área do formulário"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        
        # Grupo de cadastro
        grupo_cadastro = ModernGroupBox("📝 Cadastrar Material")
        form_layout = QFormLayout(grupo_cadastro)
        
        # Campos do formulário
        self.material_input = QLineEdit()
        self.material_input.setPlaceholderText("Ex: MAT001")
        form_layout.addRow("Código:", self.material_input)
        
        self.descricao_input = QLineEdit()
        self.descricao_input.setPlaceholderText("Ex: Arroz Branco Temperado")
        form_layout.addRow("Descrição:", self.descricao_input)
        
        self.dias_validade_input = QSpinBox()
        self.dias_validade_input.setRange(1, 365)
        self.dias_validade_input.setValue(30)
        form_layout.addRow("Dias Validade:", self.dias_validade_input)
        
        self.categoria_input = QComboBox()
        self.categoria_input.setEditable(True)
        self.categoria_input.addItems([
            "Alimento Normal",
            "Sopa",
            "Caldo",
            "Bebida",
            "Sobremesa",
            "Tempero",
            "Ingrediente"
        ])
        form_layout.addRow("Categoria:", self.categoria_input)
        
        # Novo campo: Sopa Especial
        self.sopa_especial_combo = QComboBox()
        self.sopa_especial_combo.addItems([
            "N - Normal",
            "S - Sopa Especial (90 dias)"
        ])
        form_layout.addRow("Tipo Especial:", self.sopa_especial_combo)
        
        # Explicação para sopa especial
        info_label = QLabel("ℹ️ Sopas especiais (S) dobram a validade de 30 para 90 dias")
        info_label.setStyleSheet("color: #7f8c8d; font-size: 11px; font-style: italic;")
        info_label.setWordWrap(True)
        form_layout.addRow(info_label)
        
        # Botões
        btn_layout = QHBoxLayout()
        
        btn_cadastrar = ModernButton("💾 Cadastrar", "success")
        btn_cadastrar.clicked.connect(self.cadastrar_material)
        
        btn_limpar = ModernButton("🧹 Limpar", "secondary")
        btn_limpar.clicked.connect(self.limpar_campos)
        
        btn_layout.addWidget(btn_cadastrar)
        btn_layout.addWidget(btn_limpar)
        
        form_layout.addRow(btn_layout)
        
        layout.addWidget(grupo_cadastro)
        
        # Grupo de importação/exportação
        grupo_io = ModernGroupBox("📊 Importar/Exportar")
        io_layout = QVBoxLayout(grupo_io)
        
        btn_importar = ModernButton("📥 Importar Excel", "primary")
        btn_importar.clicked.connect(self.importar_planilha)
        
        btn_exportar = ModernButton("📤 Exportar Excel", "secondary")
        btn_exportar.clicked.connect(self.exportar_planilha)
        
        btn_template = ModernButton("📋 Baixar Template", "warning")
        btn_template.clicked.connect(self.baixar_template)
        
        io_layout.addWidget(btn_importar)
        io_layout.addWidget(btn_exportar)
        io_layout.addWidget(btn_template)
        
        layout.addWidget(grupo_io)
        layout.addStretch()
        
        scroll_area.setWidget(content)
        parent.addWidget(scroll_area)
    
    def create_table_area(self, parent):
        """Cria área da tabela"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Cabeçalho da tabela
        header_layout = QHBoxLayout()
        
        title = QLabel("📋 Materiais Cadastrados")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        
        btn_atualizar = ModernButton("🔄 Atualizar", "secondary")
        btn_atualizar.clicked.connect(self.atualizar_tabela)
        
        btn_deletar = ModernButton("🗑️ Deletar", "danger")
        btn_deletar.clicked.connect(self.deletar_material)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(btn_atualizar)
        header_layout.addWidget(btn_deletar)
        
        layout.addLayout(header_layout)
        
        # Tabela
        self.tabela_materiais = QTableWidget()
        self.tabela_materiais.setColumnCount(6)
        self.tabela_materiais.setHorizontalHeaderLabels([
            "ID", "Código", "Descrição", "Validade (dias)", "Categoria", "Especial"
        ])
        
        # Configurar tabela
        header = self.tabela_materiais.horizontalHeader()
        header.setStretchLastSection(True)
        header.resizeSection(0, 50)   # ID
        header.resizeSection(1, 100)  # Código
        header.resizeSection(2, 300)  # Descrição
        header.resizeSection(3, 120)  # Validade
        header.resizeSection(4, 150)  # Categoria
        header.resizeSection(5, 80)   # Especial
        
        self.tabela_materiais.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_materiais.setAlternatingRowColors(True)
        
        layout.addWidget(self.tabela_materiais)
        parent.addWidget(widget)
    
    def cadastrar_material(self):
        """Cadastra novo material"""
        material = self.material_input.text().strip()
        descricao = self.descricao_input.text().strip()
        dias_validade = self.dias_validade_input.value()
        categoria = self.categoria_input.currentText().strip()
        sopa_especial = self.sopa_especial_combo.currentText()[0]  # S ou N
        
        if not material or not descricao or not categoria:
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos obrigatórios!")
            return
        
        try:
            self.db_manager.inserir_material(
                material, descricao, dias_validade, categoria, sopa_especial
            )
            
            QMessageBox.information(self, "Sucesso", "Material cadastrado com sucesso!")
            self.limpar_campos()
            self.atualizar_tabela()
            
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                QMessageBox.warning(self, "Erro", "Material já existe no banco de dados!")
            else:
                QMessageBox.critical(self, "Erro", f"Erro ao cadastrar material: {str(e)}")
    
    def limpar_campos(self):
        """Limpa os campos do formulário"""
        self.material_input.clear()
        self.descricao_input.clear()
        self.dias_validade_input.setValue(30)
        self.categoria_input.setCurrentIndex(0)
        self.sopa_especial_combo.setCurrentIndex(0)
        self.material_input.setFocus()
    
    def atualizar_tabela(self):
        """Atualiza a tabela de materiais"""
        try:
            dados = self.db_manager.listar_materiais()
            
            self.tabela_materiais.setRowCount(len(dados))
            
            for row, (id_material, material, descricao, dias_validade, categoria, sopa_especial) in enumerate(dados):
                self.tabela_materiais.setItem(row, 0, QTableWidgetItem(str(id_material)))
                self.tabela_materiais.setItem(row, 1, QTableWidgetItem(material))
                self.tabela_materiais.setItem(row, 2, QTableWidgetItem(descricao))
                self.tabela_materiais.setItem(row, 3, QTableWidgetItem(str(dias_validade)))
                self.tabela_materiais.setItem(row, 4, QTableWidgetItem(categoria))
                self.tabela_materiais.setItem(row, 5, QTableWidgetItem(sopa_especial))
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar materiais: {str(e)}")
    
    def deletar_material(self):
        """Deleta material selecionado"""
        row = self.tabela_materiais.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um material para deletar!")
            return
        
        id_material = int(self.tabela_materiais.item(row, 0).text())
        material = self.tabela_materiais.item(row, 1).text()
        
        resposta = QMessageBox.question(
            self, "Confirmar", 
            f"Deseja deletar o material '{material}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if resposta == QMessageBox.Yes:
            try:
                self.db_manager.deletar_material(id_material)
                QMessageBox.information(self, "Sucesso", "Material deletado com sucesso!")
                self.atualizar_tabela()
                
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao deletar material: {str(e)}")
    
    def importar_planilha(self):
        """Importa materiais de planilha Excel"""
        arquivo, _ = QFileDialog.getOpenFileName(
            self, "Importar Planilha", "", 
            "Excel Files (*.xlsx *.xls)"
        )
        
        if not arquivo:
            return
        
        try:
            df = pd.read_excel(arquivo)
            
            # Verificar colunas necessárias
            colunas_necessarias = ['material', 'descricao', 'dias_validade', 'categoria']
            if not all(col in df.columns for col in colunas_necessarias):
                QMessageBox.warning(
                    self, "Erro", 
                    f"A planilha deve ter as colunas: {', '.join(colunas_necessarias)}\n"
                    f"Opcionalmente: sopa_especial"
                )
                return
            
            importados = 0
            erros = 0
            
            for _, row in df.iterrows():
                try:
                    sopa_especial = 'N'
                    if 'sopa_especial' in df.columns:
                        sopa_especial = str(row['sopa_especial']).upper()
                        if sopa_especial not in ['S', 'N']:
                            sopa_especial = 'N'
                    
                    self.db_manager.inserir_material(
                        str(row['material']), 
                        str(row['descricao']), 
                        int(row['dias_validade']), 
                        str(row['categoria']),
                        sopa_especial
                    )
                    importados += 1
                except:
                    erros += 1
            
            QMessageBox.information(
                self, "Importação Concluída", 
                f"Importados: {importados}\nErros: {erros}"
            )
            
            self.atualizar_tabela()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao importar planilha: {str(e)}")
    
    def exportar_planilha(self):
        """Exporta dados para planilha"""
        arquivo, _ = QFileDialog.getSaveFileName(
            self, "Exportar Planilha", "materiais.xlsx", 
            "Excel Files (*.xlsx)"
        )
        
        if not arquivo:
            return
        
        try:
            dados = self.db_manager.listar_materiais()
            
            df = pd.DataFrame(dados, columns=[
                'id', 'material', 'descricao', 'dias_validade', 'categoria', 'sopa_especial'
            ])
            
            # Remover coluna ID para exportação
            df = df.drop('id', axis=1)
            
            df.to_excel(arquivo, index=False)
            QMessageBox.information(self, "Sucesso", "Planilha exportada com sucesso!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exportar planilha: {str(e)}")
    
    def baixar_template(self):
        """Cria template de exemplo"""
        arquivo, _ = QFileDialog.getSaveFileName(
            self, "Salvar Template", "template_materiais.xlsx", 
            "Excel Files (*.xlsx)"
        )
        
        if not arquivo:
            return
        
        try:
            # Dados de exemplo
            dados_exemplo = [
                ['MAT001', 'Arroz Branco Temperado', 7, 'Alimento Normal', 'N'],
                ['SOP001', 'Sopa de Legumes', 30, 'Sopa', 'S'],
                ['CAL001', 'Caldo de Frango', 15, 'Caldo', 'N'],
            ]
            
            df = pd.DataFrame(dados_exemplo, columns=[
                'material', 'descricao', 'dias_validade', 'categoria', 'sopa_especial'
            ])
            
            df.to_excel(arquivo, index=False)
            QMessageBox.information(self, "Sucesso", "Template criado com sucesso!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao criar template: {str(e)}")