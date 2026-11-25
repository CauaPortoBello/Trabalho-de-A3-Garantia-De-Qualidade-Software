"""CT08 — Administrador cria um quarto e ele aparece na lista.

Técnica: teste funcional baseado em requisito (fluxo principal).
Critério de aceitação: CA6.
O número do quarto é gerado a cada execução para não depender de dados antigos
(o site é reiniciado periodicamente).
"""
import warnings
from datetime import datetime

import pytest

from pages.admin_page import AdminPage


@pytest.mark.admin
def test_ct08_admin_cria_quarto_e_ele_aparece_na_lista(driver, base_url, credenciais_admin):
    numero = f"QA{datetime.now():%m%d%H%M%S}"  # mês+dia+hora: não repete entre execuções
    pagina = AdminPage(driver, base_url)

    pagina.login(*credenciais_admin)
    assert pagina.esta_logado(), f"Login com as credenciais de demonstração falhou: {pagina.mensagem_erro(timeout=1)!r}"

    pagina.criar_quarto(numero, tipo="Double", acessivel="true", preco="180", wifi=True)

    linha = pagina.aguardar_quarto(numero)
    assert linha is not None, f"Quarto {numero} não apareceu na lista. Linhas atuais: {pagina.linhas_texto()}"
    assert "Double" in linha and "180" in linha and "WiFi" in linha, f"Dados divergentes na linha: {linha!r}"

    # Limpeza best-effort (não faz parte da asserção). Ver DEF01, sintoma B.
    if not pagina.tentar_excluir_quarto(numero):
        warnings.warn(f"Limpeza: o quarto {numero} não pôde ser excluído pela interface (ver DEF01, sintoma B).")
