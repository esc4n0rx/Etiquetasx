import platform
import subprocess
import tempfile
import os

try:
    if platform.system() == "Windows":
        import win32print
        import win32api
        WIN32_AVAILABLE = True
    else:
        WIN32_AVAILABLE = False
except ImportError:
    WIN32_AVAILABLE = False

class PrinterManager:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.impressoras_disponiveis = self.listar_impressoras()
    
    def listar_impressoras(self):
        """Lista impressoras disponíveis"""
        impressoras = []
        
        try:
            if WIN32_AVAILABLE:
                # Windows
                printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
                for printer in printers:
                    impressoras.append(printer[2])
            else:
                # Linux/macOS
                try:
                    result = subprocess.run(['lpstat', '-p'], 
                                          capture_output=True, text=True, check=True)
                    for line in result.stdout.split('\n'):
                        if line.startswith('printer'):
                            printer_name = line.split()[1]
                            impressoras.append(printer_name)
                except:
                    impressoras = ["Impressora Padrão"]
        except:
            impressoras = ["Nenhuma impressora encontrada"]
        
        print(f"🖨️ Impressoras encontradas: {impressoras}")
        return impressoras
    
    def imprimir(self, zpl_code):
        """Imprime código ZPL"""
        # Forçar recarregamento da configuração
        impressora_nome = self.settings_manager.get_printer_name()
        
        # Debug detalhado
        print(f"🐛 === DEBUG IMPRESSÃO ===")
        print(f"📋 Impressora recuperada: '{impressora_nome}'")
        print(f"📏 Tamanho da string: {len(impressora_nome) if impressora_nome else 'N/A'}")
        print(f"🔍 É string vazia: {impressora_nome == ''}")
        print(f"🔍 É None: {impressora_nome is None}")
        print(f"📊 Tipo: {type(impressora_nome)}")
        
        # Validação detalhada
        if not impressora_nome:
            raise Exception("❌ Nenhuma impressora configurada! Configure uma impressora na aba 'Configurações'.")
        
        if impressora_nome.strip() == "":
            raise Exception("❌ Nome da impressora está vazio! Configure uma impressora na aba 'Configurações'.")
        
        if impressora_nome == "Nenhuma impressora encontrada":
            raise Exception("❌ Nenhuma impressora válida encontrada! Verifique as impressoras instaladas.")
        
        # Verificar se a impressora está disponível
        if impressora_nome not in self.impressoras_disponiveis:
            print(f"⚠️ AVISO - Impressora '{impressora_nome}' não está na lista atual")
            print(f"📋 Lista atual: {self.impressoras_disponiveis}")
            print(f"🔄 Tentando imprimir mesmo assim...")
        
        try:
            result = self._enviar_para_impressora(impressora_nome, zpl_code)
            print(f"✅ Resultado da impressão: {result}")
            return result
        except Exception as e:
            error_msg = f"❌ Erro ao imprimir na impressora '{impressora_nome}': {str(e)}"
            print(error_msg)
            raise Exception(error_msg)
    
    def _enviar_para_impressora(self, impressora_nome, zpl_code):
        """Envia ZPL para impressora específica"""
        sucesso = False
        
        print(f"📤 Enviando para impressora: '{impressora_nome}'")
        print(f"📄 Tamanho do ZPL: {len(zpl_code)} caracteres")
        
        # Método 1: win32print (Windows)
        if WIN32_AVAILABLE and platform.system() == "Windows":
            try:
                print("🖨️ Tentando método win32print...")
                printer_handle = win32print.OpenPrinter(impressora_nome)
                try:
                    job_info = ("Etiqueta", None, "RAW")
                    job_id = win32print.StartDocPrinter(printer_handle, 1, job_info)
                    try:
                        win32print.StartPagePrinter(printer_handle)
                        win32print.WritePrinter(printer_handle, zpl_code.encode('utf-8'))
                        win32print.EndPagePrinter(printer_handle)
                        sucesso = True
                        print("✅ Impressão enviada via win32print")
                    finally:
                        win32print.EndDocPrinter(printer_handle)
                finally:
                    win32print.ClosePrinter(printer_handle)
            except Exception as e:
                print(f"❌ Erro com win32print: {e}")
        
        # Método 2: Comando do sistema (fallback)
        if not sucesso:
            try:
                print("🖨️ Tentando método de comando do sistema...")
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
                    temp_file.write(zpl_code)
                    temp_file_path = temp_file.name
                
                if platform.system() == "Windows":
                    cmd = f'copy "{temp_file_path}" "\\\\localhost\\{impressora_nome}"'
                    subprocess.run(cmd, shell=True, check=True)
                elif platform.system() == "Linux":
                    cmd = f'lp -d "{impressora_nome}" "{temp_file_path}"'
                    subprocess.run(cmd.split(), check=True)
                elif platform.system() == "Darwin":  # macOS
                    cmd = f'lp -d "{impressora_nome}" "{temp_file_path}"'
                    subprocess.run(cmd.split(), check=True)
                
                os.unlink(temp_file_path)
                sucesso = True
                print("✅ Impressão enviada via comando do sistema")
                
            except Exception as e:
                print(f"❌ Erro com comando do sistema: {e}")
        
        if not sucesso:
            raise Exception("Falha em todos os métodos de impressão")
        
        return sucesso
    
    def testar_impressora(self, impressora_nome):
        """Testa impressora com etiqueta de teste"""
        print(f"🧪 Testando impressora: '{impressora_nome}'")
        
        zpl_teste = """^XA
^MMT
^PW472
^LL1181
^LS0
^CF0,50
^FO50,50^A0N,50,50^FDTESTE^FS
^FO50,150^A0N,30,30^FDSistema de Etiquetas^FS
^FO50,250^A0N,25,25^FDImpressora OK!^FS
^XZ"""
        
        return self._enviar_para_impressora(impressora_nome, zpl_teste)