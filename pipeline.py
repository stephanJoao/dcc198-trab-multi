import os, subprocess
import pandas as pd

from input_gen import input_gen
from flux_analysis import calculate_fluxes
from statistics_analysis import analysis_statistics, plot_graph, save_to_csv
from plot_results import plot_results

if __name__ == '__main__':
	
	df_results = pd.DataFrame()
	list_stats = []
	
	#factors = [0.5, 1.0, 1.5]
	#factors = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
	menor_fator = 0.5
	maior_fator = 3.0
	intervalo = 0.10
	factors = [round(menor_fator + i * intervalo, 10) for i in range(int((maior_fator - menor_fator) / intervalo) + 1)]
	#print(factors)
	
	cars_subs = 0.0

	# caminho do script
	script_path = './code_sumo/run_simulation.sh'
	
	# número de execuções
	num_execs = 5

	for factor in factors:
		
		input_gen(factor=factor, 
			cars_subs_percentage=cars_subs, 
			name='./code_sumo/entrada.poly', 
			verbose=False)
		
		# run sh command
		subprocess.run([script_path, str(num_execs)], check=True)
		
		# calculando os fluxos
		# e concatenando em df_results
		files = [f'results/rawDump_{i}.xml' for i in range(1, num_execs+1)]
		results = calculate_fluxes(files)
		results['factor'] = factor
		df_results = pd.concat([df_results, results], axis=0)
		
		# analisando o arquivo com estatisticas gerais
		xml_file = './output/estatistica.xml'
		stats = analysis_statistics(xml_file)
		
		flattened_data = {
			'factor': factor,
			**{'performance_' + k: v for k, v in stats['performance'].items()},
			**{'vehicles_' + k: v for k, v in stats['vehicles'].items()},
			**{'vehicleTripStatistics_' + k: v for k, v in stats['vehicleTripStatistics'].items()}
		}
		
		list_stats.append(flattened_data)
		#data_stats = pd.concat([df_stats, stats], axis=0)
		#df_stats.to_csv('stats.csv', index=False)
    
	#df_results.to_csv('results.csv', index=False)
	plot_results(df_results)
 
	selected_metrics = [
		'vehicles_inserted',
		'vehicleTripStatistics_duration'
		'vehicleTripStatistics_speed',
		'vehicleTripStatistics_timeLoss'
	]

	plot_graph(list_stats, selected_metrics)
	save_to_csv(list_stats)
    # Adiciona o dicionário à lista
	# plot car flux
	# plot bus flux

# (rodar simulação para diferentes fatores de substituição de carros por ônibus)

# intervalo de variação do fator de multiplicação do fluxo de entrada

# for cada fator
# 	gerar xml
# 	rodar simulação (com diferentes seeds e um número de amostra razoável = 30? 10?)
# 		(análise de sensibilidade? trabalhos futuros talvez)
#	 	armazenar fluxo para cada saída
# 	calcular fluxo médio de cada saída
# plotar fluxo médio de cada saída por fator de multiplicação (atinge saturaçao? qual a relação?)


# 3 artigos similares com o nosso (independente do software) - se der com sumo, ótimo
# 2 artigos só sobre transito

