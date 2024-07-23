import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
	# read results
	df_results = pd.read_csv('results.csv')

	types = df_results['type'].unique()

	for type in types:
		df_type = df_results[df_results['type'] == type]
		df_type = df_type.sort_values(by='factor')

		plt.plot(df_type['factor'], df_type['saida-uf'], label='Saída UF')
		plt.plot(df_type['factor'], df_type['saida-morro'], label='Saída Morro')
		plt.plot(df_type['factor'], df_type['saida-sp'], label='Saída SP')

		plt.xlabel('Fator de multiplicação')
		plt.ylabel('Fluxo médio')
		plt.legend()
		plt.show()




