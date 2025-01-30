# Tarefas

## Tarefa 1:
Uma otima noticia é que a Intel abriu o P4Studio. Aquela pilha de software que eu tinha assinado NDA com eles.  O link ta aqui: https://github.com/p4lang/open-p4studio

Se puder instalar e tenta rodar tudo, tenta o exemplo mais simples que é o forward de pacote. No dia 31 estou de volta das ferias e podemos sentar se voce tiver problemas. Hoje à noite vou incluir aquela VM com toda a pilha naquele teu diretório.

## Tarefa 2
Essa tarefa é independente da anterior. A tarefa é enviar um pacote de rede entre duas maquinas do DINF mesmo, sem o switch P4 para se familiarizar com a biblioteca scappy do python. 
Usando o Scappy, tente enviar um registro de BD entre duas máquinas. Vamos assumir que cada registro de BD é um pacote de rede. Por ex. maquina A envia 1 registro do BD pra maquina B. Anexei no email um exemplo de codigo (sniff e send pkt).
Maquina A executa o send enquanto a maquina B executa o sniff.

## Tarefa 3
Vamos usar no nosso trabalho o SSB benchmark: https://www.cs.umb.edu/~poneil/StarSchemaB.PDF
Inicialmente, crie na mão no scappy 1 ou 2 registros no formato da tabela LINEORDER. Hard-coded no scappy e rexecuta a Tarefa 2.

## Tarefa 4
Essa tarefa é gerar dados do SSB benchmark. Achei esse cara aqui que diz gerar: https://github.com/electrum/ssb-dbgen
Por enquanto gera uma escala pequena pra usarmos nos nossos experimentos iniciais (0.01 GB?)

## Tarefa 5
Essa tarefa é uma atualização das tarefas 2 e 3. A tarefa é enviar um arquivo CSV inteiro de uma maquina pra outra, pode ser o CSV da tabela LINEORDER. Para cada registro do CSV, voce monta um pacote. Como falamos, assumimos que cada registro do BD é um pacote de rede.
Anexei no email um exemplo de codigo (sniff e send CSV e multiple table). Da uma olhada e melhorada no codigo se precisar.

## Tarefa 6
Idem da tarefa 2, mas agora dentro do simulador P4 entre duas virtual ethernets. 

## Tarefa 7
Idem da tarefa 5, mas agora dentro do simulador P4 entre duas virtual ethernets. 