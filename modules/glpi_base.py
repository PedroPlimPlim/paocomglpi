"""
Funções compartilhadas entre os módulos: login, seleção de planilha, helpers.
"""

import re
from pathlib import Path
from playwright.sync_api import TimeoutError as PWTimeout

import config

SELETORES_USER = [
    'input[id="login_name"]',   'input[id="username"]',
    'input[name="login_name"]', 'input[name="username"]',
    'input[autocomplete="username"]',
]
SELETORES_PASS = [
    'input[id="login_password"]',   'input[id="password"]',
    'input[name="login_password"]', 'input[name="password"]',
    'input[autocomplete="current-password"]', 'input[type="password"]',
]
SELETORES_SUBMIT = [
    'button[type="submit"]', 'input[type="submit"]',
    'button:has-text("Entrar")', 'button:has-text("Sign in")',
]


def limpar_ticket_id(valor) -> int | None:
    """Normaliza IDs como '181 442', '181442/1', '181442/2' → 181442."""
    if not valor:
        return None
    s = str(valor).replace(" ", "").split("/")[0].strip()
    return int(s) if s.isdigit() else None


def _preencher(page, seletores, valor):
    for sel in seletores:
        try:
            elem = page.query_selector(sel)
            if elem and elem.is_visible():
                page.fill(sel, valor)
                return True
        except Exception:
            continue
    return False


def login(page):
    print(f"  [LOGIN] Acessando {config.GLPI_URL} ...")
    page.goto(f"{config.GLPI_URL}/index.php", wait_until="domcontentloaded", timeout=30_000)

    ok_user = _preencher(page, SELETORES_USER, config.GLPI_USER)
    ok_pass = _preencher(page, SELETORES_PASS, config.GLPI_PASS)

    if ok_user and ok_pass:
        for sel in SELETORES_SUBMIT:
            try:
                elem = page.query_selector(sel)
                if elem and elem.is_visible():
                    page.click(sel)
                    break
            except Exception:
                continue
    else:
        print("  [LOGIN] ⚠ Login automático falhou — aguardando login manual (120s)...")

    # Tenta por 10s; se não entrar avisa sobre credenciais e tenta mais 10s
    url_logado = re.compile(r".*(central|ticket|dashboard).*")
    try:
        page.wait_for_url(url_logado, timeout=10_000)
    except PWTimeout:
        print("  [LOGIN] ⏳ Aguardando... Você preencheu suas credenciais no config.py?")
        try:
            page.wait_for_url(url_logado, timeout=10_000)
        except PWTimeout:
            raise PWTimeout("Não foi possível fazer o login.")
    print("  [LOGIN] Autenticado com sucesso!\n")


def listar_planilhas() -> list[Path]:
    pasta = Path("input")
    return sorted(pasta.glob("*.xlsx")) + sorted(pasta.glob("*.xls"))


def selecionar_planilha() -> Path | None:
    arquivos = listar_planilhas()
    if not arquivos:
        print("\n  Nenhuma planilha encontrada na pasta 'input'.")
        print("  Coloque o arquivo .xlsx na pasta 'input' e tente novamente.\n")
        return None

    print("\n  Planilhas disponíveis em 'input':\n")
    for i, arq in enumerate(arquivos, 1):
        print(f"    {i}. {arq.name}")
    print()

    while True:
        escolha = input("  Número da planilha (0 para voltar): ").strip()
        if escolha == "0":
            return None
        if escolha.isdigit() and 1 <= int(escolha) <= len(arquivos):
            return arquivos[int(escolha) - 1]
        print("  Opção inválida. Tente novamente.")


def localizar_cabecalho(ws, coluna_ticket: str) -> tuple[int, dict] | tuple[None, None]:
    """Varre as primeiras 10 linhas procurando a coluna de ticket. Retorna (linha, mapa)."""
    for row in ws.iter_rows(min_row=1, max_row=10):
        mapa = {cell.value: cell.column for cell in row if cell.value}
        if coluna_ticket in mapa:
            return row[0].row, mapa
    return None, None


def salvar_output(wb, caminho_entrada: Path) -> Path:
    pasta_saida = Path("output")
    pasta_saida.mkdir(exist_ok=True)
    nome_saida = caminho_entrada.stem + "_scrapped" + caminho_entrada.suffix
    destino = pasta_saida / nome_saida
    wb.save(destino)
    return destino
