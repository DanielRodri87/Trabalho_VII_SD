#!/bin/bash

REPETITIONS=5 
HOST="http://localhost:8080"  # API Gateway
LOCUST_FILE="locustfile.py"
DOCKER_DIR="spring-petclinic-microservices"

# --- Função de Reset do Docker com Espera ---
docker_reset_and_wait() {
    echo "--- [$(date +%H:%M:%S)] Reiniciando o ambiente Docker para garantir estabilidade ---"

    # 1. Derruba todos os serviços (usando sudo)
    cd $DOCKER_DIR
    sudo docker-compose down
    
    # 2. Sobe todos os serviços em modo detached (usando sudo)
    sudo docker-compose up -d
    cd ..
    
    # 3. Tempo de espera CRUCIAL para estabilização (Eureka, DB, Inicialização do Spring Boot)
    echo "Aguardando 120 segundos para estabilização dos serviços..."
    sleep 120
    
    # 4. Verificação de saúde
    curl -s http://localhost:8080/api/customer/owners > /dev/null
    if [ $? -ne 0 ]; then
        echo "Aviso: A verificação de saúde do Customers Service falhou (código $?). Prosseguindo, mas verifique os logs se houver erros."
    else
        echo "Verificação de saúde via Gateway (8080) OK."
    fi
    echo "--- Ambiente Docker Pronto ---"
}

# Limpa a pasta de resultados
rm -rf results
mkdir -p results/leve results/medio results/pico

echo "Iniciando $REPETITIONS repetições para cada cenário (Total de 15 reinicializações de Docker)."
echo "O script pedirá sua senha de sudo a cada reinicialização do Docker."

# --- Cenário A (Leve) ---
echo "--- Cenário A (Leve): 50u por 10m ---"
for i in $(seq 1 $REPETITIONS); do
    docker_reset_and_wait 
    echo "  Rodada $i de $REPETITIONS: LEVE"
    locust -f $LOCUST_FILE \
      --headless \
      -u 50 -r 10 \
      --run-time 10m \
      --csv "results/leve/leve_stats_run_$i" \
      --host $HOST \
      --only-summary \
      --reset-stats
done

# --- Cenário B (Moderado) ---
echo "--- Cenário B (Moderado): 100u por 10m ---"
for i in $(seq 1 $REPETITIONS); do
    docker_reset_and_wait 
    echo "  Rodada $i de $REPETITIONS: MODERADO"
    locust -f $LOCUST_FILE \
      --headless \
      -u 100 -r 20 \
      --run-time 10m \
      --csv "results/medio/medio_stats_run_$i" \
      --host $HOST \
      --only-summary \
      --reset-stats
done

# --- Cenário C (Pico) ---
echo "--- Cenário C (Pico): 200u por 5m ---"
for i in $(seq 1 $REPETITIONS); do
    docker_reset_and_wait 
    echo "  Rodada $i de $REPETITIONS: PICO"
    locust -f $LOCUST_FILE \
      --headless \
      -u 200 -r 40 \
      --run-time 5m \
      --csv "results/pico/pico_stats_run_$i" \
      --host $HOST \
      --only-summary \
      --reset-stats
done

echo "Todos os testes concluídos. Resultados CSVs salvos nas pastas 'results'."