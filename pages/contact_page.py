from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ContactPage(BasePage):
    """Formulário "Send Us a Message" da página inicial.

    Seletores obtidos por inspeção do HTML em 25/11/2026 (ids estáveis e data-testid).
    """

    NOME = (By.ID, "name")                # data-testid="ContactName"
    EMAIL = (By.ID, "email")              # data-testid="ContactEmail"
    TELEFONE = (By.ID, "phone")           # data-testid="ContactPhone"
    ASSUNTO = (By.ID, "subject")          # data-testid="ContactSubject"
    MENSAGEM = (By.ID, "description")     # data-testid="ContactDescription"
    ENVIAR = (By.XPATH, "//button[normalize-space()='Submit']")
    ERRO = (By.CSS_SELECTOR, ".alert.alert-danger")
    SUCESSO = (By.XPATH, "//h3[contains(normalize-space(), 'Thanks for getting in touch')]")

    def enviar(self, nome, email, telefone, assunto, mensagem):
        self.digitar(self.NOME, nome)
        self.digitar(self.EMAIL, email)
        self.digitar(self.TELEFONE, telefone)
        self.digitar(self.ASSUNTO, assunto)
        self.digitar(self.MENSAGEM, mensagem)
        self.clicar(self.ENVIAR)

    def mensagem_sucesso(self, timeout=10):
        return self.texto_se_aparecer(self.SUCESSO, timeout)

    def mensagem_erro(self, timeout=10):
        return self.texto_se_aparecer(self.ERRO, timeout)
