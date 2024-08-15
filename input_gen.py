import math
import pandas as pd
import numpy as np

def input_gen(data_file='collected_data.csv', factor=1.0, cars_subs_percentage=0.0, name='input_gen', verbose=False):
	
	print('\n---- GERANDO INPUT ----\n')

	# HARD CODED VALUES
	#collected_data_time = 1800 # 30 minutes
	collected_data_time = 3600 # 60 minutes
	avg_bus_capacity = 80
	avg_bus_usage = 0.35
	avg_car_capacity = 5
	avg_car_usage = 0.35
	cars_to_buses = (avg_bus_capacity * avg_bus_usage) / (avg_car_capacity * avg_car_usage)
	
	data = pd.read_csv(data_file)
	data['veiculo_T'] = data['veiculo'].apply(lambda x: 'C' if x == 'carro' else 'O')
	data['entrada'] = data['entrada'].apply(lambda x: 'M' if x == 'morro' else x)
	data['saida'] = data['saida'].apply(lambda x: 'M' if x == 'morro' else x)
	data['id'] = data['veiculo_T'] + data['entrada'] + data['saida']
	data['from'] = data['entrada'].apply(lambda x: 'morro-0' if x == 'M' else ('uf-0' if x == 'UF' else 'sp-0'))
	data['to'] = data['saida'].apply(lambda x: 'morro-4-s' if x == 'M' else ('saida-uf' if x == 'UF' else 'sp-0-s'))
	data['color'] = data['entrada'].apply(lambda x: '0,0,255' if x == 'M' else ('255,0,0' if x == 'UF' else '0,255,0'))

	# create XML file
	with open(name + '.xml', 'w') as f:
		f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		f.write('<routes>\n')
		f.write('\t<vType id="carro" vClass="passenger" />\n')
		f.write('\t<vType id="onibus" vClass="bus" />\n\n')
		for entrada in np.unique(data['entrada']):
			data_entrada = data[data['entrada'] == entrada]
			for saida in np.unique(data_entrada['saida']):
				data_saida = data_entrada[data_entrada['saida'] == saida]
				data_carro = data_saida[data_saida['veiculo'] == 'carro']
				cars = data_carro['contagem'].values[0]
				data_onibus = data_saida[data_saida['veiculo'] == 'onibus']
				buses = data_onibus['contagem'].values[0]
				if verbose:
					print('Cars (before):', cars)
					print('Buses (before):', buses)
				buses = buses + math.ceil(((cars * cars_subs_percentage) / cars_to_buses))
				cars = cars - math.ceil((cars * cars_subs_percentage))
				if verbose:
					print('cars (after):', cars)
					print('buses (after):', buses)				
				cars_period = (collected_data_time / ((cars + 1) * factor)).astype(int)
				buses_period = (collected_data_time / ((buses + 1) * factor)).astype(int)
				f.write('\t<flow id="{0}" color="{1}" begin="0" end="{2}" period="{3}" type="{4}" departLane="best" departSpeed="max" from="{5}" to="{6}"/>\n'.format(data_carro['id'].values[0], data_carro['color'].values[0], collected_data_time, cars_period, data_carro['veiculo'].values[0], data_carro['from'].values[0], data_carro['to'].values[0]))
				f.write('\t<flow id="{0}" color="{1}" begin="0" end="{2}" period="{3}" type="{4}" departLane="best" departSpeed="max" from="{5}" to="{6}"/>\n'.format(data_onibus['id'].values[0], data_onibus['color'].values[0], collected_data_time, buses_period, data_onibus['veiculo'].values[0], data_onibus['from'].values[0], data_onibus['to'].values[0]))
		f.write('</routes>')
	
	print('\n---- INPUT GERADO ----\n')


if __name__ == '__main__':
	input_gen(factor=1.0, cars_subs_percentage=0.0, verbose=True)