Banco de Dados com Processos e Threads
O que é
Este projeto simula um sistema de gerenciamento de banco de dados utilizando processos, threads e comunicação entre processos (IPC). O objetivo é demonstrar o uso de paralelismo e sincronização no acesso a dados.

Como funciona
O cliente é uma interface gráfica (feita com Tkinter) que permite o envio de comandos para o servidor.

O servidor escuta os comandos e cria uma thread para cada requisição.

Cada thread executa a operação no banco de dados SQLite.

O acesso ao banco é protegido com mutex (threading.Lock) para evitar conflitos quando várias threads tentam acessar o banco ao mesmo tempo.

Todas as operações realizadas são salvas em um arquivo de log (log.txt) e exibidas em tempo real na interface do cliente.

Comandos aceitos
Comando	Descrição	Exemplo
INSERT	Insere um novo registro	INSERT id=1 nome='João'
SELECT	Busca um registro pelo id	SELECT id=1
UPDATE	Atualiza o nome de um registro pelo id	UPDATE id=1 nome='Carlos'
DELETE	Remove um registro pelo id	DELETE id=1
Como executar
Abra o terminal na pasta onde está o projeto.

Execute o servidor com:

nginx
Copiar
Editar
python servidor.py
Isso abrirá a interface do cliente automaticamente.

Digite os comandos no campo de texto e pressione "Enviar".

O log das operações será exibido na parte inferior da interface.

Tecnologias utilizadas
Python

Tkinter (interface gráfica)

SQLite (banco de dados)

threading.Thread (threads)

threading.Lock (mutex)

multiprocessing.Pipe (comunicação entre processos)

Objetivos do projeto
Simular o comportamento de um sistema de banco de dados com processamento paralelo.

Utilizar conceitos de IPC, concorrência, sincronização e persistência de dados.

Demonstrar o uso de processos e threads de forma segura e eficiente.
