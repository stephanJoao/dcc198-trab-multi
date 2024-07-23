import xml.etree.ElementTree as ET
#import pandas as pd
import matplotlib.pyplot as plt
import os
import csv

def analysis_statistics(xml_file):

    print('\n ---- ANALISANDO ESTATISTICAS ----\n')

    # Parse o arquivo XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extraindo valores
    performance = root.find('performance')
    vehicles = root.find('vehicles')
    #teleports = root.find('teleports')
    #safety = root.find('safety')
    #persons = root.find('persons')
    #personTeleports = root.find('personTeleports')
    vehicleTripStatistics = root.find('vehicleTripStatistics')
    #pedestrianStatistics = root.find('pedestrianStatistics')
    #rideStatistics = root.find('rideStatistics')
    #transportStatistics = root.find('transportStatistics')

    # Criando um dicionário com os valores extraídos
    data = {
        'performance': {
        #    'clockBegin': performance.get('clockBegin'),
        #    'clockEnd': performance.get('clockEnd'),
            'clockDuration': performance.get('clockDuration'),
            'traciDuration': performance.get('traciDuration'),
            'realTimeFactor': performance.get('realTimeFactor'),
            #'vehicleUpdatesPerSecond': performance.get('vehicleUpdatesPerSecond'),
            #'personUpdatesPerSecond': performance.get('personUpdatesPerSecond'),
            #'begin': performance.get('begin'),
            #'end': performance.get('end'),
            'duration': performance.get('duration')
        },
        'vehicles': {
            #'loaded': vehicles.get('loaded'),
            'inserted': vehicles.get('inserted'),
            #'running': vehicles.get('running'),
            #'waiting': vehicles.get('waiting')
        },
        #'teleports': {
        #    'total': teleports.get('total'),
        #    'jam': teleports.get('jam'),
        #    'yield': teleports.get('yield'),
        #    'wrongLane': teleports.get('wrongLane')
        #},
        # 'safety': {
        #     'collisions': safety.get('collisions'),
        #     'emergencyStops': safety.get('emergencyStops'),
        #     'emergencyBraking': safety.get('emergencyBraking')
        # },
        # 'persons': {
        #     'loaded': persons.get('loaded'),
        #     'running': persons.get('running'),
        #     'jammed': persons.get('jammed')
        # },
        # 'personTeleports': {
        #     'total': personTeleports.get('total'),
        #     'abortWait': personTeleports.get('abortWait'),
        #     'wrongDest': personTeleports.get('wrongDest')
        # },
         'vehicleTripStatistics': {
            'count': vehicleTripStatistics.get('count'),
            'routeLength': vehicleTripStatistics.get('routeLength'),
            'speed': vehicleTripStatistics.get('speed'),
            'duration': vehicleTripStatistics.get('duration'),
            'waitingTime': vehicleTripStatistics.get('waitingTime'),
            'timeLoss': vehicleTripStatistics.get('timeLoss'),
            'departDelay': vehicleTripStatistics.get('departDelay'),
            'departDelayWaiting': vehicleTripStatistics.get('departDelayWaiting'),
            'totalTravelTime': vehicleTripStatistics.get('totalTravelTime'),
            'totalDepartDelay': vehicleTripStatistics.get('totalDepartDelay')
        },
        # 'pedestrianStatistics': {
        #     'number': pedestrianStatistics.get('number'),
        #     'routeLength': pedestrianStatistics.get('routeLength'),
        #     'duration': pedestrianStatistics.get('duration'),
        #     'timeLoss': pedestrianStatistics.get('timeLoss')
        # },
        # 'rideStatistics': {
        #     'number': rideStatistics.get('number')
        # },
        # 'transportStatistics': {
        #     'number': transportStatistics.get('number')
        # }
    }

    # Convertendo o dicionário para um DataFrame
    #df = pd.DataFrame(data)

    print('\n ---- ESTATISTICAS ANALISADAS ----\n')

    # Exibindo o DataFrame
    #print(df)

    # Salvando o DataFrame em um arquivo CSV
    #df.to_csv('estatisticas.csv', index=False)
    #return df
    return data

def plot_graph(data_list, selected_metrics, output_dir='imagens'):
    
    print("\n ---- PLOTANDO GRÁFICO ---- \n")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    

    # Organize os dados por métrica
    metrics = {}
    
    for data_dict in data_list:
        if isinstance(data_dict, dict):  # Verifique se data_dict é um dicionário
            factor = data_dict['factor']
            for key, value in data_dict.items():
                if key != 'factor':
                    if key not in metrics:
                        metrics[key] = {'factor': [], 'values': []}
                    try:
                        float_value = float(value)
                        metrics[key]['factor'].append(factor)
                        metrics[key]['values'].append(float_value)
                    except ValueError:
                        print(f"Cannot convert value '{value}' for key '{key}' to float. Skipping this key.")
        else:
            print(f"Expected a dictionary but got {type(data_dict)}")
    
    # Gerar e salvar gráficos para cada métrica
    # Gerar e salvar gráficos para as métricas selecionadas
    for metric in selected_metrics:
        if metric in metrics:
            plt.figure(figsize=(10, 6))
            plt.plot(metrics[metric]['factor'], metrics[metric]['values'], marker='o', linestyle='-')
            plt.xlabel('factor')
            plt.ylabel(metric)
            plt.title(f'{metric} vs. factor')
            plt.grid(True)
            
            # Salva o gráfico no arquivo
            filename = os.path.join(output_dir, f'{metric}_vs_factor.png')
            plt.savefig(filename)
            plt.close()  # Fecha o gráfico para liberar memória
        
    print("\n ---- GRÁFICO PLOTADO ---- \n")
    
def save_to_csv(data_list, output_file='data.csv'):
    if data_list:
        # Obtenha o cabeçalho a partir das chaves do primeiro dicionário
        headers = sorted(data_list[0].keys())
        
        with open(output_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data_list)