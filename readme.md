## Sobre

Cazador é um projeto desenvolvido em Python que atua como um scraper de sites de imóveis. O objetivo principal é coletar informações relevantes de páginas de imóveis e salvá-las em um banco de dados MongoDB para futuras consultas ou análises. Este projeto é especialmente útil para quem busca automatizar a coleta de dados em sites imobiliários, proporcionando uma maneira eficiente de acessar informações atualizadas sobre imóveis disponíveis.

## Funcionalidades

- _Atualização do Banco de Dados_: Através do endpoint /update, é possível disparar o processo de scraping que coleta dados dos sites configurados e os salva no banco de dados MongoDB. Este processo pode ser automatizado ou executado manualmente conforme a necessidade.
- _Consulta de Imóveis_: O endpoint GET / permite listar os imóveis que foram previamente coletados e salvos no banco de dados, facilitando a visualização e acesso às informações de interesse.
- _Debug de Scraping_: O endpoint /debug executa o processo de scraping de forma isolada para um imóvel específico e retorna o objeto parseado. Este endpoint é particularmente útil para verificar a correta extração e parsing dos dados em desenvolvimento ou em processos de manutenção.

## Monitoramento com Grafana e Prometheus

##### Clique na imagem para ver um video no youtube da aplicacão em execucão.

[![Cazador](preview.png)](https://www.youtube.com/watch?v=mUHuRovX7bY)

Para garantir a saúde e o desempenho adequados da aplicação, o Cazador utiliza Grafana e Prometheus para monitoramento. Essas ferramentas permitem acompanhar métricas importantes da aplicação e do ambiente de execução, como uso de CPU, memória, número de requisições e tempo de resposta.

- _Prometheus_: Configurado para coletar métricas da aplicação, especialmente focado nos endpoints /healthz e /readyz, que indicam, respectivamente, a saúde geral da aplicação e sua prontidão para receber tráfego.
- _Grafana_: Integrado ao Prometheus, oferece dashboards visuais que facilitam o acompanhamento das métricas coletadas, permitindo uma visualização rápida e eficiente do estado da aplicação.

## Requisitos

- Docker
- Kubectl
- Minikube (local, com docker)
- Hey (para stress test)

## Setup

- Clone este repositório `git clone https://github.com/carlosarraes/cazadorpy.git`
- Construa a imagen do docker `docker build -t carlosarraes/cazadorpy:latest .`
- Aplique as configuracões do k8s: `kubectl apply -f k8s/`
- Utilize o endpoint /update: Após a aplicação dos arquivos de configuração do Kubernetes, o serviço estará pronto para uso. (Ache o ip com Minikube ip, o endpoint estará exposto n porta 30007)
- Vá no Grafana, adicione prometheus como data source (http://prometheus:9090), crie uma dashboard, e uma das configuracões que coloquei manualmente no python foi um middleware de count

## Próximos passos

- Implementar a coleta de todas as páginas com base na entrada inicial (quantidade de imóveis encontrados).
- No momento, as 4 replicas estão batendo no mesmo endpoint, colocar para o controle do endpoint dizer qual bairro, dessa forma tem como "direcionar" qual bairro o endpoint ser chamado, evitando as replicas baterem na mesma pagina.
- Aprimorar o controle sobre a paginação dos resultados.
- Aprimorar o controle sobre a faixa de preço dos imóveis.
- Adicionar mais scrapers para diferentes sites de imóveis.
- Desenvolver uma interface básica para visualização dos dados coletados.

## Stress Test

Para realizar um teste de estresse na aplicação e visualizar como ela se comporta sob carga, você pode utilizar a ferramenta Hey, seguindo o exemplo abaixo:

`hey -n 1000 http://<endereço-do-serviço-no-minikube>:<porta>/`

Substitua <endereço-do-serviço-no-minikube> e <porta> pelos valores correspondentes ao serviço exposto pelo Minikube.
