import sys
import platform
from PyQt5.QtWidgets import QMessageBox

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    try:
        import pandas
        import openpyxl
    except ImportError:
        QMessageBox.critical(None, "Erro - Dependências", 
                           "Dependências não encontradas!\n\n"
                           "Execute no terminal:\n"
                           "pip install pandas openpyxl\n\n"
                           "Ou se estiver usando conda:\n"
                           "conda install pandas openpyxl")
        return False
    
    # Verificar pywin32 no Windows (opcional)
    if platform.system() == "Windows":
        try:
            import win32print
            import win32api
        except ImportError:
            resposta = QMessageBox.question(None, "Dependência Opcional", 
                                          "Para melhor funcionamento no Windows, instale pywin32:\n\n"
                                          "pip install pywin32\n\n"
                                          "Deseja continuar mesmo assim?",
                                          QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.No:
                return False
    
    return True

def mostrar_dicas_sistema():
    """Mostra dicas específicas do sistema operacional"""
    sistema = platform.system()
    
    if sistema == "Windows":
        print("🖥️ Sistema Windows detectado")
        print("📋 Dicas para configuração:")
        print("   1. Certifique-se que a impressora Zebra ZD220 está conectada via USB")
        print("   2. Instale os drivers da Zebra (ZebraLink)")
        print("   3. Configure a impressora no Windows (Painel de Controle > Impressoras)")
        print("   4. Para melhor funcionamento: pip install pywin32")
        print("   5. Se necessário, compartilhe a impressora local")
    elif sistema == "Linux":
        print("🐧 Sistema Linux detectado")
        print("📋 Dicas para configuração:")
        print("   1. Instale o CUPS: sudo apt-get install cups")
        print("   2. Configure a impressora: sudo lpadmin -p ZD220 -E -v usb://Zebra/ZD220")
        print("   3. Verifique com: lpstat -p")
    elif sistema == "Darwin":  # macOS
        print("🍎 Sistema macOS detectado")
        print("📋 Dicas para configuração:")
        print("   1. Adicione a impressora via Preferências do Sistema")
        print("   2. Selecione o driver genético ou Zebra específico")
    else:
        print(f"💻 Sistema {sistema} detectado")