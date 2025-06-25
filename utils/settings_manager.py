import json
import os
from PyQt5.QtCore import QSettings

class SettingsManager:
    def __init__(self):
        # Usar QSettings do Qt para persistência confiável
        self.settings = QSettings("SistemaEtiquetas", "Config")
        
        # Arquivo JSON como backup
        self.config_file = "config.json"
        
        # Configurações padrão
        self.default_config = {
            'fonte_titulo': 18,
            'fonte_subtitulo': 14,
            'fonte_texto': 12,
            'centralizar': True,
            'espacamento': 25,
            'margem_x': 20,
            'margem_y': 20,
            'impressora': '',
            'largura_etiqueta': 472,
            'altura_etiqueta': 1181
        }
        
        # Carregar configurações salvas ou usar padrão
        self.current_config = self.load_settings()
    
    def load_settings(self):
        """Carrega configurações salvas"""
        try:
            config = {}
            
            # Tentar carregar do QSettings primeiro
            for key, default_value in self.default_config.items():
                if isinstance(default_value, bool):
                    config[key] = self.settings.value(key, default_value, type=bool)
                elif isinstance(default_value, int):
                    config[key] = self.settings.value(key, default_value, type=int)
                else:
                    config[key] = self.settings.value(key, default_value, type=str)
            
            # Garantir que impressora não seja None
            if config['impressora'] is None:
                config['impressora'] = ''
            
            print(f"✅ Configurações carregadas: {config}")
            print(f"🖨️ Impressora carregada: '{config['impressora']}'")
            return config
            
        except Exception as e:
            print(f"⚠️ Erro ao carregar configurações: {e}")
            return self.default_config.copy()
    
    def save_settings(self, config=None):
        """Salva configurações"""
        try:
            if config:
                self.current_config.update(config)
            
            # Garantir que impressora não seja None
            if self.current_config.get('impressora') is None:
                self.current_config['impressora'] = ''
            
            # Salvar no QSettings
            for key, value in self.current_config.items():
                self.settings.setValue(key, value)
                print(f"🔧 Salvando {key}: {value}")
            
            # Forçar sincronização
            self.settings.sync()
            
            # Salvar também em JSON como backup
            self.save_to_json()
            
            print(f"✅ Configurações salvas: {self.current_config}")
            print(f"🖨️ Impressora salva: '{self.current_config.get('impressora')}'")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar configurações: {e}")
            return False
    
    def save_to_json(self):
        """Salva configurações em arquivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_config, f, indent=4, ensure_ascii=False)
            print(f"📄 JSON salvo: {self.config_file}")
        except Exception as e:
            print(f"⚠️ Erro ao salvar JSON: {e}")
    
    def get_layout_config(self):
        """Retorna configurações de layout"""
        return {
            'fonte_titulo': self.current_config.get('fonte_titulo', 18),
            'fonte_subtitulo': self.current_config.get('fonte_subtitulo', 14),
            'fonte_texto': self.current_config.get('fonte_texto', 12),
            'centralizar': self.current_config.get('centralizar', True),
            'espacamento': self.current_config.get('espacamento', 25),
            'margem_x': self.current_config.get('margem_x', 20),
            'margem_y': self.current_config.get('margem_y', 20)
        }
    
    def update_layout_config(self, layout_config):
        """Atualiza configurações de layout"""
        self.current_config.update(layout_config)
        # Salvar automaticamente
        self.save_settings()
    
    def get_printer_name(self):
        """Retorna nome da impressora"""
        impressora = self.current_config.get('impressora', '')
        print(f"🔍 Recuperando impressora: '{impressora}' (tipo: {type(impressora)})")
        
        # Garantir que não seja None
        if impressora is None:
            impressora = ''
            print("⚠️ Impressora era None, convertido para string vazia")
        
        return impressora
    
    def save_printer_name(self, impressora):
        """Salva nome da impressora"""
        print(f"💾 Salvando impressora: '{impressora}' (tipo: {type(impressora)})")
        
        # Garantir que seja string
        if impressora is None:
            impressora = ''
        
        # Atualizar configuração atual
        self.current_config['impressora'] = impressora
        
        # Salvar imediatamente no QSettings
        self.settings.setValue('impressora', impressora)
        self.settings.sync()
        
        # Salvar todas as configurações
        success = self.save_settings()
        
        print(f"📋 Resultado do salvamento: {success}")
        print(f"📊 Config atual após salvamento: {self.current_config}")
        
        return success
    
    def get_default_config(self):
        """Retorna configuração padrão"""
        return self.default_config.copy()
    
    def reset_to_default(self):
        """Reseta para configuração padrão"""
        self.current_config = self.default_config.copy()
        self.save_settings()
        return self.current_config
    
    def get_etiqueta_size(self):
        """Retorna tamanho da etiqueta"""
        return {
            'largura': self.current_config.get('largura_etiqueta', 472),
            'altura': self.current_config.get('altura_etiqueta', 1181)
        }
    
    def debug_config(self):
        """Método de debug para verificar configurações"""
        print("🐛 === DEBUG SETTINGS MANAGER ===")
        print(f"📁 Arquivo config: {self.config_file}")
        print(f"⚙️ QSettings organização: {self.settings.organizationName()}")
        print(f"📱 QSettings aplicação: {self.settings.applicationName()}")
        print(f"📊 Config atual: {self.current_config}")
        print(f"🖨️ Impressora atual: '{self.get_printer_name()}'")
        
        # Verificar QSettings diretamente
        qsettings_impressora = self.settings.value('impressora', '')
        print(f"🔧 QSettings direto: '{qsettings_impressora}'")
        
        # Verificar arquivo JSON
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    json_config = json.load(f)
                print(f"📄 JSON file: {json_config}")
            except Exception as e:
                print(f"❌ Erro ao ler JSON: {e}")
        else:
            print("📄 Arquivo JSON não existe")
        
        print("🐛 === FIM DEBUG ===")