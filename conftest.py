"""Configuração central da suíte A3 — Grupo 4 (Restful Booker Platform).

- BASE_URL centralizada (pode ser sobrescrita pela variável de ambiente BASE_URL).
- Leitura opcional de um arquivo .env (sem dependência extra).
- Fixture `driver`: abre e fecha o Chrome a cada teste.
- Captura automática de screenshot ao final de cada teste (passou ou falhou)
  em evidencias/screenshots/.
- Verificação de conectividade: só uma falha de rede (DNS, conexão, tempo
  esgotado) marca os testes como SKIP "AMBIENTE". Qualquer resposta HTTP,
  mesmo 403 ou 500, conta como site alcançado.
"""
import os
import re
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver

try:
    import pytest_html
except ImportError:  # o relatório HTML é opcional
    pytest_html = None

RAIZ = Path(__file__).parent


def _carregar_env(caminho: Path) -> None:
    """Lê pares CHAVE=valor de um .env simples sem sobrescrever variáveis já definidas."""
    if not caminho.exists():
        return
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        os.environ.setdefault(chave.strip(), valor.strip())


_carregar_env(RAIZ / ".env")

BASE_URL = os.environ.get("BASE_URL", "https://automationintesting.online").rstrip("/")
HEADLESS = os.environ.get("HEADLESS", "0") == "1"
# Credenciais PÚBLICAS de demonstração publicadas no README oficial do projeto
# (https://github.com/mwinteringham/restful-booker-platform, seção "Login").
# Podem ser sobrescritas por ADMIN_USERNAME / ADMIN_PASSWORD no .env.
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME") or "admin"
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") or "password"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
PASTA_SCREENSHOTS = RAIZ / "evidencias" / "screenshots"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


def checar_conectividade(url, timeout=20):
    """Retorna None se houve comunicação HTTP com o servidor; senão, o motivo da falha de rede.

    Qualquer resposta HTTP (inclusive 403 ou 500) prova que o servidor foi alcançado:
    se uma funcionalidade está quebrada, isso é papel dos testes descobrir, não da
    verificação de conectividade. Só erros de DNS, conexão ou tempo esgotado contam.
    """
    pedido = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(pedido, timeout=timeout):
            return None
    except urllib.error.HTTPError:
        return None  # o servidor respondeu
    except (urllib.error.URLError, OSError) as erro:
        return str(getattr(erro, "reason", erro))


@pytest.fixture(scope="session", autouse=True)
def site_disponivel():
    """Falha de rede é problema de AMBIENTE, não defeito do sistema."""
    motivo = checar_conectividade(BASE_URL)
    if motivo:
        pytest.skip(f"AMBIENTE: sem conexão com {BASE_URL} ({motivo})")


@pytest.fixture
def driver():
    opcoes = webdriver.ChromeOptions()
    if HEADLESS:
        opcoes.add_argument("--headless=new")
    opcoes.add_argument("--window-size=1366,900")
    opcoes.add_argument("--lang=pt-BR")
    navegador = webdriver.Chrome(options=opcoes)  # Selenium Manager resolve o chromedriver
    yield navegador
    navegador.quit()


@pytest.fixture
def credenciais_admin():
    return ADMIN_USERNAME, ADMIN_PASSWORD


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Salva um screenshot ao fim da fase de execução de cada teste."""
    resultado = yield
    relatorio = resultado.get_result()
    if relatorio.when != "call":
        return
    navegador = item.funcargs.get("driver")
    if navegador is None:
        return
    PASTA_SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    status = "PASSOU" if relatorio.passed else "FALHOU"
    nome = re.sub(r"[^\w\-]+", "_", item.name)
    arquivo = PASTA_SCREENSHOTS / f"{nome}_{status}_{datetime.now():%Y%m%d_%H%M%S}.png"
    try:
        imagem_b64 = navegador.get_screenshot_as_base64()
        navegador.save_screenshot(str(arquivo))
    except Exception:  # noqa: BLE001 - evidência não pode derrubar o relatório
        return
    if pytest_html is not None:  # embute a imagem no relatório HTML do pytest-html
        extras = getattr(relatorio, "extras", [])
        extras.append(pytest_html.extras.png(imagem_b64))
        relatorio.extras = extras
