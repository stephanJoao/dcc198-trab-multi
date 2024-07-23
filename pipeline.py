import os, subprocess
import pandas as pd
from input_gen import input_gen
from flux_analysis import calculate_fluxes

if __name__ == '__main__':
	
	df_results = pd.DataFrame()
	
	factors = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
	cars_subs = 0.0

	for factor in factors:
		print('\n---- GERANDO INPUT ----\n')
		input_gen(factor=factor, cars_subs_percentage=cars_subs, name='./code_sumo/multidisciplinar/entrada.poly', verbose=True)
		print('\n---- INPUT GERADO ----\n')
		
		x = 3
		
		# run sh command
		subprocess.run(['sh', './code_sumo/multidisciplinar/run_simulation.sh'], check=True)
		
		files = [f'results/rawDump_{i}.xml' for i in range(1, x+1)]
		print('\n---- CALCULANDO FLUXOS ----\n')
		results = calculate_fluxes(files)
		print('\n---- FLUXOS CALCULADOS ----\n')
		results['factor'] = factor
		df_results = pd.concat([df_results, results], axis=0)

	df_results.to_csv('results.csv', index=False)

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
