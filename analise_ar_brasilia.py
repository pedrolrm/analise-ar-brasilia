import requests
import time
import pandas as pd
import matplotlib.pyplot as plt

# Substitua pela sua chave de API
api_key = "sua chave api"

# Latitude e Longitude de Brasília
lat = "-15.7801"
lon = "-47.9292"

# Função para coletar dados de um período específico
def coletar_dados(start_date, end_date, api_key):
    start = int(time.mktime(time.strptime(start_date, "%Y-%m-%d %H:%M:%S")))
    end = int(time.mktime(time.strptime(end_date, "%Y-%m-%d %H:%M:%S")))

    url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao fazer requisição: {response.status_code}")

# Coletando dados de 2024
data_2024 = coletar_dados("2024-07-17 00:00:00", "2024-09-17 00:00:00", api_key)

# Coletando dados de 2023
data_2023 = coletar_dados("2023-07-17 00:00:00", "2023-09-17 00:00:00", api_key)

# Função para extrair dados específicos
def extrair_dados(data):
    data_list = []
    for entry in data['list']:
        timestamp = entry['dt']
        date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp))
        pm2_5 = entry['components']['pm2_5']
        pm10 = entry['components']['pm10']
        co = entry['components']['co']
        no2 = entry['components']['no2']
        aqi = entry['main']['aqi']
        
        data_list.append({
            'Data': date_time,
            'AQI': aqi,
            'PM2.5': pm2_5,
            'PM10': pm10,
            'CO': co,
            'NO2': no2,
        })
    return pd.DataFrame(data_list)

# Convertendo os dados para DataFrames
df_2024 = extrair_dados(data_2024)
df_2023 = extrair_dados(data_2023)

# Converta a coluna 'Data' para o formato datetime
df_2024['Data'] = pd.to_datetime(df_2024['Data'])
df_2023['Data'] = pd.to_datetime(df_2023['Data'])

# Determinando o intervalo máximo para o eixo y
max_pm25_2024 = df_2024['PM2.5'].max()
max_pm10_2024 = df_2024['PM10'].max()
max_pm25_2023 = df_2023['PM2.5'].max()
max_pm10_2023 = df_2023['PM10'].max()

max_pm25 = max(max_pm25_2024, max_pm25_2023)
max_pm10 = max(max_pm10_2024, max_pm10_2023)

# Definindo o tamanho do gráfico
plt.figure(figsize=(14, 7))

# Primeiro gráfico: Dados do período do ano 2023
plt.subplot(1, 2, 1)
plt.plot(df_2023['Data'], df_2023['PM2.5'], label='PM2.5', linestyle='-', color='blue')
plt.plot(df_2023['Data'], df_2023['PM10'], label='PM10', linestyle='-', color='red')
plt.title('Poluição do Ar por Material Particulado (DF) - 2023')
plt.xlabel('Data')
plt.ylabel('Concentração de Poluentes (µg/m³)')
plt.legend()
plt.xticks(rotation=45)
plt.ylim(0, max_pm25 + 10)  # Ajusta o intervalo do eixo y com o mesmo valor

# Segundo gráfico: Dados do período 2024
plt.subplot(1, 2, 2)
plt.plot(df_2024['Data'], df_2024['PM2.5'], label='PM2.5', linestyle='-', color='blue')
plt.plot(df_2024['Data'], df_2024['PM10'], label='PM10', linestyle='-', color='red')
plt.title('Poluição do Ar por Material Particulado (DF) - 2024')
plt.xlabel('Data')
plt.ylabel('Concentração de Poluentes (µg/m³)')
plt.legend()
plt.xticks(rotation=45)
plt.ylim(0, max_pm25 + 10)  # Ajusta o intervalo do eixo y com um pequeno buffer

# Ajustando o layout para que os gráficos não se sobreponham
plt.tight_layout()

# Exibindo os gráficos
plt.show()

oms_limits = {
    'PM2.5_daily': 15,  # µg/m³
    'PM10_daily': 45   # µg/m³
}

# Agrupar os dados por dia e calcular a média
daily_avg_2023 = df_2023.resample('D', on='Data').mean()
daily_avg_2024 = df_2024.resample('D', on='Data').mean()

# Contar dias que excedem os limites para 2023
count_2023_pm25 = (daily_avg_2023['PM2.5'] > oms_limits['PM2.5_daily']).sum()
count_2023_pm10 = (daily_avg_2023['PM10'] > oms_limits['PM10_daily']).sum()

# Contar dias que excedem os limites para 2024
count_2024_pm25 = (daily_avg_2024['PM2.5'] > oms_limits['PM2.5_daily']).sum()
count_2024_pm10 = (daily_avg_2024['PM10'] > oms_limits['PM10_daily']).sum()

# Exibir os resultados
print('-'*110)
print(f"2023 - Número de dias que PM2.5 excedeu o limite da OMS: {count_2023_pm25}")
print(f"2023 - Número de dias que PM10 excedeu o limite da OMS: {count_2023_pm10}")
print('-'*110)
print(f"2024 - Número de dias que PM2.5 excedeu o limite da OMS: {count_2024_pm25}")
print(f"2024 - Número de dias que PM10 excedeu o limite da OMS: {count_2024_pm10}")
print('-'*110)
print(f'Em 2024, ocorreu um aumento de {int(count_2024_pm25 / count_2023_pm25 * 100 - 100)}% na quantidade de dias que o limite da OMS para PM2.5 foi ultrapassado')
print('-'*110)

# Tratando outiliers nos dados acerca da concentração de NO2
min_valid_no2 = 0
max_valid_no2 = 300

# Filtrando os dados para remover outliers
df_2024_clean = df_2024[(df_2024['NO2'] >= min_valid_no2) & (df_2024['NO2'] <= max_valid_no2)]
df_2023_clean = df_2023[(df_2023['NO2'] >= min_valid_no2) & (df_2023['NO2'] <= max_valid_no2)]

# Determinando o intervalo máximo para o eixo y
max_no2_2024 = df_2024['NO2'].max()
max_no2_2023 = df_2023['NO2'].max()
max_no2 = max(max_no2_2024, max_no2_2023)

# Definindo o tamanho do gráfico
plt.figure(figsize=(14, 7))

# Primeiro gráfico: Dados do período do ano passado para NO2
plt.subplot(1, 2, 1)
plt.plot(df_2023['Data'], df_2023['NO2'], label='NO2', linestyle='-', color='purple')
plt.title('Concentração de NO2 no Ar (DF) - 2023')
plt.xlabel('Data')
plt.ylabel('Concentração de NO2 (µg/m³)')
plt.legend()
plt.xticks(rotation=45)
plt.ylim(0, max_no2 + 10)  # Ajusta o intervalo do eixo y com o mesmo valor

# Segundo gráfico: Dados do período atual para NO2
plt.subplot(1, 2, 2)
plt.plot(df_2024['Data'], df_2024['NO2'], label='NO2', linestyle='-', color='purple')
plt.title('Concentração de NO2 no Ar (DF) - 2024')
plt.xlabel('Data')
plt.ylabel('Concentração de NO2 (µg/m³)')
plt.legend()
plt.xticks(rotation=45)
plt.ylim(0, max_no2 + 10)  # Ajusta o intervalo do eixo y com um pequeno buffer

# Ajustando o layout para que os gráficos não se sobreponham
plt.tight_layout()

# Exibindo os gráficos
plt.show()

# Determinando o intervalo máximo para o eixo y
max_co_2024 = df_2024['CO'].max()
max_co_2023 = df_2023['CO'].max()
max_co = max(max_co_2024, max_co_2023)

# Definindo o tamanho do gráfico
plt.figure(figsize=(14, 7))

# Primeiro gráfico: Dados do período do ano passado para CO
plt.subplot(1, 2, 1)
plt.plot(df_2023['Data'], df_2023['CO'], label='CO', linestyle='-', color='green')
plt.title('Concentração de CO no Ar (DF) - 2023')
plt.xlabel('Data')
plt.ylabel('Concentração de CO no Ar (µg/m³)')
plt.legend()
plt.xticks(rotation=45)
plt.ylim(0, max_co + 10)  # Ajusta o intervalo do eixo y com o mesmo valor

# Segundo gráfico: Dados do período atual para CO
plt.subplot(1, 2, 2)
plt.plot(df_2024['Data'], df_2024['CO'], label='CO', linestyle='-', color='green')
plt.title('Concentração de CO no Ar (DF) - 2024')
plt.xlabel('Data')
plt.ylabel('Concentração de CO (µg/m³)')
plt.legend()
plt.xticks(rotation=45)
plt.ylim(0, max_co + 10)  # Ajusta o intervalo do eixo y com um pequeno buffer

# Ajustando o layout para que os gráficos não se sobreponham
plt.tight_layout()

# Exibindo os gráficos
plt.show()
