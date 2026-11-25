from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from pages.base_page import BasePage


class AdminPage(BasePage):
    """Painel administrativo (/admin): login e gestão de quartos."""

    USUARIO = (By.ID, "username")
    SENHA = (By.ID, "password")
    ENTRAR = (By.ID, "doLogin")
    ERRO = (By.CSS_SELECTOR, ".alert.alert-danger")

    NUMERO_QUARTO = (By.ID, "roomName")
    TIPO = (By.ID, "type")
    ACESSIVEL = (By.ID, "accessible")
    PRECO = (By.ID, "roomPrice")
    WIFI = (By.ID, "wifiCheckbox")
    CRIAR = (By.ID, "createRoom")
    LINHAS = (By.CSS_SELECTOR, "[data-testid='roomlisting']")

    def login(self, usuario, senha):
        self.abrir("/admin")
        self.digitar(self.USUARIO, usuario)
        self.digitar(self.SENHA, senha)
        self.clicar(self.ENTRAR)

    def mensagem_erro(self, timeout=10):
        return self.texto_se_aparecer(self.ERRO, timeout)

    def esta_logado(self, timeout=10):
        try:
            self.visivel(self.CRIAR, timeout)
            return True
        except TimeoutException:
            return False

    def criar_quarto(self, numero, tipo="Double", acessivel="true", preco="180", wifi=True):
        self.digitar(self.NUMERO_QUARTO, numero)
        Select(self.visivel(self.TIPO)).select_by_value(tipo)
        Select(self.visivel(self.ACESSIVEL)).select_by_value(acessivel)
        self.digitar(self.PRECO, preco)
        if wifi:
            self.clicar(self.WIFI)
        self.clicar(self.CRIAR)

    def linhas_texto(self):
        return [linha.text.replace("\n", " | ") for linha in self.driver.find_elements(*self.LINHAS)]

    def aguardar_quarto(self, numero, timeout=10):
        """Espera a linha do quarto aparecer na lista; retorna o texto da linha ou None."""
        localizador = (By.XPATH, f"//*[@data-testid='roomlisting'][.//*[@id='roomName{numero}']]")
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(localizador)).text
        except TimeoutException:
            return None

    def tentar_excluir_quarto(self, numero, timeout=8):
        """Limpeza best-effort. Retorna True se a linha sumiu da lista.

        Em 25/11/2026 a exclusão retornava HTTP 500 sem aviso na tela (DEF01, sintoma B);
        por isso o resultado é apenas registrado, sem derrubar o teste.
        """
        linha = (By.XPATH, f"//*[@data-testid='roomlisting'][.//*[@id='roomName{numero}']]")
        try:
            self.driver.find_element(*linha).find_element(By.CSS_SELECTOR, "span.roomDelete").click()
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(linha))
            return True
        except Exception:  # noqa: BLE001
            return False
