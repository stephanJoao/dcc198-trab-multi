#!/bin/bash

# Diretório onde está o SUMO
SUMO_DIR="/usr/bin"

# Caminho do arquivo de configuração
CONFIG_FILE="./code_sumo/multidisciplinar/simulation_batch.sumocfg"

# Número de execuções
NUM_EXECUTIONS=10

# Diretório para salvar os resultados
OUTPUT_DIR="results"

# Criar o diretório de resultados se não existir
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir "$OUTPUT_DIR"
fi

# Loop para executar a simulação com seeds variáveis
for i in $(seq 1 $NUM_EXECUTIONS); do
    SEED=$i
    OUTPUT_FILE="$OUTPUT_DIR/rawDump_$i.xml"
    echo "Executando simulação com seed $SEED e salvando em $OUTPUT_FILE"
    "$SUMO_DIR/sumo" -c "$CONFIG_FILE" --seed $SEED --netstate-dump "$OUTPUT_FILE"
done

echo "Todas as execuções foram concluídas."
