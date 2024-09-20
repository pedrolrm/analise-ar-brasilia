# Análise da Qualidade do Ar no Distrito Federal

Este projeto analisa a qualidade do ar no Distrito Federal, com foco no impacto das queimadas. Os dados foram coletados via API OpenWeather, comparando os níveis de poluição entre os anos de 2023 e 2024. O principal objetivo é visualizar o aumento das micropartículas no ar e outros poluentes durante o período de seca.

## Descrição
O projeto visa investigar os seguintes pontos:

- Comparação dos níveis de **PM2.5** e **PM10** (materiais particulados nocivos) entre 2023 e 2024.
- Avaliação dos níveis de **NO2** e **CO**, gases associados à queima de biomassa.
- Visualização das mudanças sazonais e impactos das queimadas nos níveis de poluição.

## Gráficos Gerados
Os gráficos mostram a concentração de poluentes no ar entre os meses de julho e setembro, destacando a diferença entre os anos de 2023 e 2024:

## Tecnologias Utilizadas

- **Python**: Para análise e visualização de dados.
- **Pandas**: Para manipulação dos dados.
- **Matplotlib**: Para criação dos gráficos.
- **API OpenWeather**: Fonte dos dados meteorológicos.

## Como Executar o Projeto

1. Clone este repositório:
   ```bash
   git clone https://github.com/pedrolrm/analise-ar-brasilia.git

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt 

3. Rode o script de análise:
   ```bash
   python AnaliseArBrasilia.py
