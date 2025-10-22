# Cria um diretório de resultados se não existir
mkdir -p results/leve

# Roda o teste com 50 usuários por 10 minutos (600 segundos)
locust -f locustfile.py \
  --headless \
  -u 50 -r 10 \
  --run-time 10m \
  --csv results/leve/run \
  --host http://localhost:8080 \
  --only-summary \
  --reset-stats # Reseta estatísticas antes de começar.