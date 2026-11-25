# A3 — Garantia da Qualidade de Software · Grupo 4 · Restful Booker Platform

Trabalho A3 da unidade curricular **Garantia da Qualidade de Software**, Universidade São Judas Tadeu, Prof. Leandro Negreiros, 2026/2.


## Objetivo

Avaliar a qualidade de um sistema web real, atuando como equipe de QA. O trabalho inclui:

- plano de testes;
- especificação de casos com partição de equivalência e análise de valor-limite;
- automação de cinco cenários com Selenium e pytest;
- registro de defeitos e cálculo de métricas;
- análise ética dos impactos sobre as pessoas afetadas.

## Sistema avaliado

O [Restful Booker Platform](https://github.com/mwinteringham/restful-booker-platform) é uma aplicação de código aberto criada para treino de automação de testes. A instância pública https://automationintesting.online (v2.2) simula a pousada fictícia *Shady Meadows B&B*. O site é reiniciado periodicamente.

Fluxos avaliados:

1. formulário de contato;
2. reserva de quarto por datas;
3. painel administrativo (`/admin`): login e gestão de quartos.

Ficaram fora do escopo os testes de carga e estresse, outros sites e outros navegadores. Todos os dados usados são fictícios.

## Tecnologias

Versões usadas na execução local de 25/11/2026 (Windows 11):

| Ferramenta | Versão |
|---|---|
| Python | 3.12.4 |
| Selenium | 4.54.0 (o Selenium Manager baixa o chromedriver automaticamente) |
| pytest | 9.2.0 |
| pytest-html | 4.2.0 |
| Google Chrome | 158.0.8127.38 |

## Estrutura do projeto

```text
A3-Garantia-Qualidade-Software/
├── README.md
├── REFERENCIAS.md
├── requirements.txt          dependências
├── pytest.ini                configuração do pytest (relatório HTML e JUnit)
├── conftest.py               URL, credenciais de demonstração, navegador, conectividade e prints
├── verificar_ambiente.py     checagem do ambiente antes da execução
├── .env.example              modelo opcional para mudar URL, modo headless ou credenciais
├── .gitignore
├── pages/                    Page Objects: contact_page, booking_page, admin_page
├── tests/                    os 5 testes automatizados
├── docs/
│   ├── relatorio_A3.docx     relatório (editável)
│   ├── relatorio_A3.pdf      relatório (versão de entrega)
│   ├── grafico_metricas.png  gráfico usado no relatório
│   └── PERGUNTAS_E_RESPOSTAS.md
├── slides/
│   ├── apresentacao_A3.pptx
│   └── apresentacao_A3.pdf
├── evidencias/
│   ├── execucao/             log da execução manual e capturas dos casos aprovados
│   │   └── automatizada/     saída e print do terminal da execução final + 1ª tentativa
│   ├── screenshots/          prints gerados pelo pytest na execução final
│   └── defeitos/             capturas dos defeitos, observações e reverificação HTTP
└── relatorios_execucao/      relatório HTML e JUnit XML da execução final
```

As pastas `relatorios_execucao/` e `evidencias/screenshots/` são regravadas a cada execução do pytest. As versões publicadas são as da execução final de 25/11/2026.

## Testes automatizados

| Teste | Caso | O que verifica | Técnica |
|---|---|---|---|
| `test_ct01_contato_valido.py` | CT01 | Contato com todos os campos válidos exibe "Thanks for getting in touch Ana Exemplo!" | Partição de equivalência |
| `test_ct03_telefone_valor_limite.py` | CT03 | Telefone com 10 e 22 caracteres é recusado; com 11 e 21, aceito (4 execuções parametrizadas) | Valor-limite |
| `test_ct05_reserva_datas_invertidas.py` | CT05 | A busca com saída anterior à entrada deve exibir um aviso | Partição de equivalência |
| `test_ct07_login_senha_incorreta.py` | CT07 | Senha incorreta exibe "Invalid credentials" e não abre o painel | Partição de equivalência |
| `test_ct08_admin_cria_quarto.py` | CT08 | Um quarto criado no painel aparece na lista com os dados informados | Teste funcional |

Os 10 casos especificados (CT01 a CT10) e seus resultados estão no capítulo 2 do relatório.

## Como executar no Windows (PowerShell)

1. Abra o PowerShell na pasta do projeto:

   ```powershell
   cd C:\caminho\para\A3-Garantia-Qualidade-Software
   ```

2. Crie e ative um ambiente virtual:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   Se o PowerShell bloquear a ativação, rode antes `Set-ExecutionPolicy -Scope Process RemoteSigned` (vale só para a janela atual).

3. Instale as dependências:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Verifique o ambiente. A saída deve terminar com `AMBIENTE OK`:

   ```powershell
   python verificar_ambiente.py
   ```

5. Execute os testes:

   ```powershell
   python -m pytest                       # todos os testes
   python -m pytest -k ct05               # um caso
   python -m pytest -m contato            # um fluxo: contato, reserva ou admin
   ```

### Configuração

Nenhuma configuração é obrigatória. O CT08 usa as **credenciais públicas de demonstração** publicadas no README oficial do Restful Booker Platform (seção "Login"). Não são contas pessoais.

Para mudar algum valor, copie o `.env.example` para `.env` (`copy .env.example .env`) e preencha o que quiser. As opções são:

- `HEADLESS=1`: executa o Chrome sem janela;
- `BASE_URL`: muda a URL testada;
- `ADMIN_USERNAME` e `ADMIN_PASSWORD`: usa outras credenciais.

O arquivo `.env` não é versionado.

## Resultados e evidências

Cada execução do pytest gera:

| Arquivo | Conteúdo |
|---|---|
| `relatorios_execucao/relatorio_pytest.html` | Relatório com o resultado de cada teste e o print embutido |
| `relatorios_execucao/junit.xml` | Resultado em formato JUnit |
| `evidencias/screenshots/` | Um print por teste, com `PASSOU` ou `FALHOU` no nome do arquivo |

### Resultado da execução automatizada (25/11/2026, 17h28, execução local)

| ID | Cenário | Resultado | Observação |
|---|---|---|---|
| CT01 | Contato com campos válidos | PASSED | Confirmação "Thanks for getting in touch Ana Exemplo!" |
| CT03 | Telefone com 10, 11, 21 e 22 caracteres | 4 PASSED | Limites 11 e 21 respeitados |
| CT05 | Saída anterior à entrada | **FAILED** | Nenhum aviso; 3 links "Book now". Reproduz o DEF02 |
| CT07 | Login com senha incorreta | PASSED | "Invalid credentials"; painel não abre |
| CT08 | Admin cria quarto | PASSED | Quarto listado; a exclusão de limpeza falhou (DEF01, sintoma B) |

Total: 8 itens coletados (o CT03 gera quatro), **7 PASSED, 1 FAILED, 0 SKIPPED**, em 77 s.

A primeira tentativa, às 17h21, teve 6 falhas causadas pela automação: o site usa rolagem suave e o clique acontecia no meio da rolagem (`ElementClickInterceptedException`). A rolagem passou a ser instantânea em `pages/base_page.py`, sem mudar nenhuma asserção. Os arquivos dessa tentativa estão guardados para consulta.

| Local | Conteúdo |
|---|---|
| `relatorios_execucao/relatorio_pytest.html` | Relatório HTML da execução final, com os prints embutidos |
| `relatorios_execucao/junit.xml` | Resultado da execução final em JUnit XML |
| `evidencias/screenshots/` | Um print por item de teste da execução final |
| `evidencias/execucao/automatizada/saida_pytest_execucao_final.txt` | Saída completa do terminal (verificação do ambiente + pytest) |
| `evidencias/execucao/automatizada/print_terminal_execucao_final.png` | Print real do terminal ao fim da execução |
| `evidencias/execucao/automatizada/tentativa1_antes_da_correcao/` | Saída, relatórios e prints da 1ª tentativa |
| `evidencias/defeitos/reverificacao_http_20261125.txt` | Reverificação, só com GET, de DEF01 e DEF03 às 17h30 |

### Evidências da execução manual (histórico, 25/11/2026)

| Local | Conteúdo |
|---|---|
| `evidencias/execucao/LOG_EXECUCAO_MANUAL.md` | Registro de cada execução, indicando a natureza da evidência (captura, HTTP ou texto) |
| `evidencias/execucao/` | Capturas de CT01, CT02, CT07 e CT08 |
| `evidencias/defeitos/` | Capturas de DEF01, DEF02, OBS01 e OBS02 |

### Como ler os status

| Status | Onde aparece | Significado |
|---|---|---|
| **PASSED** | pytest | O teste rodou e a asserção foi satisfeita |
| **FAILED** | pytest | O teste rodou e a asserção falhou. Pode ser um defeito do sistema (como o CT05) ou um erro da automação; a mensagem indica qual |
| **SKIPPED** | pytest | O teste não rodou. Com o motivo `AMBIENTE`, não houve conexão com o site (DNS, rede ou tempo esgotado). Qualquer resposta HTTP, mesmo 403 ou 500, conta como site alcançado e não gera SKIP |
| **Aprovado / Reprovado** | relatório (execução manual) | O caso foi executado manualmente e o resultado correspondeu, ou não, ao esperado |
| **Bloqueado** | relatório (execução manual) | Um defeito em outra parte do sistema impediu executar os passos do caso (CT06). Não equivale a FAILED |

Os resultados manuais e os automatizados são registrados separadamente.

**Comportamento esperado:** na execução manual, o site não exibiu aviso para datas invertidas (DEF02). Por isso, o **CT05 deve terminar como FAILED** enquanto o defeito existir. É um achado do trabalho, e a asserção não deve ser alterada para passar.

## Situação da validação

- A execução manual dos 10 casos foi feita em 25/11/2026, com apoio de IA no navegador, e está registrada no log.
- A suíte automatizada foi executada localmente contra o site em 25/11/2026, com os resultados da tabela acima.
- O `verificar_ambiente.py` distingue falha de DNS, falha de conexão, tempo esgotado e respostas HTTP (normal, 403, 500).

## Achados

**Defeitos confirmados**

| ID | Defeito | Fluxo | Severidade |
|---|---|---|---|
| DEF01 | API de quartos por ID responde HTTP 500: a página de reserva não carrega e a exclusão de quartos falha sem aviso | Reserva (também afeta o Admin) | Crítica |
| DEF02 | A busca de disponibilidade aceita saída anterior à entrada, sem aviso. A API de reserva recusa essas datas (409) | Reserva | Média |
| DEF03 | `GET /api/message` sem autenticação lista nome e assunto de todas as mensagens | Contato | Média |

**Observações condicionadas a premissas e risco de segurança**

| ID | Observação | Fluxo |
|---|---|---|
| OBS01 | Telefone sem dígitos é aceito (premissa P1: o telefone deve conter dígitos) | Contato |
| OBS02 | Número de quarto duplicado é aceito (premissa P2: o número do quarto é único) | Admin |
| RS01 | Cinco senhas incorretas seguidas sem bloqueio observado (boa prática, sem requisito explícito no site) | Admin |

## Relatório, apresentação e referências

- Relatório: `docs/relatorio_A3.pdf` (editável em `docs/relatorio_A3.docx`)
- Apresentação: `slides/apresentacao_A3.pptx` e `slides/apresentacao_A3.pdf`
- Referências: `REFERENCIAS.md`
- Preparação para perguntas: `docs/PERGUNTAS_E_RESPOSTAS.md`

## Limitações conhecidas

- O site é público e reiniciado periodicamente, e seu comportamento pode mudar. Os testes não dependem de dados criados em outro dia: o CT08 gera um número de quarto novo a cada execução.
- Por causa do DEF01, o quarto criado pelo CT08 não é excluído e permanece até o próximo reinício do site. O teste não depende da exclusão.
- O CT06 não foi automatizado, porque a página de reserva não carrega (DEF01).
- Os campos de data usam o componente react-datepicker. O teste digita a data como um usuário. Se o navegador não repassar o atalho Ctrl+A, o teste aplica o valor pelo evento de entrada do React (`pages/booking_page.py`).

## Integrantes — Grupo 4

| Nome | RA |
|---|---|
| Cauã Porto Bello | 312510332 |
| Douglas Pozenato Junior | 312512280 |
| Henryco Meneghetti de Queiróz | 312512176 |
| Lucas da Silva Cavalcante | 312621165 |
| Matheus Fioruci | 312510854 |
| Yasmin Morais Silva | 312512177 |
