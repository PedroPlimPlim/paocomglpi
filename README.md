# GLPI Tools

Ferramentas de automação para consulta e preenchimento de planilhas a partir do GLPI.

---

## Funcionalidades

| Opção | Nome | O que faz |
|---|---|---|
| 1 | Scrapping de Chamados | Preenche Analista, Início e Final do atendimento |
| 2 | Café com Elsys | Identifica chamados Elsys e preenche Analista, Resultado e Observação |

---

## Instalação

> Pré-requisito: Python 3.10 ou superior instalado.

**1. Clone o repositório**
```bash
git clone <url-do-repositorio>
cd glpiscrapping
```

**2. (Recomendado) Crie e ative um ambiente virtual**
```bash
# Criar
python -m venv venv

# Ativar — Windows
venv\Scripts\activate

# Ativar — Linux/Mac
source venv/bin/activate
```
> Com a venv ativa, os pacotes ficam isolados do Python global.  
> Para desativar quando terminar: `deactivate`

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Instale o navegador usado pelo Playwright**
```bash
playwright install chromium
```

---

## Configuração

Abra o arquivo `config.py` e preencha:

```python
GLPI_URL  = "https://blablabla.blablabla.com"   # sem subdominios 
GLPI_USER = "seu.usuario@email.com"              # seu e-mail de acesso ao GLPI
GLPI_PASS = "sua_senha"                        # sua senha do GLPI

ANALISTAS = [
    "Nome Analista 1",   # nomes EXATAMENTE como aparecem no GLPI
    "Nome Analista 2",
]
```

> **Atenção:** nunca suba o `config.py` com suas credenciais para o GitHub.  
> O arquivo já está no `.gitignore` — verifique antes de fazer commit.

---

## Como usar

**1. Coloque a planilha na pasta `input/`**

**2. Execute o programa**
```bash
python main.py
```

**3. Escolha a opção no menu e siga as instruções na tela**

Os resultados são salvos automaticamente em `output/` com o sufixo `_scrapped`.

---

## Estrutura do projeto

```
glpiscrapping/
├── main.py                  # ponto de entrada — menu principal
├── config.py                # credenciais e configurações (não versionar)
├── requirements.txt
├── input/                   # coloque as planilhas aqui
├── output/                  # resultados gerados aqui
└── modules/
    ├── glpi_base.py         # funções compartilhadas (login, helpers)
    ├── scrapper.py          # Scrapping de Chamados
    └── cafe_elsys.py        # Café com Elsys
```

---

## Formato das planilhas

### Scrapping de Chamados
- Coluna com os tickets: `GLPI`
- Aceita formatos: `181442`, `181 442`, `181442/1`
- Colunas preenchidas: `Analista`, `Início do atendimento`, `Final do atendimento`

### Café com Elsys
- Coluna com os tickets: `GLPI`, `ID` ou `TICKET`
- Aceita os mesmos formatos acima
- Colunas preenchidas: `Analista`, `Resultado`, `Observação`
- Critério de preenchimento: ticket contém `TECNOLOGIA: ELSYS`, `OPERADORA: TIM`, `TOPOLOGIA: 2` ou `TIPO DE SITE: 2` -> podem ser alterados no código cafe_elsys.py
