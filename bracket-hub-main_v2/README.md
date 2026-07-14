# BRACKET.HUB - Tournament Management Suite

Sistema para gerenciamento de torneios de e-sports.

---

## COMO EXECUTAR O PROJETO - GUIA COMPLETO

### 1. Baixar o Projeto

Baixe o projeto como ZIP e extraia em uma pasta no seu computador.

### 2. Abrir o Terminal na Pasta do Projeto

Abra a pasta onde voce extraiu o projeto, clique na barra de enderecos da pasta, digite `cmd` ou no terminal do VSCode e pressione Enter. O terminal abrira dentro da pasta do projeto.

### 3. Criar Ambiente Virtual

No terminal, digite `python -m venv venv` e pressione Enter. Isso criara uma pasta chamada `venv` dentro do projeto.

### 4. Ativar Ambiente Virtual

No terminal, digite `venv\Scripts\activate` e pressione Enter. O terminal agora mostrara `(venv)` no inicio da linha, indicando que o ambiente virtual esta ativo.

### 5. Instalar Dependencias

No terminal, digite `pip install flask` e pressione Enter. Aguarde a instalacao ser concluida.

### 6. Configurar Banco de Dados

No terminal, digite `python reset_db.py` e pressione Enter. Isso criara o banco de dados com 42 jogos disponiveis, 8 torneios de exemplo, produtos na loja e um usuario administrador.

### 7. Iniciar o Servidor

No terminal, digite `python app.py` e pressione Enter. O servidor iniciara e mostrara a mensagem "Running on http://localhost:5005".

### 8. Acessar o Site

Abra seu navegador e digite `http://localhost:5005` na barra de enderecos. Mas também no proprio cmd/terminal dara um link pra ir direto ao site ex: `ttp://127.0.0.1:5005`
### 9. Fazer Login

No topo da pagina, clique em "Entrar / Cadastrar". Use as credenciais: E-mail: alan@gg.com, Senha: 123. Clique em "Acessar Plataforma" para entrar.

### 10. Explorar o Sistema

Agora voce pode criar torneios, adicionar participantes, gerar brackets, registrar placares, usar a loja e gerenciar seu perfil. Explore os menus laterais para conhecer todas as funcionalidades.

### 11. Sair do Sistema

Quando terminar, no terminal pressione `Ctrl+C` para parar o servidor. Depois digite `deactivate` e pressione Enter para desativar o ambiente virtual.

---

## PROBLEMAS E SOLUCOES

### Erro ao executar reset_db.py

Se aparecer "python: can't open file 'reset_db.py'", certifique-se de que o terminal esta na pasta correta do projeto.

### Porta 5005 em uso

Altere a porta no arquivo `app.py` na ultima linha: `app.run(debug=True, port=5006)`

### Erro ao instalar flask

Verifique se o ambiente virtual esta ativado. O terminal deve mostrar `(venv)` no inicio da linha.

### Os jogos nao aparecem na lista

Delete a pasta `database/` e execute `python reset_db.py` novamente.

### O carrinho da loja nao funciona

Limpe os cookies do seu navegador.

### O bracket nao gera

Tenha exatamente 2, 4, 8 ou 16 jogadores no torneio antes de gerar a chave.