"""CT05 — Reserva com data de saída anterior à data de entrada é recusada.

Técnica: partição de equivalência (classe inválida: saída < entrada).
Critério de aceitação: CA3.

Na execução manual de 25/11/2026 o sistema NÃO exibiu aviso e manteve os
quartos com "Book now" (DEF02). Se este teste falhar, a falha deve ser mantida
e registrada no relatório — não altere a asserção para fazê-lo passar.
"""
from datetime import date, timedelta

import pytest

from pages.booking_page import BookingPage


@pytest.mark.reserva
def test_ct05_reserva_com_saida_antes_da_entrada_e_recusada(driver, base_url):
    entrada = date.today() + timedelta(days=30)
    saida = entrada - timedelta(days=2)
    entrada_txt, saida_txt = entrada.strftime("%d/%m/%Y"), saida.strftime("%d/%m/%Y")

    pagina = BookingPage(driver, base_url)
    pagina.buscar(entrada_txt, saida_txt)

    # Pré-condição do próprio teste: as datas inválidas precisam estar nos campos
    assert pagina.datas_exibidas() == [entrada_txt, saida_txt], (
        f"Não foi possível preencher as datas (problema de automação, não defeito): {pagina.datas_exibidas()}"
    )

    aviso = pagina.aviso_validacao()
    assert aviso is not None, (
        f"O sistema não exibiu aviso para saída ({saida_txt}) anterior à entrada ({entrada_txt}) "
        f"e continuou oferecendo {pagina.quantidade_links_reserva()} link(s) 'Book now'."
    )
