# Cria um diretório de resultados se não existir
mkdir -p results/pico

# Roda o teste com 200 usuários por 5 minutos (300 segundos)
locust -f locustfile.py \
  --headless \
  -u 200 -r 40 \
  --run-time 5m \
  --csv results/pico/run \
  --host http://localhost:8080 \
  --only-summary \
  --reset-stats