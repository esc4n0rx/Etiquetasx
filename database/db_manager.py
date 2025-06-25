import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path="etiquetas.db"):
        self.db_path = db_path
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.create_tables()
            print(f"✅ Banco de dados conectado: {self.db_path}")
        except Exception as e:
            print(f"❌ Erro ao conectar banco: {e}")
            raise
    
    def create_tables(self):
        """Cria as tabelas necessárias"""
        cursor = self.conn.cursor()
        
        # Tabela de materiais atualizada
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materiais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                material TEXT UNIQUE NOT NULL,
                descricao TEXT NOT NULL,
                dias_validade INTEGER NOT NULL,
                categoria TEXT NOT NULL,
                sopa_especial TEXT DEFAULT 'N' CHECK(sopa_especial IN ('S', 'N')),
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Verificar se precisa adicionar a coluna sopa_especial
        cursor.execute("PRAGMA table_info(materiais)")
        colunas = [row[1] for row in cursor.fetchall()]
        
        if 'sopa_especial' not in colunas:
            cursor.execute('ALTER TABLE materiais ADD COLUMN sopa_especial TEXT DEFAULT "N"')
            print("✅ Coluna 'sopa_especial' adicionada à tabela materiais")
        
        # Tabela de impressões (log)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS impressoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                material TEXT NOT NULL,
                tipo TEXT NOT NULL,
                dados_extras TEXT,
                data_impressao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        print("✅ Tabelas criadas/verificadas com sucesso")
    
    def get_cursor(self):
        """Retorna cursor do banco"""
        return self.conn.cursor()
    
    def commit(self):
        """Commit das transações"""
        self.conn.commit()
    
    def close(self):
        """Fecha a conexão"""
        if self.conn:
            self.conn.close()
    
    def inserir_material(self, material, descricao, dias_validade, categoria, sopa_especial='N'):
        """Insere novo material"""
        cursor = self.get_cursor()
        cursor.execute('''
            INSERT INTO materiais (material, descricao, dias_validade, categoria, sopa_especial)
            VALUES (?, ?, ?, ?, ?)
        ''', (material, descricao, dias_validade, categoria, sopa_especial))
        self.commit()
    
    def listar_materiais(self):
        """Lista todos os materiais"""
        cursor = self.get_cursor()
        cursor.execute('''
            SELECT id, material, descricao, dias_validade, categoria, sopa_especial
            FROM materiais ORDER BY material
        ''')
        return cursor.fetchall()
    
    def deletar_material(self, material_id):
        """Deleta material por ID"""
        cursor = self.get_cursor()
        cursor.execute('DELETE FROM materiais WHERE id = ?', (material_id,))
        self.commit()
    
    def log_impressao(self, material, tipo, dados_extras=None):
        """Registra impressão no log"""
        cursor = self.get_cursor()
        cursor.execute('''
            INSERT INTO impressoes (material, tipo, dados_extras)
            VALUES (?, ?, ?)
        ''', (material, tipo, dados_extras))
        self.commit()