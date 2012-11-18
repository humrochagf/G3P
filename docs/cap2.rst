Para a elaboração do aplicativo será necessário uma série de informações as quais serão descritas a seguir.

Descrição do Problema
=====================
Uma loja de festas infantis quer implementar um sistema automatizado para gerenciar seus produtos e pedidos bem como interagir de forma mais dinâmica com seus parceiros oferecendo-os um meio onde possam fazer seus pedidos sem, necessariamente, estar em contato direto com algum encarregado da empresa. E, para isso, ela precisará armazenar uma série de dados.

Produto
-------
O produtos fornecidos pela loja possuem um série de características onde algumas estão presentes em todo produto e outras não. 

As características presentes em todo produto são:

- Código para identifica-lo;

- Título que descreve o produto;

- Preço;

- Tipo, do qual o produto se enquadra ao ser criado, podendo ser de aluguel ou venda;

Parceiro
--------
É o usuário do sistema e responsável por efetuar os pedidos. Sobre ele guarda-se:

- Código para identifica-lo;

- Nome;

- E-mail;

- login;

- Senha;

Pedido
------
É efetuado pelos parceiros sendo o responsável por intermediar o relacionamento deles com os produtos da loja. Sobre ele é guardado:

- Código que o identifica;

- Data em que o pedido foi feito;

- Data de saída do pedido;

- Data de retorno do pedido em caso de produtos alugados;

- Status que indica se o pedido foi aprovado ou não;

- Comentários.

Um parceiro pode fazer diversos pedidos podendo nele conter um ou mais produtos.

Pagamento
---------
Os pagamentos feitos pelos parceiros são registrados pelo gerente da loja, sendo guardado sobre eles:

- Código que o identifica;

- Data em que o pagamento foi efetuado;

- Valor;

- Número do cheque em caso de pagamento em cheque;

- Número do depósito em caso de débito em conta;

- Data do depósito em caso de débito em conta;

- Banco em caso de pagamento em cheque ou débito em conta;

- Titular da conta em caso de pagamento em cheque ou débito em conta.

Descontos
---------
Há a nececidade de se dar bonificações ou multas sobre pedidos sendo importante informar:

- Valor do desconto;

- Justificativa do desconto.

**Observação Importante:** A visão do gerente do sistema não está inclusa na modelagem pois o framework é quem cuidará da abstração da administração garantindo o foco total na resolução do problema.

Sentença de Posição do Produto
==============================
Este aplicativo pretende atender a esta loja em particular buscando trazer maior organização, segurança e eficiência em seus negócios.

+-----------------+------------------------------+
|**Para**         |loja de festas infantis       |
+-----------------+------------------------------+
|**Que**          |enfrenta dificuldades em      |
|                 |gerenciar seus parceiros.     |
+-----------------+------------------------------+
|**O G3P**        |é um gerenciador de produtos, |
|                 |parceiros e pedidos.          |
+-----------------+------------------------------+
|**Que**          |organiza dados, gerencia 	 |
|                 |seus parceiros e garante um   |
|                 |maior controle sobre seus     |
|                 |produtos e pedidos.           |
+-----------------+------------------------------+
|**Diferente de** |sistemas extremamente         |  
|                 |genéricos e complexos do      |
|                 |mercado.                      |
+-----------------+------------------------------+
|**Nosso produto**|busca a simplicidade e        |
|                 |especialização.               |
+-----------------+------------------------------+

Levantado o problema e a proposta de solução segue ao processo de pesquisa e métodos para a descrição tecnológica dos mesmos.
