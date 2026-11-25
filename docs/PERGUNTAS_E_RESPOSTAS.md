# Perguntas prováveis na apresentação

Material de preparação do Grupo 4. As respostas se apoiam nos arquivos do projeto.

**1. Por que vocês automatizaram esses cinco casos e não outros?**
CT01, CT03, CT05, CT07 e CT08 cobrem os três fluxos e as duas técnicas obrigatórias, e o CT05 é o de maior risco (RP1). Os demais ficaram manuais por motivos diferentes:
- CT02 cai na mesma partição de saída do CT03;
- CT04 exige digitar 2000 caracteres;
- CT06 está bloqueado pelo DEF01;
- CT09 e CT10 dependem de premissas.

Ver relatório, seção 3.1.

**2. O que é o Page Object Model e onde ele aparece no código?**
É uma classe por página que concentra os seletores e as ações, como `ContactPage.enviar(...)`. Se o site mudar um id, a correção é feita em `pages/`, sem mexer em cada teste.

**3. Como vocês escolheram os valores-limite do telefone?**
O próprio sistema informa a regra: "Phone must be between 11 and 21 characters." Testamos o último inválido e o primeiro válido de cada lado: 10, 11, 21 e 22. Ver `tests/test_ct03_telefone_valor_limite.py`, que usa parametrize.

**4. O CT05 falha. Vocês não deveriam corrigir o teste?**
Não. O teste exige um aviso que o sistema não exibe. Alterar a asserção esconderia o DEF02.

**5. Qual a diferença entre o CT05 reprovado e o CT06 bloqueado?**
- No CT05, os passos foram executados e o resultado divergiu do esperado.
- No CT06, a página de reserva não carregou (DEF01), e os passos de reservar nem puderam ser executados.

Por isso, o CT06 fica fora do denominador da métrica M1.

**6. Por que consulta e exclusão de quartos são um defeito só (DEF01)?**
As duas falham na mesma rota, `/api/room/{id}`, com HTTP 500, em métodos diferentes (GET e DELETE). Contá-las separadamente seria duplicidade. O relatório descreve os dois sintomas.

**7. Por que OBS01 e OBS02 não contam como defeitos confirmados?**
Eles dependem de regras que o site não documenta. A P1 é que o telefone deve ter dígitos; a P2 é que o número do quarto é único. São premissas do grupo, e não requisitos oficiais. Por isso, aparecem à parte na métrica M3.

**8. Por que o RS01 é um risco e não um defeito?**
Cinco senhas erradas não causaram bloqueio, mas o sistema não declara um limite de tentativas. É uma boa prática recomendada pela OWASP, e isso sozinho não comprova a violação de um requisito.

**9. Como se calcula a M1?**
É aprovados ÷ casos com veredito: 6 ÷ 9 = 66,7%. O bloqueado fica de fora. Sem os dois casos que dependem de premissas, o resultado seria 6 ÷ 7 = 85,7%.

**10. Como vocês diferenciam uma falha de rede de um defeito?**
A fixture `site_disponivel` (`conftest.py`) faz uma requisição com cabeçalho de navegador:
- se houver qualquer resposta HTTP, mesmo 403 ou 500, a suíte roda;
- só uma falha de DNS, de conexão ou tempo esgotado gera SKIP "AMBIENTE".

**11. Onde ficam as credenciais do admin?**
O CT08 usa as credenciais públicas de demonstração publicadas no README oficial do Restful Booker Platform. Elas podem ser trocadas pelo `.env`, que não é versionado.

**12. Quem é afetado pelo DEF03 e qual é o tamanho do problema?**
Os visitantes que enviaram mensagens. Nome e assunto ficam visíveis sem login, e o assunto pode conter informação pessoal. E-mail e telefone não apareceram nessa resposta. A recomendação correspondente é a R3.

**13. Por que usar WebDriverWait e não time.sleep?**
O sleep espera um tempo fixo, que pode ser curto demais ou lento demais. A espera explícita verifica uma condição e segue assim que ela é atendida. Ver `pages/base_page.py`.

**14. Qual foi o resultado da suíte automatizada?**
Na execução local de 25/11/2026 (17h28), o pytest coletou 8 itens: 7 PASSED, 1 FAILED e 0 SKIPPED. O FAILED é o CT05, que reproduziu o DEF02. A saída do terminal e o print estão em `evidencias/execucao/automatizada/`, e os relatórios HTML e JUnit em `relatorios_execucao/`.

**15. A primeira execução teve 6 falhas. O que aconteceu?**
Eram falhas da automação, não do site. O site usa rolagem suave (`scroll-behavior: smooth`), e o clique acontecia antes de o botão chegar à posição final (`ElementClickInterceptedException`). A correção foi fazer a rolagem instantânea em `BasePage.rolar_ate`, sem mudar nenhuma asserção. A tentativa original está guardada em `evidencias/execucao/automatizada/tentativa1_antes_da_correcao/`.

**16. Como a IA foi usada?**
Ver a declaração de uso de IA no fim do relatório.
