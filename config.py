# ============================================================
#  CONFIGURAÇÕES DO GLPI TOOLS
#  Preencha com suas credenciais antes de rodar
# ============================================================

# --- Credenciais de acesso ao GLPI ---
GLPI_URL  = "https://blabla.bla.com"  # URL do seu GLPI (sem barra no final)
GLPI_USER = "seu.usuario@email.com"
GLPI_PASS = "sua_senha"

# --- Analistas reconhecidos pelo Scrapping de Chamados ---
# Coloque os nomes EXATAMENTE como aparecem no GLPI
ANALISTAS = [
    "Nome Analista 1",
    "Nome Analista 2",
    "Nome Analista 3",
]

# --- Colunas da planilha (Scrapping de Chamados) ---
COLUNA_TICKET             = "GLPI"
COLUNA_ANALISTA           = "Analista"
COLUNA_INICIO_ATENDIMENTO = "Início do atendimento"
COLUNA_FINAL_ATENDIMENTO  = "Final do atendimento"

# --- Comportamento ---
DELAY_ENTRE_CHAMADOS = 0.5   # segundos entre cada chamado
MAX_TENTATIVAS       = 3     # tentativas por chamado em caso de erro