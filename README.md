# Speedrun Data Collector and Visualizer

Este projeto é uma solução completa para coletar dados de speedruns de um jogo específico na plataforma [speedrun.com](https://www.speedrun.com/) e visualizá-los de forma interativa. Ele é composto por um script Python para a extração e processamento dos dados, e um projeto Processing para a criação de visualizações dinâmicas dos tempos e rankings dos jogadores ao longo do tempo.



## Descrição

O script `gerar_csv_speedrun.py` em Python interage com a API do speedrun.com para extrair os melhores tempos diários de speedruns para um jogo e categoria específicos. Os dados coletados incluem informações sobre os jogadores e seus tempos, que são então organizados e exportados para um arquivo CSV (`data.csv`).

Complementarmente, o projeto Processing (composto por `Person.pde` e `DataVisualization.pde`) utiliza esses dados para gerar visualizações dinâmicas, mostrando a evolução dos tempos e as posições dos jogadores no ranking ao longo do tempo. Isso permite uma análise aprofundada do desempenho e da competitividade na categoria de speedrun selecionada.



## Funcionalidades

- **Coleta de Dados Automatizada**: Extrai os melhores tempos diários de speedruns diretamente da API do speedrun.com.
- **Processamento de Dados**: Organiza os dados coletados, identificando jogadores únicos e seus melhores tempos por dia.
- **Exportação para CSV**: Salva os dados processados em um arquivo CSV (`data.csv`) para fácil acesso e análise.
- **Visualização Dinâmica**: Gera animações interativas que mostram a progressão dos tempos e rankings dos jogadores ao longo do tempo.
- **Suporte a Múltiplas Plataformas**: O script Python é compatível com diferentes sistemas operacionais, e o projeto Processing pode ser executado em ambientes que suportam Java.



## Como Começar

Para configurar e executar este projeto, siga as instruções abaixo:

### Pré-requisitos

- **Python 3.x**: Necessário para executar o script de coleta de dados.
- **Processing**: Necessário para executar o projeto de visualização. Baixe-o em [processing.org](https://processing.org/download/).

### Instalação

1. Clone este repositório para sua máquina local:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. Instale as dependências Python:
   ```bash
   pip install requests tqdm
   ```

### Configuração do Projeto Processing

1. Abra o IDE do Processing.
2. Vá em `File > Open...` e selecione o arquivo `DataVisualization.pde` dentro da pasta do projeto.
3. Certifique-se de que os arquivos `Person.pde`, `data.tsv` e `Jygquif1-96.vlw` estejam na mesma pasta do `DataVisualization.pde`.
4. O projeto Processing utiliza a biblioteca `VideoExport` (com.hamoid). Se você não a tiver instalada, vá em `Sketch > Import Library > Add Library...` e procure por `VideoExport` para instalá-la.



## Uso

### Coletando Dados (Python)

1. Edite o arquivo `gerar_csv_speedrun.py` para configurar o `GAME_ID`, `CATEGORY_ID`, `VAR_PLATFORM`, `VAR_PLATFORM_VALUE`, `VAR_HOVERBOARD` e `VAR_HOVERBOARD_VALUE` de acordo com o jogo e categoria de speedrun que você deseja analisar. Você pode encontrar esses IDs na URL do speedrun.com ou na documentação da API.

2. Execute o script Python:
   ```bash
   python gerar_csv_speedrun.py
   ```
   Isso irá gerar um arquivo `data.csv` (ou `data.tsv` se você alterar o delimitador no script) com os dados coletados.

### Visualizando Dados (Processing)

1. Certifique-se de que o arquivo `data.tsv` (ou `data.csv` renomeado para `data.tsv` se o script Python gerou `data.csv` e você não alterou o código Processing para ler `.csv`) esteja na mesma pasta do seu sketch Processing.
2. Abra o `DataVisualization.pde` no Processing IDE.
3. Clique no botão 'Run' (o triângulo ▶) para iniciar a visualização. O sketch irá gerar um vídeo (`VideoTeste.mp4`) mostrando a evolução dos rankings.



## Tecnologias Utilizadas

- **Python 3.x**: Para coleta e processamento de dados.
- **Processing**: Para visualização e geração de vídeo.
- **Requests**: Biblioteca Python para fazer requisições HTTP à API do speedrun.com.
- **tqdm**: Biblioteca Python para exibir barras de progresso durante a coleta de dados.
- **VideoExport (Processing Library)**: Para exportar as visualizações como arquivos de vídeo.
- **FFmpeg**: Ferramenta externa utilizada pela biblioteca VideoExport para codificação de vídeo (geralmente já incluída ou facilmente instalável).



## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.




## Funcionalidades

*   **Coleta de Dados Automatizada**: Extrai os melhores tempos diários de speedruns diretamente da API do speedrun.com.
*   **Processamento de Dados**: Organiza os dados coletados, identificando jogadores únicos e seus melhores tempos por dia.
*   **Exportação para CSV/TSV**: Salva os dados processados em um arquivo CSV ou TSV (`data.csv` ou `data.tsv`) para fácil acesso e análise.
*   **Visualização Dinâmica**: Gera animações interativas que mostram a progressão dos tempos e rankings dos jogadores ao longo do tempo.
*   **Suporte a Múltiplas Plataformas**: O script Python é compatível com diferentes sistemas operacionais, e o projeto Processing pode ser executado em ambientes que suportam Java.




## Como Começar

Para configurar e executar este projeto, siga as instruções abaixo:

### Pré-requisitos

*   **Python 3.x**: Necessário para executar o script de coleta de dados. Recomenda-se usar um ambiente virtual (`venv` ou `conda`).
*   **Processing**: Necessário para executar o projeto de visualização. Baixe-o em [processing.org](https://processing.org/download/).
*   **Git**: Para clonar o repositório.

### Instalação

1.  Clone este repositório para sua máquina local:
    ```bash
    git clone https://github.com/gustavobergz/SpeedrunDataCollector.git
    cd SpeedrunDataCollector
    ```
2.  (Opcional) Crie e ative um ambiente virtual para as dependências Python:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Linux/macOS
    # venv\Scripts\activate  # No Windows
    ```
3.  Instale as dependências Python:
    ```bash
    pip install requests tqdm
    ```

### Configuração do Projeto Processing

1.  Abra o IDE do Processing.
2.  Vá em `File > Open...` e selecione o arquivo `DataVisualization.pde` dentro da pasta `DataVisualization` do projeto clonado.
3.  Certifique-se de que os arquivos `Person.pde`, `data.tsv` e `Jygquif1-96.vlw` (fonte utilizada) estejam na mesma pasta do `DataVisualization.pde`.
4.  O projeto Processing utiliza a biblioteca `VideoExport` (com.hamoid). Se você não a tiver instalada, vá em `Sketch > Import Library > Add Library...` e procure por `VideoExport` para instalá-la. Certifique-se de que o FFmpeg esteja configurado corretamente, conforme as instruções da biblioteca VideoExport.




## Uso

### Coletando Dados (Python)

1.  Edite o arquivo `gerar_csv_speedrun.py` para configurar as variáveis `GAME_ID`, `CATEGORY_ID`, `VAR_PLATFORM`, `VAR_PLATFORM_VALUE`, `VAR_HOVERBOARD` e `VAR_HOVERBOARD_VALUE` de acordo com o jogo e categoria de speedrun que você deseja analisar. Você pode encontrar esses IDs na URL do speedrun.com ou consultando a documentação da API do speedrun.com.
    *   **`GAME_ID`**: O ID único do jogo no speedrun.com.
    *   **`CATEGORY_ID`**: O ID único da categoria de speedrun dentro do jogo.
    *   **`VAR_PLATFORM`** e **`VAR_PLATFORM_VALUE`**: IDs para filtrar por plataforma (ex: "Web").
    *   **`VAR_HOVERBOARD`** e **`VAR_HOVERBOARD_VALUE`**: IDs para filtrar por uma variável específica do jogo (ex: "No Hoverboard").

2.  Execute o script Python a partir do terminal:
    ```bash
    python gerar_csv_speedrun.py
    ```
    Este comando irá gerar um arquivo `data.tsv` (ou `data.csv`, dependendo da configuração no script) na raiz do projeto com os dados coletados. O script inclui uma barra de progresso (`tqdm`) para acompanhar a coleta de dados diária.

### Visualizando Dados (Processing)

1.  Certifique-se de que o arquivo `data.tsv` (gerado pelo script Python) esteja presente na pasta `DataVisualization` do seu projeto Processing. Se o script Python gerou `data.csv`, você precisará renomeá-lo para `data.tsv` ou ajustar o código Processing para ler `.csv`.
2.  Abra o `DataVisualization.pde` no Processing IDE.
3.  Clique no botão 'Run' (o ícone de triângulo ▶) para iniciar a visualização. O sketch irá gerar um vídeo (`VideoTeste.mp4`) na pasta `DataVisualization` mostrando a evolução dos rankings dos jogadores ao longo do tempo.




## Tecnologias Utilizadas

*   **Python 3.x**: Linguagem de programação utilizada para a coleta e processamento de dados.
*   **Processing**: Ambiente de desenvolvimento e linguagem para a criação de visualizações dinâmicas e geração de vídeo.
*   **Requests**: Biblioteca Python para realizar requisições HTTP à API do speedrun.com de forma eficiente.
*   **tqdm**: Biblioteca Python para exibir barras de progresso informativas durante a execução do script de coleta de dados.
*   **VideoExport (Processing Library)**: Biblioteca essencial do Processing para exportar as visualizações animadas como arquivos de vídeo (MP4).
*   **FFmpeg**: Ferramenta externa de código aberto utilizada pela biblioteca VideoExport para codificação e manipulação de vídeo.




## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.


