locust -f locustfile.py \
  --headless \
  -u 100 -r 20 \
  --run-time 10m \
  --csv results/medio \
  --host http://localhost:8080 \
  --only-summary
