"""Checagem rápida do ambiente antes de rodar o pytest.

Uso:  python verificar_ambiente.py
Imprime "AMBIENTE OK" quando tudo está pronto.

Conectividade e qualidade funcional são coisas diferentes: qualquer resposta HTTP
(inclusive 403 ou 500) prova que o servidor foi alcançado, mas não prova que as
funcionalidades estão corretas — isso é papel dos testes.
"""
import importlib
import socket
import sys
import urllib.error
import urllib.request

URL = "https://automationintesting.online"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def classificar_conexao(url, timeout=20):
    """Retorna (conectou, descricao). Distingue DNS, conexão, timeout e respostas HTTP."""
    pedido = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(pedido, timeout=timeout) as resp:
            return True, f"HTTP {resp.status} (resposta normal)"
    except urllib.error.HTTPError as erro:
        tipo = "acesso negado" if erro.code == 403 else "erro do servidor" if erro.code >= 500 else "erro HTTP"
        return True, f"HTTP {erro.code} ({tipo}; o servidor respondeu, há conectividade)"
    except urllib.error.URLError as erro:
        motivo = erro.reason
        if isinstance(motivo, socket.gaierror):
            return False, f"falha de DNS ({motivo})"
        if isinstance(motivo, (socket.timeout, TimeoutError)):
            return False, "tempo esgotado (timeout)"
        return False, f"falha de conexão ({motivo})"
    except (socket.timeout, TimeoutError):
        return False, "tempo esgotado (timeout)"
    except OSError as erro:
        return False, f"falha de conexão ({erro})"


def main():
    problemas = []
    print(f"Python {sys.version.split()[0]}")
    if sys.version_info < (3, 10):
        problemas.append(f"Use Python 3.10 ou superior (validado com 3.12.4; atual: {sys.version.split()[0]})")

    for modulo in ("selenium", "pytest", "pytest_html"):
        try:
            mod = importlib.import_module(modulo)
            print(f"{modulo} {getattr(mod, '__version__', '')}")
        except ImportError:
            problemas.append(f"Pacote ausente: {modulo} → rode: python -m pip install -r requirements.txt")

    conectou, descricao = classificar_conexao(URL)
    print(f"Conectividade com {URL}: {descricao}")
    if not conectou:
        problemas.append(f"Sem conexão com {URL}: {descricao}")

    if not problemas:
        try:
            from selenium import webdriver

            opcoes = webdriver.ChromeOptions()
            opcoes.add_argument("--headless=new")
            navegador = webdriver.Chrome(options=opcoes)
            print(f"Chrome {navegador.capabilities.get('browserVersion')} iniciado com sucesso")
            navegador.quit()
        except Exception as erro:  # noqa: BLE001
            problemas.append(f"Não foi possível abrir o Chrome via Selenium: {erro}")

    if problemas:
        print("AMBIENTE COM PROBLEMAS:")
        for p in problemas:
            print(" -", p)
        sys.exit(1)
    print("AMBIENTE OK")


if __name__ == "__main__":
    main()
