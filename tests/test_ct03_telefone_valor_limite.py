"""CT03 — Telefone abaixo, no limite e acima do tamanho permitido.

Técnica: análise de valor-limite. O próprio sistema informa a regra:
"Phone must be between 11 and 21 characters." → limites 11 e 21.
Valores testados: 10 (abaixo), 11 (mínimo), 21 (máximo), 22 (acima).
Critério de aceitação: CA2.
"""
import pytest

from pages.contact_page import ContactPage

ERRO_TELEFONE = "Phone must be between 11 and 21 characters."


@pytest.mark.contato
@pytest.mark.parametrize(
    "tamanho, deve_aceitar",
    [(10, False), (11, True), (21, True), (22, False)],
    ids=["10_abaixo_do_minimo", "11_minimo", "21_maximo", "22_acima_do_maximo"],
)
def test_ct03_telefone_valor_limite(driver, base_url, tamanho, deve_aceitar):
    pagina = ContactPage(driver, base_url)
    pagina.abrir("/")

    pagina.enviar(
        nome="Bruno Ficticio",
        email="bruno.ficticio@exemplo.com",
        telefone="1" * tamanho,
        assunto="Teste de valor-limite",
        mensagem="Mensagem ficticia para teste de valor-limite do telefone.",
    )

    if deve_aceitar:
        confirmacao = pagina.mensagem_sucesso()
        assert confirmacao and "Thanks for getting in touch" in confirmacao, (
            f"Telefone com {tamanho} caracteres deveria ser aceito. "
            f"Erro exibido: {pagina.mensagem_erro(timeout=1)!r}"
        )
    else:
        erro = pagina.mensagem_erro()
        assert erro is not None and ERRO_TELEFONE in erro, (
            f"Telefone com {tamanho} caracteres deveria ser recusado com '{ERRO_TELEFONE}'. "
            f"Erro obtido: {erro!r}; confirmação: {pagina.mensagem_sucesso(timeout=1)!r}"
        )
