from datetime import datetime

class ZPLGenerator:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
    
    def gerar_zpl(self, dados):
        """Gera código ZPL baseado no tipo de etiqueta"""
        if dados['tipo'] == 'sopa':
            return self._gerar_zpl_sopa(dados)
        else:
            return self._gerar_zpl_normal(dados)
    
    def _gerar_zpl_normal(self, dados):
        """Gera ZPL para etiquetas normais"""
        config = self.settings_manager.get_layout_config()
        
        zpl = "^XA\n"
        zpl += "^MMT\n"
        zpl += "^PW472\n"
        zpl += "^LL1181\n"
        zpl += "^LS0\n"
        
        pos_y = config['margem_y'] * 8
        pos_x = config['margem_x'] * 8
        align = "C" if config['centralizar'] else "N"
        
        if config['centralizar']:
            pos_x = 236  # Centro da etiqueta
        
        # Código
        # Código
        zpl += f"^CF0,{config['fonte_titulo'] * 3}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_titulo'] * 3},{config['fonte_titulo'] * 3}^FH\\^FDCodigo: {dados['codigo']}^FS\n"
        
        pos_y += config['espacamento'] * 3
        
        # Descrição
        zpl += f"^CF0,{config['fonte_subtitulo'] * 2}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_subtitulo'] * 2},{config['fonte_subtitulo'] * 2}^FH\\^FDDescricao:^FS\n"
        
        pos_y += config['espacamento'] * 2
        
        # Quebrar descrição em linhas
        linhas_descricao = self._quebrar_texto(dados['descricao'], 30)
        for linha in linhas_descricao:
            zpl += f"^CF0,{config['fonte_texto'] * 2}\n"
            zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_texto'] * 2},{config['fonte_texto'] * 2}^FH\\^FD{linha}^FS\n"
            pos_y += config['espacamento'] * 1.5
        
        pos_y += config['espacamento']
        
        # Validade
        zpl += f"^CF0,{config['fonte_subtitulo'] * 2}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_subtitulo'] * 2},{config['fonte_subtitulo'] * 2}^FH\\^FDValidade: {dados['validade']}^FS\n"
        
        pos_y += config['espacamento'] * 2
        
        # Data de impressão
        data_impressao = datetime.now().strftime('%d/%m/%Y %H:%M')
        zpl += f"^CF0,{config['fonte_texto'] * 2}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_texto'] * 2},{config['fonte_texto'] * 2}^FH\\^FDData: {data_impressao}^FS\n"
        
        zpl += "^XZ"
        return zpl
    
    def _gerar_zpl_sopa(self, dados):
        """Gera ZPL para etiquetas de sopa"""
        config = self.settings_manager.get_layout_config()
        
        zpl = "^XA\n"
        zpl += "^MMT\n"
        zpl += "^PW472\n"
        zpl += "^LL1181\n"
        zpl += "^LS0\n"
        
        pos_y = config['margem_y'] * 8
        pos_x = config['margem_x'] * 8
        align = "C" if config['centralizar'] else "N"
        
        if config['centralizar']:
            pos_x = 236  # Centro da etiqueta
        
        # Código
        zpl += f"^CF0,{config['fonte_titulo'] * 3}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_titulo'] * 3},{config['fonte_titulo'] * 3}^FH\\^FDCodigo: {dados['codigo']}^FS\n"
        
        pos_y += config['espacamento'] * 3
        
        # Descrição
        zpl += f"^CF0,{config['fonte_subtitulo'] * 2}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_subtitulo'] * 2},{config['fonte_subtitulo'] * 2}^FH\\^FDDescricao:^FS\n"
        
        pos_y += config['espacamento'] * 2
        
        # Quebrar descrição em linhas
        linhas_descricao = self._quebrar_texto(dados['descricao'], 30)
        for linha in linhas_descricao:
            zpl += f"^CF0,{config['fonte_texto'] * 2}\n"
            zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_texto'] * 2},{config['fonte_texto'] * 2}^FH\\^FD{linha}^FS\n"
            pos_y += config['espacamento'] * 1.5
        
        pos_y += config['espacamento']
        
        # Código da sopa (caldeira+turno+lote)
        zpl += f"^CF0,{config['fonte_subtitulo'] * 2}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_subtitulo'] * 2},{config['fonte_subtitulo'] * 2}^FH\\^FDCodigo Sopa: {dados['codigo_sopa']}^FS\n"
        
        pos_y += config['espacamento'] * 2
        
        # Validade
        zpl += f"^CF0,{config['fonte_subtitulo'] * 2}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_subtitulo'] * 2},{config['fonte_subtitulo'] * 2}^FH\\^FDValidade: {dados['validade']}^FS\n"
        
        pos_y += config['espacamento'] * 2
        
        # Informações de conservação
        linhas_conservacao = dados['conservacao'].split('\n')
        for linha in linhas_conservacao:
            if linha.strip():
                zpl += f"^CF0,{config['fonte_texto'] * 2}\n"
                zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_texto'] * 2},{config['fonte_texto'] * 2}^FH\\^FD{linha.strip()}^FS\n"
                pos_y += config['espacamento'] * 1.2
        
        pos_y += config['espacamento']
        
        # Data de impressão
        data_impressao = datetime.now().strftime('%d/%m/%Y %H:%M')
        zpl += f"^CF0,{config['fonte_texto'] * 2}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_texto'] * 2},{config['fonte_texto'] * 2}^FH\\^FDData: {data_impressao}^FS\n"
        
        zpl += "^XZ"
        return zpl
    
    def _quebrar_texto(self, texto, max_chars):
        """Quebra texto em linhas"""
        palavras = texto.split()
        linhas = []
        linha_atual = ""
        
        for palavra in palavras:
            if len(linha_atual + " " + palavra) <= max_chars:
                linha_atual += (" " if linha_atual else "") + palavra
            else:
                if linha_atual:
                    linhas.append(linha_atual)
                linha_atual = palavra
        
        if linha_atual:
            linhas.append(linha_atual)
        
        return linhas