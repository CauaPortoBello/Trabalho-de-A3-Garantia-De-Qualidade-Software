from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ESPERA_PADRAO = 15  # segundos; o site é público e às vezes lento


class BasePage:
    """Operações comuns com espera explícita (nunca time.sleep)."""

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, ESPERA_PADRAO)

    def abrir(self, caminho="/"):
        self.driver.get(self.base_url + caminho)

    def visivel(self, locator, timeout=ESPERA_PADRAO):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def rolar_ate(self, elemento):
        # behavior 'instant': o site usa "scroll-behavior: smooth" (Bootstrap); com rolagem
        # animada o clique acontecia no meio do caminho e era interceptado (execução de 25/11/2026).
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});", elemento)

    def clicar(self, locator):
        elemento = self.wait.until(EC.presence_of_element_located(locator))
        self.rolar_ate(elemento)
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def digitar(self, locator, texto):
        elemento = self.visivel(locator)
        elemento.clear()
        elemento.send_keys(texto)

    def texto_se_aparecer(self, locator, timeout=5):
        """Retorna o texto do elemento se ele ficar visível no prazo; senão None."""
        try:
            return self.visivel(locator, timeout).text.strip()
        except TimeoutException:
            return None
