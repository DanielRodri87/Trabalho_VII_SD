from locust import HttpUser, task, between
import random

class PetClinicUser(HttpUser):
    wait_time = between(1, 3)

    @task(4)
    def get_owners(self):
        self.client.get("/api/customer/owners")

    @task(3)
    def get_owner_by_id(self):
        owner_id = random.randint(1, 10)
        self.client.get(f"/api/customer/owners/{owner_id}")

    @task(2)
    def get_vets(self):
        self.client.get("/api/vet/vets")

    @task(1)
    def create_owner(self):
        payload = {
            "firstName": f"Test{random.randint(1, 9999)}",
            "lastName": "User",
            "address": "123 Main St",
            "city": "Picos",
            "telephone": str(random.randint(100000000, 999999999))
        }
        self.client.post("/api/customer/owners", json=payload)
