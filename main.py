import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QFont
import platform

# Adicionar o diretório atual ao path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow
from utils.system_check import verificar_dependencias, mostrar_dicas_sistema

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Sistema de Etiquetas")
    app.setApplicationVersion("2.1")
    
    # Configurar fonte padrão da aplicação
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    # Verificar dependências
    if not verificar_dependencias():
        sys.exit(1)
    
    # Mostrar dicas do sistema
    mostrar_dicas_sistema()
    
    print("\n🚀 Iniciando Sistema de Etiquetas v2.1...")
    print("✨ Interface moderna com detecção automática de tipos!")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()