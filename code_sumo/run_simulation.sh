#!/bin/bash

# Verifica se um parâmetro foi passado
if [ $# -eq 0 ]; then
    echo "Uso: $0 <numero_de_execucoes>"
    exit 1
fi

# Número de execuções passado como parâmetro
NUM_EXECUTIONS=$1

# Diretório onde está o SUMO
SUMO_DIR="/usr/bin"

# Caminho do arquivo de configuração
CONFIG_FILE="./code_sumo/simulation_batch.sumocfg"


# Diretório para salvar os resultados
RAWDUMP_DIR="results"
OUTPUT_DIR="output"


# Criar o diretório de resultados se não existir
if [ ! -d "$RAWDUMP_DIR" ]; then
    mkdir "$RAWDUMP_DIR"
fi
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir "$OUTPUT_DIR"
fi

# Loop para executar a simulação com seeds variáveis
for i in $(seq 1 $NUM_EXECUTIONS); do
    SEED=$i
    OUTPUT_FILE="$RAWDUMP_DIR/rawDump_$i.xml"
    echo "Executando simulação com seed $SEED e salvando em $OUTPUT_FILE"
    "$SUMO_DIR/sumo" -c "$CONFIG_FILE" --seed $SEED --netstate-dump "$OUTPUT_FILE" --statistic-output ./output/estatistica.xml > "$OUTPUT_DIR"/output_$i.txt
done

echo "Todas as execuções foram concluídas."
