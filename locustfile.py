from locust import HttpUser, task, between
import random

# Definimos o host principal (API Gateway)
API_GATEWAY_HOST = "http://localhost:8080"
MAX_OWNER_ID = 200 # Assumindo que você populará o banco

class PetClinicUser(HttpUser):
    # O host base para todas as requisições
    host = API_GATEWAY_HOST 
    wait_time = between(1, 3)

    @task(4)
    def get_owners(self):
        # GET /api/customer/owners (Rota do Gateway para Customer Service)
        self.client.get("/api/customer/owners", name="GET /owners List")

    @task(3)
    def get_owner_by_id(self):
        # GET /api/customer/owners/{id}
        owner_id = random.randint(1, MAX_OWNER_ID)
        self.client.get(f"/api/customer/owners/{owner_id}", name="GET /owners/[id]")

    @task(2)
    def get_vets(self):
        # GET /api/vet/vets (Rota do Gateway para Vets Service)
        self.client.get("/api/vet/vets", name="GET /vets List")

    @task(1)
    def create_owner(self):
        # POST /api/customer/owners
        payload = {
            "firstName": f"Test{random.randint(1, 99999)}",
            "lastName": f"User{random.randint(1, 99999)}",
            "address": "123 Main St",
            "city": "Picos",
            "telephone": str(random.randint(1000000000, 9999999999))
        }
        self.client.post("/api/customer/owners", json=payload, name="POST /owners")