import csv
import matplotlib.pyplot as plt
import os

def read_csv(file_path):
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def plot_comparison(data_a, data_b, data_c, metrics, output_dir='imagens'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for metric in metrics:
        plt.figure(figsize=(10, 6))
        
        # Plotando os dados do parâmetro 'a'
        factors_a = [float(item['factor']) for item in data_a]
        values_a = [float(item[metric]) for item in data_a]
        plt.plot(factors_a, values_a, marker='o', linestyle='-', label='car_subs = 0')

        # Plotando os dados do parâmetro 'b'
        factors_b = [float(item['factor']) for item in data_b]
        values_b = [float(item[metric]) for item in data_b]
        plt.plot(factors_b, values_b, marker='s', linestyle='-', label='car_subs = 0.2')

        # Plotando os dados do parâmetro 'c'
        factors_c = [float(item['factor']) for item in data_c]
        values_c = [float(item[metric]) for item in data_c]
        plt.plot(factors_c, values_c, marker='^', linestyle='-', label='car_subs = 0.3')
        
        plt.xlabel('Fator')
        if metric == 'vehicleTripStatistics_duration':
            plt.ylabel("Duração da viagem (s)")
        elif metric == 'vehicles_inserted':
            plt.ylabel("Veículos inseridos")
        elif metric == 'vehicleTripStatistics_speed':
            plt.ylabel("Velocidade média (m/s)")
        elif metric == 'vehicleTripStatistics_timeLoss':
            plt.ylabel("Tempo abaixo da velocidade ideal (s)")
        else:
            plt.ylabel(metric)
        
        # plt.title(f'{metric} vs. Factor')
        plt.legend()
        plt.grid(True)
        
        # Salva o gráfico no arquivo
        filename = os.path.join(output_dir, f'{metric}_comparison.png')
        plt.savefig(filename)
        plt.close()

# Exemplo de uso:
data_a = read_csv('data_0.csv')
data_b = read_csv('data_1.csv')
data_c = read_csv('data_2.csv')

# Escolha as métricas que você deseja comparar
selected_metrics = [
		'vehicleTripStatistics_duration',
		'vehicles_inserted',
		'vehicleTripStatistics_speed',
		'vehicleTripStatistics_timeLoss'
	]

# Gerar gráficos comparando os parâmetros a, b, c
plot_comparison(data_a, data_b, data_c, selected_metrics)