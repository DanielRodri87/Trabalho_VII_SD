locust -f locustfile.py \
  --headless \
  -u 50 -r 10 \
  --run-time 10m \
  --csv results/leve \
  --host http://localhost:8080 \
  --only-summary
