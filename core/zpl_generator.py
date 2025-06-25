from datetime import datetime
import unicodedata
import re

class ZPLGenerator:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
    
    def gerar_zpl(self, dados):
        """Gera código ZPL baseado no tipo de etiqueta"""
        if dados['tipo'] == 'sopa':
            return self._gerar_zpl_sopa(dados)
        else:
            return self._gerar_zpl_normal(dados)
    
    def _sanitizar_texto_zpl(self, texto):
        """Sanitiza texto para impressoras Zebra ZPL"""
        if not texto:
            return ""
        
        # Mapeamento de caracteres especiais para equivalentes ASCII
        substituicoes = {
            'ç': 'c', 'Ç': 'C',
            'ã': 'a', 'Ã': 'A',
            'à': 'a', 'À': 'A',
            'á': 'a', 'Á': 'A',
            'â': 'a', 'Â': 'A',
            'ä': 'a', 'Ä': 'A',
            'é': 'e', 'É': 'E',
            'è': 'e', 'È': 'E',
            'ê': 'e', 'Ê': 'E',
            'ë': 'e', 'Ë': 'E',
            'í': 'i', 'Í': 'I',
            'ì': 'i', 'Ì': 'I',
            'î': 'i', 'Î': 'I',
            'ï': 'i', 'Ï': 'I',
            'ó': 'o', 'Ó': 'O',
            'ò': 'o', 'Ò': 'O',
            'ô': 'o', 'Ô': 'O',
            'õ': 'o', 'Õ': 'O',
            'ö': 'o', 'Ö': 'O',
            'ú': 'u', 'Ú': 'U',
            'ù': 'u', 'Ù': 'U',
            'û': 'u', 'Û': 'U',
            'ü': 'u', 'Ü': 'U',
            'ñ': 'n', 'Ñ': 'N',
            '°': ' graus',
            '²': '2',
            '³': '3',
            '½': '1/2',
            '¼': '1/4',
            '¾': '3/4',
            '–': '-',
            '—': '-',
            ''': "'",
            ''': "'",
            '"': '"',
            '"': '"',
            '…': '...',
        }
        
        # Aplicar substituições
        texto_sanitizado = texto
        for char_especial, char_ascii in substituicoes.items():
            texto_sanitizado = texto_sanitizado.replace(char_especial, char_ascii)
        
        # Remover caracteres não ASCII restantes
        texto_sanitizado = unicodedata.normalize('NFKD', texto_sanitizado)
        texto_sanitizado = texto_sanitizado.encode('ascii', 'ignore').decode('ascii')
        
        # Remover caracteres problemáticos para ZPL
        texto_sanitizado = re.sub(r'[^\x20-\x7E]', '', texto_sanitizado)
        
        return texto_sanitizado
    
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
        codigo_sanitizado = self._sanitizar_texto_zpl(dados['codigo'])
        zpl += f"^CF0,{config['fonte_titulo'] * 3}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_titulo'] * 3},{config['fonte_titulo'] * 3}^FH\\^FDCodigo: {codigo_sanitizado}^FS\n"
        
        pos_y += config['espacamento'] * 3
        
        # Descrição
        zpl += f"^CF0,{config['fonte_subtitulo'] * 2}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_subtitulo'] * 2},{config['fonte_subtitulo'] * 2}^FH\\^FDDescricao:^FS\n"
        
        pos_y += config['espacamento'] * 2
        
        # Quebrar descrição em linhas
        descricao_sanitizada = self._sanitizar_texto_zpl(dados['descricao'])
        linhas_descricao = self._quebrar_texto(descricao_sanitizada, 30)
        for linha in linhas_descricao:
            zpl += f"^CF0,{config['fonte_texto'] * 2}\n"
            zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_texto'] * 2},{config['fonte_texto'] * 2}^FH\\^FD{linha}^FS\n"
            pos_y += config['espacamento'] * 1.5
        
        pos_y += config['espacamento']
        
        # Validade
        validade_sanitizada = self._sanitizar_texto_zpl(dados['validade'])
        zpl += f"^CF0,{config['fonte_subtitulo'] * 2}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_subtitulo'] * 2},{config['fonte_subtitulo'] * 2}^FH\\^FDValidade: {validade_sanitizada}^FS\n"
        
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
        codigo_sanitizado = self._sanitizar_texto_zpl(dados['codigo'])
        zpl += f"^CF0,{config['fonte_titulo'] * 3}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_titulo'] * 3},{config['fonte_titulo'] * 3}^FH\\^FDCodigo: {codigo_sanitizado}^FS\n"
        
        pos_y += config['espacamento'] * 3
        
        # Descrição
        zpl += f"^CF0,{config['fonte_subtitulo'] * 2}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_subtitulo'] * 2},{config['fonte_subtitulo'] * 2}^FH\\^FDDescricao:^FS\n"
        
        pos_y += config['espacamento'] * 2
        
        # Quebrar descrição em linhas
        descricao_sanitizada = self._sanitizar_texto_zpl(dados['descricao'])
        linhas_descricao = self._quebrar_texto(descricao_sanitizada, 30)
        for linha in linhas_descricao:
            zpl += f"^CF0,{config['fonte_texto'] * 2}\n"
            zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_texto'] * 2},{config['fonte_texto'] * 2}^FH\\^FD{linha}^FS\n"
            pos_y += config['espacamento'] * 1.5
        
        pos_y += config['espacamento']
        
        # Código da sopa (caldeira+turno+lote)
        codigo_sopa_sanitizado = self._sanitizar_texto_zpl(dados['codigo_sopa'])
        zpl += f"^CF0,{config['fonte_subtitulo'] * 2}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_subtitulo'] * 2},{config['fonte_subtitulo'] * 2}^FH\\^FDCodigo Sopa: {codigo_sopa_sanitizado}^FS\n"
        
        pos_y += config['espacamento'] * 2
        
        # Validade
        validade_sanitizada = self._sanitizar_texto_zpl(dados['validade'])
        zpl += f"^CF0,{config['fonte_subtitulo'] * 2}\n"
        zpl += f"^FO{pos_x},{pos_y}^A0{align},{config['fonte_subtitulo'] * 2},{config['fonte_subtitulo'] * 2}^FH\\^FDValidade: {validade_sanitizada}^FS\n"
        
        pos_y += config['espacamento'] * 2
        
        # Informações de conservação (com quebra manual melhorada)
        conservacao_sanitizada = self._sanitizar_texto_zpl(dados['conservacao'])
        
        # Quebrar manualmente o texto de conservação em pontos específicos
        linhas_conservacao_custom = [
            "Conservacao: -10 a -18 graus",
            "ou mais frio.",
            "Validade apos descongelamento:",
            "5 dias"
        ]
        
        for linha in linhas_conservacao_custom:
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