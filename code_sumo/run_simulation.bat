@echo off
setlocal enabledelayedexpansion

rem Diretório onde está o SUMO
set SUMO_DIR=C:\Users\marce\Documents\Faculdade\sumo-1.18.0\bin\

rem Caminho do arquivo de configuração
set CONFIG_FILE=simulation_batch.sumocfg

rem Número de execuções
set NUM_EXECUTIONS=30

rem Diretório para salvar os resultados
set OUTPUT_DIR=results

rem Criar o diretório de resultados se não existir
if not exist %OUTPUT_DIR% (
    mkdir %OUTPUT_DIR%
)

rem Loop para executar a simulação com seeds variáveis
for /L %%i in (1,1,%NUM_EXECUTIONS%) do (
    set SEED=%%i
    set OUTPUT_FILE=%OUTPUT_DIR%\rawDump_%%i.xml
    echo Executando simulação com seed !SEED! e salvando em !OUTPUT_FILE!
    %SUMO_DIR%\sumo -c %CONFIG_FILE% --seed !SEED! --netstate-dump !OUTPUT_FILE!
)

echo Todas as execuções foram concluídas.
