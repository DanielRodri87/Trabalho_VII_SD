locust -f locustfile.py \
  --headless \
  -u 200 -r 40 \
  --run-time 5m \
  --csv results/pico \
  --host http://localhost:8080 \
  --only-summary
