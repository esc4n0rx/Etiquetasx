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
        
        return impressoras
    
    def imprimir(self, zpl_code):
        """Imprime código ZPL"""
        impressora_nome = self.settings_manager.get_printer_name()
        
        if not impressora_nome:
            raise Exception("Nenhuma impressora configurada!")
        
        try:
            return self._enviar_para_impressora(impressora_nome, zpl_code)
        except Exception as e:
            raise Exception(f"Erro ao imprimir: {str(e)}")
    
    def _enviar_para_impressora(self, impressora_nome, zpl_code):
        """Envia ZPL para impressora específica"""
        sucesso = False
        
        # Método 1: win32print (Windows)
        if WIN32_AVAILABLE and platform.system() == "Windows":
            try:
                printer_handle = win32print.OpenPrinter(impressora_nome)
                try:
                    job_info = ("Etiqueta", None, "RAW")
                    job_id = win32print.StartDocPrinter(printer_handle, 1, job_info)
                    try:
                        win32print.StartPagePrinter(printer_handle)
                        win32print.WritePrinter(printer_handle, zpl_code.encode('utf-8'))
                        win32print.EndPagePrinter(printer_handle)
                        sucesso = True
                    finally:
                        win32print.EndDocPrinter(printer_handle)
                finally:
                    win32print.ClosePrinter(printer_handle)
            except Exception as e:
                print(f"Erro com win32print: {e}")
        
        # Método 2: Comando do sistema (fallback)
        if not sucesso:
            try:
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
                
            except Exception as e:
                print(f"Erro com comando do sistema: {e}")
        
        return sucesso
    
    def testar_impressora(self, impressora_nome):
        """Testa impressora com etiqueta de teste"""
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