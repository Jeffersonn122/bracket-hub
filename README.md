# Bracket Hub

**Integrante(s): Anderson Kayque e Jefferson Gabriel**

## Projeto: Bracket Hub

## 1. Visão Geral

Uma plataforma de gerenciamento e inscrição para torneios de eSports e jogos de luta, utilizando na sua criação com base com python para suas funções de conectar jogadores, organizadores e espectadores, automatizando desde o chaveamento e registro de participantes até a confirmação de partidas e relatórios de resultados.

## 2. Requisitos Funcionais (RF)

**RF01 – Autenticação e Cadastro de Usuário:** O sistema deve permitir que o usuário realize cadastro informando nome completo, nickname (gamertag), e-mail e senha, bem como login utilizando e-mail e senha. O e-mail deve ser único no sistema.

**RF02 – Visualização de Torneios Disponíveis (Home):** A página inicial deve exibir uma grade de torneios ativos com informações como: nome, jogo, plataforma, código de convite, vagas disponíveis e status das inscrições. Deve ser possível filtrar os torneios por nome do jogo e por texto de busca.

**RF03 – Criação de Torneios:** Qualquer usuário autenticado pode criar um novo torneio informando: nome do torneio, jogo (selecionado de uma lista pré-cadastrada), código de acesso e limite de vagas. O torneio deve aparecer imediatamente na lista de torneios disponíveis.

**RF04 – Detalhes e Inscrição:** Exibição das informações do torneio e formulário para adicionar jogadores manualmente. Competidores: Lista de participantes inscritos, com opção de remoção e exportação para CSV. Chaveamento (Double Elimination): Visualização da árvore de dupla eliminação (Winners, Losers e Grand Final), com campos para reportar placares. Disputas: Mediação de conflitos de placar (estrutura presente, mas com funcionalidade simulada). Overlay OBS: Geração de link para sobreposição em transmissão ao vivo.

**RF05 – Geração Automática de Chaveamento:** O organizador deve poder gerar um chaveamento de dupla eliminação a partir da lista de jogadores inscritos. O sistema deve distribuir os participantes na chave superior (Winners Bracket) e automaticamente organizar a chave inferior (Losers Bracket) e a Grande Final.

**RF06 – Registro de Resultados e Propagação na Chave:** O organizador deve poder registrar o placar de uma partida (sets). Ao finalizar uma partida, o sistema deve:

- Declarar o vencedor e o perdedor.
- Propagar o vencedor para a próxima fase da chave superior ou final.
- Propagar o perdedor para a chave inferior (repescagem).
- Atualizar automaticamente os confrontos subsequentes.

**RF07 – Regra de Bracket Reset na Grande Final:** Se o competidor vindo da chave inferior (Losers) vencer a primeira Grande Final, o sistema deve automaticamente gerar uma partida extra (Bracket Reset) para definir o campeão absoluto.

**RF08 – Loja de Eventos:** O sistema deve disponibilizar uma seção "Loja" exibindo itens temáticos com nome, preço e imagem. O usuário pode clicar em "Adicionar à Sacola" (ação simulada).

**RF09 – Suporte e FAQ:** O sistema deve conter uma seção de suporte com informações básicas de ajuda, acessível pelo menu lateral.

**RF10 – Seleção de Idioma (Internacionalização):** O menu lateral deve conter um seletor de idioma com opções "Português (BR)" e "English (US)". A funcionalidade de troca imediata de idioma não está implementada, apenas o seletor visual.

**RF11 – Exportação de Lista de Participantes:** O organizador deve poder exportar a lista de participantes inscritos em um torneio para um arquivo CSV contendo Seed e GamerTag.

## 3. Modelo Entidade-Relacionamento

O diagrama ER do sistema esta disponivel no arquivo:

[bracket-hub.pdf](./bracket-hub.pdf)
