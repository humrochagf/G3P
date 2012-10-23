Para a elaboração do aplicativo será necessário uma série de informações das quais serão descritas a seguir.

Descrição do Problema
=====================
A loja quer implementar um sistema automatizado para gerenciar seus produtos e pedidos bem como interagir de forma mais dinâmica com seus parceiros oferecendo-os um meio onde possam fazer seus pedidos sem necessariamente estar em contato direto com algum encarregado da empresa. E para isso ela precisará armazenar uma série de dados.

Produto
-------
O produtos fornecidos pela loja possuem um série de características onde algumas estão presentes em todo produto e outras não. 

As características presentes em todo produto são:

- Código (todo produto possui um código que o identifica );

- Preço;

- Categoria (todo produto ao ser criado deve se enquadrar em somente uma categoria pré definida e esta categoria pode se referir a vários produtos );

- Tipo (todo produto deve possuir somente um tipo, podendo este possuir vários produtos ou não ).

As demais não são características de todo produto e são elas :

- Tema (nem todo produto possui um tema, mas caso possua será somente um, tendo este tema a possibilidade de se referir a outros produtos );

- Cor (nem todo produto possui uma cor, mas caso possua será somente uma, tendo esta cor a possibilidade de se referir a outros produtos );

- Estoque (nem todo produto possui estoque, mas caso possua será somente um onde este determinado estoque se refere única e somente a este produto não tendo necessidade de armazená-lo em caso de exclusão deste produto).

Existem determinados produtos que se encaixam em uma determinada categoria (nomeada de “composto” para se referir a produtos compostos ) que é um produto do qual é fruto de uma composição de outros produtos e possui sua própria instância. Este produto pode ser resultado da junção de vários produtos e um produto ligado a ele pode estar ligado a outro produto desta categoria.

Parceiro
--------
É o usuário do sistema e responsável por efetuar os pedidos. Sobre ele guarda-se:

- E-mail (responsável por identificar o parceiro e exercerá a função de login no sistema );

- Nome (nome do parceiro);

- Senha;

- Endereço;

- Telefone (Sendo este composto por numero e tipo, podendo o parceiro possuir mais de um, dês de que distintos, sendo ligados a obrigatoriamente um e somente um parceiro onde em caso de exclusão do mesmo não há necessidade de mantê-lo );

Pedido
------
É efetuado pelos parceiros sendo o responsável por intermediar o relacionamento deles com os produtos da loja. Sobre ele é guardado:

- Código (que o identifica );

- Data de saída;

- Data de retorno;

- Status (que indica se o pedido foi aprovado ou não );

- Comentários.

Todo pedido deve ser feito obrigatoriamente por um e somente um parceiro, mas este parceiro pode fazer diversos pedidos guardando no processo o instante do pedido mantendo seu histórico.

Um produto pode estar em vários pedidos e um pedido pode conter vários produtos,  dês de que uma ocorrência de cada produto apareça somente uma vez por pedido guardando sua quantidade.

Balanço e Pagamento
-------------------
O balanço é um fechamento feito todo mês para cada parceiro individualmente onde se pega todos os pedidos entregues daquele mês (dados como débito ) somados aos pagamentos realizados referentes àquele balanço (dados como crédito ) somados ao saldo anterior àquele balanço. Sobre ele guarda-se:

- Código (que o identifica );

- Data (sempre referente ao primeiro dia do mês a que se refere );

- Saldo anterior.

Um balanço deve ser vinculado a um e somente um parceiro e um parceiro pode ter vários balanços.

Um pedido pode ser vinculado a no máximo um balanço e um balanço pode ter vários pedidos.

O pagamento é feito referente à dívida acumulada no balanço (mas sem a obrigatoriedade de saná-la com precisão, dando margem para acumular crédito ou débito para o balanço seguinte ) e pode ser feito em dinheiro, cheque ou débito em conta. Sobre ele guarda-se :

- Código (que o identifica nos três casos de pagamento);

- Data/hora (momento em que o pagamento foi efetuado nos três casos de pagamento );

- Valor (nos três casos de pagamento);

- Número do cheque (em caso de pagamento em cheque );

- Número do depósito (em caso de débito em conta );

- Data do depósito (em caso de débito em conta );

- Banco (em caso de pagamento em cheque ou débito em conta );

- Titular da conta (em caso de pagamento em cheque ou débito em conta ).

Um pagamento deve ser vinculado a um e somente um balanço e um balanço pode ter vários pagamentos.

Regras de negócios
------------------
Existem algumas regras que regem o funcionamento de sistema que não necessariamente são de responsabilidade do banco e são elas :

- Somente produtos da categoria “composto” são composição de outros produtos;

- Somente produtos da categoria aluguel possuem estoque;

- Ao fazer pedido de um produto da categoria aluguel deve-se fazer a checagem de sua disponibilidade em estoque para aquele período através do cruzamento de todos os pedidos que tenham interseção de data de saída/retorno com o do pedido a ser feito, sendo vetada a realização de pedidos indisponíveis em estoque;

- O produto composto funciona como um modelo, ao se fazer um pedido de produto composto deve se fazer a checagem de disponibilidade de todos produtos de aluguel que o compõem;

- Um pedido é permitido se houver uma diferença mínima de 24h entre a data de saída e a data de realização do pedido;

- Todo pedido concluído é submetido a aprovação do gerente do sistema;

- O parceiro pode adicionar, alterar e remover pedidos e consultar o balanço;

- Um pedido somete poderá ser alterado e removido por um parceiro com 24h de antecedência de sua data de saída;

- O gerente do sistema pode manter produtos, pedidos, balanço, parceiros e pagamentos.

**Observação Importante:** A visão do gerente do sistema não está inclusa na modelagem pois o framework é quem cuidará da abstração da administração garantindo o foco total na resolução do problema.

Sentença de Posição do Produto
------------------------------
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
