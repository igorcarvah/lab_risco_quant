import os
import glob
import sys
from datetime import datetime

# Tenta importar a biblioteca de automação do Windows
try:
    import win32com.client as win32
    TEM_LIBS_WINDOWS = True
except ImportError:
    TEM_LIBS_WINDOWS = False

# ==============================================================================
# 🛠️ CONFIGURAÇÃO DE CAMINHOS (FIXED)
# ==============================================================================
DIRETORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
# Sobe 2 níveis: scripts -> src -> RAIZ
RAIZ_PROJETO = os.path.abspath(os.path.join(DIRETORIO_SCRIPT, "..", "..")) 
PASTA_REPORTS = os.path.join(RAIZ_PROJETO, "reports")
# ==============================================================================

def validar_ambiente_bancario():
    """Verifica se o computador tem as ferramentas corporativas necessárias."""
    if not TEM_LIBS_WINDOWS:
        print("\n❌ ERRO CRÍTICO DE AMBIENTE")
        print("As bibliotecas de automação Windows não foram encontradas.")
        print("Este sistema exige ambiente Windows com Outlook Desktop instalado.")
        sys.exit(1)

def main():
    print(f"\n📧 --- MÓDULO DE DISTRIBUIÇÃO CORPORATIVA (STRICT MODE) ---")
    validar_ambiente_bancario()

    # 1. Validação de Arquivos
    if not os.path.exists(PASTA_REPORTS):
        print(f"❌ ERRO: Pasta 'reports' não encontrada em: {PASTA_REPORTS}")
        return

    arquivos = glob.glob(os.path.join(PASTA_REPORTS, "*.xlsx"))
    if not arquivos:
        print(f"❌ Nenhum relatório (.xlsx) disponível para envio.")
        return

    # Pega o arquivo mais recente
    arquivo_recente = os.path.abspath(max(arquivos, key=os.path.getmtime))
    nome_arquivo = os.path.basename(arquivo_recente)
    print(f"📎 Arquivo em anexo: {nome_arquivo}")

    # 2. Input de Destinatários
    print("\n👥 Digite os e-mails corporativos (separados por vírgula).")
    input_usuario = input("Destinatários: ")
    if not input_usuario: return

    # Tratamento para ponto e vírgula (Padrão Outlook)
    lista_limpa = [email.strip() for email in input_usuario.split(',')]
    destinatarios_outlook = "; ".join(lista_limpa)

    # 3. ROTINA DE ENVIO (SOMENTE OUTLOOK)
    print("\n🔄 Conectando ao Servidor Exchange/Outlook...")

    try:
        # Tenta instanciar o Outlook Desktop
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        
        # Configuração da Mensagem
        mail.To = destinatarios_outlook
        mail.Subject = f"Relatório Risco de Mercado - {datetime.now().strftime('%d/%m/%Y')}"
        mail.Body = (
            "Prezados,\n\n"
            "Segue em anexo o relatório atualizado de monitoramento de risco e stress testing.\n\n"
            "Atenciosamente,\n"
            "Lab Risco Quant | Automação Financeira"
        )
        
        # Anexo Obrigatório
        mail.Attachments.Add(arquivo_recente)
        
        # Disparo
        mail.Send()
        print(f"✅ SUCESSO! Relatório enviado via Protocolo Corporativo.")
        print(f"📤 Destino: {destinatarios_outlook}")

    except Exception as e:
        # MENSAGEM DE ERRO PERSONALIZADA (PEDIDO DO USUÁRIO)
        print("\n" + "="*60)
        print("⛔ FALHA DE SEGURANÇA / PROTOCOLO")
        print("="*60)
        print("Não foi possível conectar ao Microsoft Outlook Desktop.")
        print("\nMOTIVO:")
        print("1. O Outlook Clássico está fechado ou não instalado.")
        print("2. Você pode estar tentando usar o 'Novo Outlook' (Web), que não permite automação.")
        print("\n⚠️ AVISO:")
        print("Por normas de segurança bancária, o uso de GMAIL ou e-mails pessoais")
        print("é PROIBIDO nesta estação de trabalho. O sistema foi encerrado.")
        print("="*60)
        print(f"Erro técnico original: {e}")

if __name__ == "__main__":
    main()