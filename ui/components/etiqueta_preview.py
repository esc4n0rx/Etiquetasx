from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class EtiquetaPreview(QWidget):
    def __init__(self):
        super().__init__()
        self.dados = None
        self.configuracoes = {
            'fonte_titulo': 18,
            'fonte_subtitulo': 14, 
            'fonte_texto': 12,
            'centralizar': True,
            'espacamento': 25,
            'margem_x': 20,
            'margem_y': 20
        }
        self.setMinimumSize(300, 400)
        self.setMaximumSize(350, 450)
    
    def atualizar_dados(self, dados):
        """Atualiza dados do preview"""
        self.dados = dados
        self.update()
    
    def atualizar_configuracoes(self, config):
        """Atualiza configurações de layout"""
        self.configuracoes.update(config)
        self.update()
    
    def limpar(self):
        """Limpa o preview"""
        self.dados = None
        self.update()
    
    def mostrar_erro(self, mensagem):
        """Mostra mensagem de erro no preview"""
        self.dados = {'erro': mensagem}
        self.update()
    
    def paintEvent(self, event):
        """Desenha o preview da etiqueta"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fundo da etiqueta
        rect = self.rect().adjusted(10, 10, -10, -10)
        painter.fillRect(rect, QColor(255, 255, 255))
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        painter.drawRect(rect)
        
        if not self.dados:
            self._desenhar_placeholder(painter, rect)
            return
        
        if 'erro' in self.dados:
            self._desenhar_erro(painter, rect)
            return
        
        if self.dados.get('tipo') == 'sopa':
            self._desenhar_etiqueta_sopa(painter, rect)
        else:
            self._desenhar_etiqueta_normal(painter, rect)
    
    def _desenhar_placeholder(self, painter, rect):
        """Desenha placeholder quando não há dados"""
        painter.setPen(QColor(150, 150, 150))
        painter.setFont(QFont("Arial", 12))
        painter.drawText(rect, Qt.AlignCenter, "Aguardando dados...\n\nDigite um código e\nclique em 'Buscar Material'")
    
    def _desenhar_erro(self, painter, rect):
        """Desenha mensagem de erro"""
        painter.setPen(QColor(231, 76, 60))
        painter.setFont(QFont("Arial", 11, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, f"⚠️ {self.dados['erro']}")
    
    def _desenhar_etiqueta_normal(self, painter, rect):
       """Desenha etiqueta normal"""
       x = rect.x() + self.configuracoes['margem_x']
       y = rect.y() + self.configuracoes['margem_y']
       largura = rect.width() - (self.configuracoes['margem_x'] * 2)
       
       if self.configuracoes['centralizar']:
           align = Qt.AlignCenter
       else:
           align = Qt.AlignLeft
       
       # Código
       painter.setPen(QColor(44, 62, 80))
       painter.setFont(QFont("Arial", self.configuracoes['fonte_titulo'], QFont.Bold))
       codigo_rect = QRect(x, y, largura, 30)
       painter.drawText(codigo_rect, align, f"Codigo: {self.dados['codigo']}")
       
       y += self.configuracoes['espacamento'] + 10
       
       # Descrição
       painter.setFont(QFont("Arial", self.configuracoes['fonte_subtitulo'], QFont.Bold))
       desc_rect = QRect(x, y, largura, 25)
       painter.drawText(desc_rect, align, "Descrição:")
       
       y += self.configuracoes['espacamento']
       
       # Texto da descrição (quebrar se necessário)
       painter.setFont(QFont("Arial", self.configuracoes['fonte_texto']))
       descricao_lines = self._quebrar_texto(self.dados['descricao'], largura, painter.fontMetrics())
       
       for linha in descricao_lines:
           linha_rect = QRect(x, y, largura, 20)
           painter.drawText(linha_rect, align, linha)
           y += self.configuracoes['espacamento'] - 5
       
       y += 10
       
       # Validade
       painter.setPen(QColor(39, 174, 96))
       painter.setFont(QFont("Arial", self.configuracoes['fonte_subtitulo'], QFont.Bold))
       val_rect = QRect(x, y, largura, 25)
       painter.drawText(val_rect, align, f"Validade: {self.dados['validade']}")
       
       y += self.configuracoes['espacamento'] + 10
       
       # Data de impressão
       painter.setPen(QColor(127, 140, 141))
       painter.setFont(QFont("Arial", self.configuracoes['fonte_texto'] - 2))
       from datetime import datetime
       data_impressao = datetime.now().strftime('%d/%m/%Y %H:%M')
       data_rect = QRect(x, y, largura, 20)
       painter.drawText(data_rect, align, f"Data: {data_impressao}")
   
    def _desenhar_etiqueta_sopa(self, painter, rect):
        """Desenha etiqueta de sopa"""
        x = rect.x() + self.configuracoes['margem_x']
        y = rect.y() + self.configuracoes['margem_y']
        largura = rect.width() - (self.configuracoes['margem_x'] * 2)
        
        if self.configuracoes['centralizar']:
            align = Qt.AlignCenter
        else:
            align = Qt.AlignLeft
        
        # Código
        painter.setPen(QColor(44, 62, 80))
        painter.setFont(QFont("Arial", self.configuracoes['fonte_titulo'], QFont.Bold))
        codigo_rect = QRect(x, y, largura, 30)
        painter.drawText(codigo_rect, align, f"Codigo: {self.dados['codigo']}")
        
        y += self.configuracoes['espacamento'] + 5
        
        # Descrição
        painter.setFont(QFont("Arial", self.configuracoes['fonte_subtitulo'], QFont.Bold))
        desc_rect = QRect(x, y, largura, 25)
        painter.drawText(desc_rect, align, "Descrição:")
        
        y += self.configuracoes['espacamento'] - 5
        
        # Texto da descrição
        painter.setFont(QFont("Arial", self.configuracoes['fonte_texto']))
        descricao_lines = self._quebrar_texto(self.dados['descricao'], largura, painter.fontMetrics())
        
        for linha in descricao_lines:
            linha_rect = QRect(x, y, largura, 18)
            painter.drawText(linha_rect, align, linha)
            y += self.configuracoes['espacamento'] - 8
        
        y += 5
        
        # Código da sopa (se disponível)
        if self.dados.get('codigo_sopa'):
            painter.setPen(QColor(142, 68, 173))
            painter.setFont(QFont("Arial", self.configuracoes['fonte_subtitulo'], QFont.Bold))
            sopa_rect = QRect(x, y, largura, 25)
            painter.drawText(sopa_rect, align, f"Codigo Sopa: {self.dados['codigo_sopa']}")
            y += self.configuracoes['espacamento']
        
        # Validade
        painter.setPen(QColor(39, 174, 96))
        painter.setFont(QFont("Arial", self.configuracoes['fonte_subtitulo'], QFont.Bold))
        val_rect = QRect(x, y, largura, 25)
        painter.drawText(val_rect, align, f"Validade: {self.dados['validade']}")
        
        y += self.configuracoes['espacamento']
        
        # Informações de conservação
        painter.setPen(QColor(230, 126, 34))
        painter.setFont(QFont("Arial", self.configuracoes['fonte_texto'] - 1, QFont.Bold))
        
        conservacao_lines = self.dados.get('conservacao', '').split('\n')
        for linha in conservacao_lines:
            if linha.strip():
                cons_rect = QRect(x, y, largura, 16)
                painter.drawText(cons_rect, align, linha.strip())
                y += self.configuracoes['espacamento'] - 10
        
        y += 5
        
        # Data de impressão
        painter.setPen(QColor(127, 140, 141))
        painter.setFont(QFont("Arial", self.configuracoes['fonte_texto'] - 2))
        from datetime import datetime
        data_impressao = datetime.now().strftime('%d/%m/%Y %H:%M')
        data_rect = QRect(x, y, largura, 20)
        painter.drawText(data_rect, align, f"Data: {data_impressao}")
    
    def _quebrar_texto(self, texto, largura_max, font_metrics):
        """Quebra texto em linhas que cabem na largura"""
        palavras = texto.split()
        linhas = []
        linha_atual = ""
        
        for palavra in palavras:
            teste_linha = linha_atual + (" " if linha_atual else "") + palavra
            if font_metrics.horizontalAdvance(teste_linha) <= largura_max:
                linha_atual = teste_linha
            else:
                if linha_atual:
                    linhas.append(linha_atual)
                linha_atual = palavra
        
        if linha_atual:
            linhas.append(linha_atual)
        
        return linhas