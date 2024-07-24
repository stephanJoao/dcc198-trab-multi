import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_results(df_results, output_dir='imagens'):
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	# read results
	#df_results = pd.read_csv('results.csv')

	types = df_results['type'].unique()

	for type in types:
		df_type = df_results[df_results['type'] == type]
		df_type = df_type.sort_values(by='factor')

		plt.plot(df_type['factor'], df_type['saida-uf'], label='Saída UF', marker='o', linestyle='-')
		plt.plot(df_type['factor'], df_type['saida-morro'], label='Saída Morro', marker='o', linestyle='-')
		plt.plot(df_type['factor'], df_type['saida-sp'], label='Saída SP', marker='o', linestyle='-')

		plt.xlabel('Fator de multiplicação')
		plt.ylabel('Fluxo médio')
		plt.legend()
		plt.grid(True)

		#plt.show()

		# Salva o gráfico no arquivo
		filename = os.path.join(output_dir, f'fluxo_{type}_vs_factor.png')
		plt.savefig(filename)
		plt.close()  # Fecha o gráfico para liberar memória




