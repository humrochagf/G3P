Para a elaboração do aplicativo será necessário uma série de informações das quais serão descritas a seguir.

Descrição do Problema
=====================
Uma loja de festas infantis quer implementar um sistema automatizado para gerenciar seus produtos e pedidos bem como interagir de forma mais dinâmica com seus parceiros oferecendo-os um meio onde possam fazer seus pedidos sem necessariamente estar em contato direto com algum encarregado da empresa. E para isso ela precisará armazenar uma série de dados.

Produto
-------
O produtos fornecidos pela loja possuem um série de características onde algumas estão presentes em todo produto e outras não. 

As características presentes em todo produto são:

- Código para identifica-lo;

- Preço;

- Categoria a qual o produto se enquadra ao ser criado, sendo ele enquadrado em somente uma que é pré definida e pode se referir a outros produtos. As categorias são 3, aluguel, venda e composto;

- Tipo do produto. Por exemplo se ele é um painel, uma vela, uma toalha, etc. Podem haver vários produtos de um mesmo tipo.

As demais não são características de todo produto e são elas :

- Tema, onde nem todo produto o possui, mas caso possua será somente um, tendo este tema a possibilidade de se referir a outros produtos;

- Cor, onde nem todo produto a possui, mas caso possua será somente uma, tendo esta cor a possibilidade de se referir a outros produtos;

- Estoque que é uma característica de produtos da categoria aluguel.

Existem determinados produtos que se encaixam em uma determinada categoria (categoria "composto") que é um produto do qual é fruto de uma composição de outros produtos e possui sua própria instância. Este produto pode ser resultado da junção de vários produtos e um produto ligado a ele pode estar ligado a outro produto desta categoria.

Parceiro
--------
É o usuário do sistema e responsável por efetuar os pedidos. Sobre ele guarda-se:

- Código para identifica-lo;

- E-mail do usuário responsável por exercer a função de login no sistema;

- Nome do parceiro;

- Senha;

- Endereço;

- Telefone do parceiro, composto por numero e tipo, podendo o parceiro possuir mais de um, dês de que distintos, sendo ligados a obrigatoriamente um e somente um parceiro onde em caso de exclusão do mesmo não há necessidade de mantê-lo;

Pedido
------
É efetuado pelos parceiros sendo o responsável por intermediar o relacionamento deles com os produtos da loja. Sobre ele é guardado:

- Código que o identifica;

- Data em que o pedido foi feito;

- Data de saída do pedido;

- Data de retorno do pedido em caso de produtos alugados;

- Status que indica se o pedido foi aprovado ou não;

- Comentários.

Todo pedido é feito por apenas um parceiro, mas este parceiro pode fazer diversos pedidos.

Um produto pode estar em vários pedidos e um pedido pode conter vários produtos,  dês de que uma ocorrência de cada produto apareça somente uma vez por pedido guardando sua quantidade.

Balanço e Pagamento
-------------------
O balanço é um fechamento feito todo mês para cada parceiro individualmente onde se pega todos os pedidos entregues daquele mês (dados como débito) somados aos pagamentos realizados referentes àquele balanço (dados como crédito) somados ao saldo anterior àquele balanço. Sobre ele guarda-se:

- Código que o identifica;

- Data sempre referente ao primeiro dia do mês a que se refere;

- Saldo anterior.

Um balanço deve ser vinculado a um e somente um parceiro e um parceiro pode ter vários balanços.

Um pedido pode ser vinculado a no máximo um balanço e um balanço pode ter vários pedidos.

O pagamento é feito referente à dívida acumulada no balanço (mas sem a obrigatoriedade de saná-la com precisão, dando margem para acumular crédito ou débito para o balanço seguinte) e pode ser feito em dinheiro, cheque ou débito em conta. Sobre ele guarda-se :

- Código que o identifica;

- Data em que o pagamento foi efetuado;

- Valor;

- Número do cheque em caso de pagamento em cheque;

- Número do depósito em caso de débito em conta;

- Data do depósito em caso de débito em conta;

- Banco em caso de pagamento em cheque ou débito em conta;

- Titular da conta em caso de pagamento em cheque ou débito em conta.

Um pagamento deve ser vinculado a um e somente um balanço e um balanço pode ter vários pagamentos.

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
|**Que**          |organiza seus dados, gerencia |
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
