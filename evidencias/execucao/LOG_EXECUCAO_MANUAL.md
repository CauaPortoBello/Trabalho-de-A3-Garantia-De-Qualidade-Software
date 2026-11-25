# Registro da execução manual dos casos de teste

- **Sistema:** Restful Booker Platform v2.2, em https://automationintesting.online
- **Datas:** 25/11/2026, em duas sessões: manhã (08h52 às 09h10) e tarde (16h45 às 16h56), horário de Brasília.
- **Navegador:** Google Chrome (Windows).
- **Forma de execução:** execução manual assistida por ferramenta de IA no navegador (ver a declaração de uso de IA no relatório). As mensagens foram copiadas literalmente da tela e os códigos HTTP foram lidos no painel de rede do navegador.
- **Dados:** somente fictícios. Nomes usados: "Ana Exemplo", "Maria Teste", "Joao Ficticio" e "Hospede Ficticio"; e-mails no domínio `exemplo.com`.
- **Natureza das evidências:** **[captura]** captura da interface, arquivo em `evidencias/`; **[HTTP]** código de resposta observado no painel de rede; **[texto]** texto exibido na tela, transcrito neste registro.

> **Correção de registro.** Uma versão anterior deste log atribuía ao CT01 um envio de "Ana Exemplo" que, na verdade, tinha telefone com letras. O CT01 foi executado exatamente como especificado na sessão da tarde (seção 1, linha 1).

## 1. Formulário de contato

Seletores: `#name`, `#email`, `#phone`, `#subject`, `#description` e o botão "Submit".

| # | Sessão | Entrada | Resultado exibido pelo sistema | Caso | Status | Evidência |
|---|---|---|---|---|---|---|
| 1 | Tarde, 16h54 | Ana Exemplo; ana.exemplo@exemplo.com; 11987654321; "Duvida sobre reserva"; "Gostaria de saber se a pousada aceita animais." (46 caracteres) | "Thanks for getting in touch Ana Exemplo!" e o assunto repetido | CT01 | Aprovado | [captura] `execucao/CT01_confirmacao_ana_exemplo.jpg` |
| 2 | Manhã | Todos os campos vazios | Mensagens de validação que revelam os limites: telefone de 11 a 21 caracteres, assunto de 5 a 100 e mensagem de 20 a 2000 | exploração | — | [texto] |
| 3 | Manhã | Maria Teste, e-mail `maria.teste` | "must be a well-formed email address"; nada enviado | CT02 | Aprovado | [texto] |
| 4 | Manhã | Ana Exemplo, e-mail `ana.exemplo` | "must be a well-formed email address"; nada enviado | CT02 | Aprovado | [captura] `execucao/CT02_email_invalido_erro.jpg` |
| 5 | Manhã | Telefone com 10 caracteres | "Phone must be between 11 and 21 characters." | CT03 | Aprovado | [texto] |
| 6 | Manhã | Telefone com 22 caracteres | "Phone must be between 11 and 21 characters." | CT03 | Aprovado | [texto] |
| 7 | Manhã | Joao Ficticio; telefone com 11, assunto com 5 e mensagem com 20 caracteres | "Thanks for getting in touch Joao Ficticio!" | CT03, CT04 | Aprovado | [texto] |
| 8 | Manhã | Joao Ficticio; telefone com 21, assunto com 100 e mensagem com 2000 caracteres | "Thanks for getting in touch Joao Ficticio!" | CT03, CT04 | Aprovado | [texto] |
| 9 | Manhã | Assunto com 4 e com 101 caracteres (um envio para cada) | "Subject must be between 5 and 100 characters." | CT04 | Aprovado | [texto] |
| 10 | Manhã | Mensagem com 19 e com 2001 caracteres (um envio para cada) | "Message must be between 20 and 2000 characters." | CT04 | Aprovado | [texto] |
| 11 | Manhã | Maria Teste, telefone `abcdefghijkl` | "Thanks for getting in touch Maria Teste!" (mensagem aceita) | CT09 | Reprovado sob a premissa P1 | [texto] |
| 12 | Manhã | Ana Exemplo, telefone `abcdefghijkl` | Mensagem aceita | CT09 (repetição) | Reprovado sob a premissa P1 | [texto] |
| 13 | Tarde, 16h55 | Maria Teste; maria.teste@exemplo.com; telefone `abcdefghijkl`; demais campos válidos | "Thanks for getting in touch Maria Teste!" | CT09 (repetição) | Reprovado sob a premissa P1 | [captura] `defeitos/OBS01_a_…` (campos preenchidos, sem alerta) e `defeitos/OBS01_b_…` (confirmação) |

**Mensagens sem autenticação (DEF03):**
- Pela manhã, `GET /api/message` feito **sem cookies** respondeu **200**, com a lista de mensagens contendo apenas os campos `id`, `name`, `read` e `subject` [HTTP].
- Às 16h45, o mesmo pedido respondeu **200** novamente [HTTP].
- Na mesma condição, `GET /api/booking` e `GET /api/report` responderam **401** [HTTP].
- A rota de detalhe `GET /api/message/1` respondeu **500** com e sem sessão, então não foi possível verificar se ela expõe outros dados.

## 2. Reserva por datas

| # | Sessão | Ação | Observado | Caso | Status | Evidência |
|---|---|---|---|---|---|---|
| 1 | Manhã | Página inicial, "Book now" do quarto 1 (entrada 10/12/2026, saída 11/12/2026) | Indicador de carregamento contínuo, sem conteúdo; console: `SyntaxError: Unexpected token 'I', "Internal S"... is not valid JSON`; `GET /api/room/1` → **500** | CT06 | Bloqueado (DEF01) | [captura] `defeitos/DEF01_…` e [HTTP] |
| 2 | Manhã | `GET /api/room/1`, `/2` e `/3`; `GET /api/room` (lista) | **500** nos três quartos; **200** na lista | CT06 | — | [HTTP] |
| 3 | Manhã, depois do reinício automático do site | `GET /api/room/1` | **500** | CT06 | — | [HTTP] |
| 4 | Tarde, 16h45 e 16h56 | Mesma página de reserva; `GET /api/room/1` e `/2` | Carregamento contínuo; **500** | CT06 | Bloqueado (DEF01) | [HTTP] |
| 5 | Manhã | Check In 12/12/2026, Check Out 10/12/2026, "Check Availability" | Nenhum aviso; os 3 quartos continuam com "Book now", com links para entrada 2026-12-12 e saída 2026-12-10 | CT05 | Reprovado (DEF02) | [captura] `defeitos/DEF02_…` |
| 6 | Tarde, 16h56 | Repetição do item 5 | Nenhum aviso no bloco de reserva; 3 links "Book now" | CT05 | Reprovado (DEF02) | [texto] |
| 7 | Manhã | `GET /api/room` com entrada posterior à saída | **200**, com 3 quartos | CT05 | — | [HTTP] |
| 8 | Manhã | `POST /api/booking`, quarto 3, entrada 2027-03-12, saída 2027-03-10 | **409** `{"error":"Failed to create booking"}` | Complementar | Servidor recusa | [HTTP] |
| 9 | Manhã | `POST /api/booking`, entrada igual à saída (2027-03-20) | **409** | Complementar | Servidor recusa | [HTTP] |
| 10 | Manhã | `POST /api/booking`, entrada 2027-03-25, saída 2027-03-26 (uma noite) | **201**, `bookingid: 4` | Complementar | Servidor aceita | [HTTP] |
| 11 | Manhã | `DELETE /api/booking/4` (limpeza) | **500**; a reserva de teste não pôde ser removida | Limpeza | — | [HTTP] |

## 3. Painel administrativo

Seletores: `#username`, `#password`, `#doLogin`, `#roomName`, `#type`, `#accessible`, `#roomPrice`, `#createRoom`, `[data-testid=roomlisting]` e `span.roomDelete`.

| # | Sessão | Ação | Observado | Caso | Status | Evidência |
|---|---|---|---|---|---|---|
| 1 | Manhã | Usuário `admin`, senha `senhaErrada123` | "Invalid credentials"; a página permanece em `/admin` | CT07 | Aprovado | [captura] `execucao/CT07_…` |
| 2 | Manhã | 5 tentativas seguidas com senha errada (`tentativa1` a `tentativa5`) | "Invalid credentials" nas 5 | Exploratório | — | [texto] |
| 3 | Manhã | Login com a credencial de demonstração pela API (`POST /api/auth/login`), logo depois das 5 falhas | **200**; nenhum bloqueio ou atraso observado | Exploratório | Risco RS01 | [HTTP] |
| 4 | Manhã | Criar quarto com todos os campos vazios | "Failed to create room" | Exploratório | — | [texto] |
| 5 | Manhã | Criar quarto com preço −50 e com preço 0 | "must be greater than or equal to 1" | Exploratório | — | [texto] |
| 6 | Manhã | Criar quarto T408, Double, acessível, 180, WiFi | Linha "T408 / Double / true / 180 / WiFi" listada | CT08 | Aprovado | [texto] |
| 7 | Tarde, 16h55 | Criar quarto T501, Double, acessível, 180, WiFi | Linha "T501 / Double / true / 180 / WiFi" listada | CT08 | Aprovado | [captura] `execucao/CT08_quarto_T501_criado.jpg` |
| 8 | Manhã | Criar quarto "101" (número existente), preço 120 | Aceito; a lista passa a ter dois quartos "101" | CT10 | Reprovado sob a premissa P2 | [texto] |
| 9 | Manhã, depois do reinício do site | Repetição do item 8 | Aceito novamente | CT10 | Reprovado sob a premissa P2 | [captura] `defeitos/OBS02_…` |
| 10 | Manhã | Excluir os quartos criados (ícone ×) | `DELETE /api/room/4` e `/5` → **500**; nenhuma mensagem na tela; as linhas continuam listadas | DEF01 (sintoma B) | — | [HTTP] |
| 11 | Tarde, 16h55 | Excluir T501 (id 8) | `DELETE /api/room/8` → **500**; a linha continua listada; nenhuma mensagem | DEF01 (sintoma B) | — | [HTTP] |

## 4. Credenciais de demonstração

O README oficial do projeto (`github.com/mwinteringham/restful-booker-platform`, seção "Login") publica o usuário `admin` e a senha `password`. Elas são credenciais públicas de um ambiente de treino, não contas pessoais.
