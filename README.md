# p4join


## Executando os containers para teste

### Subindo os containers

```bash
docker compose build
docker compose up -d
```

### Acessando os container
```bash
# Acessando o sender
docker exec -ti sender bash

# Acessando o receiver
docker exec -ti receiver bash
```

Com acesso aos containers, é possível executar o scripts `send.py` para ler o
arquivo `lineorder.csv`, e enviar o conteúdo de cada linha como um frame
ethernet.
Só deve modificar o MAC destino do script, para que seja o de receiver.

E em outro container se executa o script `recv.py` pra sniffar a interface de
rede padrão, e monitorar o que chega.


## Links úteis
- Pisa arch: https://sdn.systemsapproach.org/switch.html