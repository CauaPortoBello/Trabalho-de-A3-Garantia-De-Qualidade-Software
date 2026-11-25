"""CT01 — Contato com todos os campos válidos apresenta confirmação.

Técnica: partição de equivalência (classe válida para todos os campos).
Critério de aceitação: CA1.
"""
import pytest

from pages.contact_page import ContactPage


@pytest.mark.contato
def test_ct01_contato_com_campos_validos_exibe_confirmacao(driver, base_url):
    pagina = ContactPage(driver, base_url)
    pagina.abrir("/")

    pagina.enviar(
        nome="Ana Exemplo",
        email="ana.exemplo@exemplo.com",
        telefone="11987654321",
        assunto="Duvida sobre reserva",
        mensagem="Gostaria de saber se a pousada aceita animais.",
    )

    confirmacao = pagina.mensagem_sucesso()
    assert confirmacao == "Thanks for getting in touch Ana Exemplo!", (
        f"Confirmação esperada não apareceu. Texto obtido: {confirmacao!r}; "
        f"erro exibido: {pagina.mensagem_erro(timeout=1)!r}"
    )
