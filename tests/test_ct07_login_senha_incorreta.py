"""CT07 — Login administrativo com senha incorreta.

Técnica: partição de equivalência (classe inválida: senha errada).
Critério de aceitação: CA5. Não precisa da senha real: usa uma senha fictícia errada.
"""
import pytest

from pages.admin_page import AdminPage


@pytest.mark.admin
def test_ct07_login_com_senha_incorreta_e_recusado(driver, base_url):
    pagina = AdminPage(driver, base_url)

    pagina.login("admin", "senhaErrada123")

    assert pagina.mensagem_erro() == "Invalid credentials"
    assert not pagina.esta_logado(timeout=3), "O painel de quartos não deveria abrir com senha incorreta"
