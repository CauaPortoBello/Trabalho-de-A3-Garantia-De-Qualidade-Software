from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class BookingPage(BasePage):
    """Bloco "Check Availability & Book Your Stay" da página inicial.

    Os campos de data são componentes react-datepicker sem id próprio; o formato
    exibido é dd/MM/aaaa (confirmado em 25/11/2026: 10/12/2026 gera checkout=2026-12-10).
    """

    DATAS = (By.CSS_SELECTOR, "#booking .react-datepicker__input-container input")
    TITULO = (By.XPATH, "//h3[contains(., 'Check Availability')]")
    VERIFICAR = (By.XPATH, "//button[normalize-space()='Check Availability']")
    LINKS_RESERVA = (By.CSS_SELECTOR, "a[href*='/reservation/']")
    # qualquer aviso de validação que o site venha a exibir no bloco de reserva
    AVISO = (By.CSS_SELECTOR, "#booking .alert, #booking .invalid-feedback, #booking .text-danger")

    def _preencher_data(self, campo, data_ddmmaaaa):
        self.rolar_ate(campo)
        campo.click()
        campo.send_keys(Keys.CONTROL, "a")
        campo.send_keys(data_ddmmaaaa)
        self.clicar(self.TITULO)  # fecha o calendário sem descartar o valor
        if campo.get_attribute("value") != data_ddmmaaaa:
            # Plano B documentado: alguns navegadores/SOs não repassam Ctrl+A ao datepicker.
            # Usa o setter nativo + evento "input", o mesmo caminho que a digitação percorre no React.
            self.driver.execute_script(
                "const s = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;"
                "s.call(arguments[0], arguments[1]);"
                "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));",
                campo, data_ddmmaaaa,
            )
            self.clicar(self.TITULO)

    def buscar(self, entrada, saida):
        self.abrir("/")
        self.wait.until(lambda d: len(d.find_elements(*self.DATAS)) == 2)
        campos = self.driver.find_elements(*self.DATAS)
        self._preencher_data(campos[0], entrada)
        self._preencher_data(campos[1], saida)
        self.clicar(self.VERIFICAR)

    def datas_exibidas(self):
        return [c.get_attribute("value") for c in self.driver.find_elements(*self.DATAS)]

    def aviso_validacao(self, timeout=5):
        return self.texto_se_aparecer(self.AVISO, timeout)

    def quantidade_links_reserva(self):
        return len(self.driver.find_elements(*self.LINKS_RESERVA))
