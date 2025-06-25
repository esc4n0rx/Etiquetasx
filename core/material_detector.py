from datetime import datetime, timedelta

class MaterialDetector:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def detectar_material(self, codigo):
        """Detecta tipo de material e retorna informações completas"""
        try:
            cursor = self.db_manager.get_cursor()
            cursor.execute('''
                SELECT descricao, dias_validade, categoria, sopa_especial 
                FROM materiais 
                WHERE material = ?
            ''', (codigo,))
            
            resultado = cursor.fetchone()
            
            if not resultado:
                return None
            
            descricao, dias_validade, categoria, sopa_especial = resultado
            
            # Detectar se é sopa
            eh_sopa = self._eh_sopa(categoria, descricao)
            
            # Calcular validade
            validade_dias = self._calcular_validade(dias_validade, eh_sopa, sopa_especial)
            data_validade = (datetime.now() + timedelta(days=validade_dias)).strftime('%d/%m/%Y')
            
            return {
                'codigo': codigo,
                'descricao': descricao,
                'dias_validade': dias_validade,
                'categoria': categoria,
                'sopa_especial': sopa_especial,
                'tipo': 'sopa' if eh_sopa else 'normal',
                'data_validade': data_validade,
                'validade_dias': validade_dias
            }
            
        except Exception as e:
            raise Exception(f"Erro ao detectar material: {str(e)}")
    
    def _eh_sopa(self, categoria, descricao):
        """Detecta se o material é uma sopa"""
        # Verificar por categoria
        if categoria and 'sopa' in categoria.lower():
            return True
        
        # Verificar por palavras-chave na descrição
        palavras_sopa = ['sopa', 'caldo', 'cremoso', 'líquido', 'potage']
        descricao_lower = descricao.lower()
        
        for palavra in palavras_sopa:
            if palavra in descricao_lower:
                return True
        
        return False
    
    def _calcular_validade(self, dias_validade, eh_sopa, sopa_especial):
        """Calcula a validade baseada nas regras de negócio"""
        if not eh_sopa:
            return dias_validade
        
        # Para sopas normais
        if dias_validade <= 30:
            return dias_validade
        
        # Para sopas especiais (SP=S), dobrar a validade de 30 para 90
        if sopa_especial == 'S' and dias_validade == 30:
            return 90
        
        return dias_validade