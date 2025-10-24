# 🚀 Testes de Performance - Spring PetClinic Microservices

<div align="center">

![Performance Testing](https://img.shields.io/badge/Testing-Performance-blue?style=for-the-badge)
![Locust](https://img.shields.io/badge/Locust-Load_Testing-green?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-Analysis-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Análise de carga e performance para arquitetura de microserviços**

[Visão Geral](#-visão-geral) •
[Instalação](#-instalação) •
[Execução](#-execução) •
[Resultados](#-resultados) •
[Arquitetura](#-arquitetura)

</div>

---

[![YouTube](https://img.shields.io/badge/YouTube-Demonstração-red?style=for-the-badge&logo=youtube&logoColor=white)](https://youtu.be/PGOzffyX7eQ?si=H35gxCF3-zcO3oPc)


## 📋 Visão Geral

Este projeto implementa testes de carga automatizados para o **Spring PetClinic Microservices**, avaliando o comportamento do sistema sob diferentes cenários de stress. Utilizando **Locust** para simulação de usuários e **Docker** para isolamento de ambiente, garantimos resultados consistentes e reproduzíveis.

### 🎯 Objetivos

- Avaliar latência e throughput em condições variadas
- Identificar gargalos de performance
- Medir taxas de erro sob alta carga
- Gerar métricas consolidadas para análise

---

## 🏗️ Arquitetura

```
┌─────────────┐
│   Locust    │  Simula usuários concorrentes
│  (Cliente)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ API Gateway │  Porta 8080
│  (Spring)   │
└──────┬──────┘
       │
       ├──────────┬──────────┬──────────┐
       ▼          ▼          ▼          ▼
  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
  │Customer│ │  Vets  │ │ Visits │ │Discovery│
  │Service │ │Service │ │Service │ │(Eureka)│
  └────────┘ └────────┘ └────────┘ └────────┘
```

### 📡 Endpoints Testados

| Método | Endpoint | Peso | Descrição |
|--------|----------|------|-----------|
| `GET` | `/api/customer/owners` | 4 | Lista todos os proprietários |
| `GET` | `/api/customer/owners/{id}` | 3 | Busca proprietário por ID |
| `GET` | `/api/vet/vets` | 2 | Lista todos os veterinários |
| `POST` | `/api/customer/owners` | 1 | Cria novo proprietário |

---

## 🔧 Instalação

### Pré-requisitos

- **Docker** & **Docker Compose**
- **Python 3.8+**
- **Maven** (para build do projeto)
- **Locust**

### Setup Rápido

```bash
# 1. Clone o repositório
git clone <seu-repositorio>
cd <diretorio-projeto>

# 2. Instale dependências Python
pip install -r req.txt
pip install locust

# 3. Build do projeto Spring Boot
./mvnw clean install -DskipTests

# 4. Suba os containers Docker
docker-compose -f docker-compose.yml up -d

# 5. Aguarde estabilização (2-3 minutos)
sleep 120
```

### 📦 Dependências Python

```
pandas
numpy
matplotlib
seaborn
locust
tabulate
```

---

## 🚀 Execução

### Executar Todos os Cenários

O script automatizado executa **5 repetições** de cada cenário com reinicialização completa do ambiente:

```bash
chmod +x run_all_scenarios.sh
./run_all_scenarios.sh
```

> ⚠️ **Nota**: O script solicitará senha `sudo` a cada reinicialização do Docker (15 vezes no total).

### Cenários de Teste

| Cenário | Usuários | Ramp-up | Duração | Objetivo |
|---------|----------|---------|---------|----------|
| **🟢 Leve** | 50 | 10/s | 10 min | Operação normal |
| **🟡 Moderado** | 100 | 20/s | 10 min | Carga elevada |
| **🔴 Pico** | 200 | 40/s | 5 min | Stress máximo |

### Execução Manual

```bash
# Cenário Leve
locust -f locustfile.py --headless -u 50 -r 10 --run-time 10m \
  --csv results/leve/run_1 --host http://localhost:8080

# Cenário Moderado
locust -f locustfile.py --headless -u 100 -r 20 --run-time 10m \
  --csv results/medio/run_1 --host http://localhost:8080

# Cenário Pico
locust -f locustfile.py --headless -u 200 -r 40 --run-time 5m \
  --csv results/pico/run_1 --host http://localhost:8080
```

---

## 📊 Resultados

### Análise Consolidada

Após a execução, gere o relatório consolidado:

```bash
python analyze_results.py
```

### Métricas Obtidas

| Cenário | Usuários | Latência Média (ms) | Latência Máxima (ms) | Req/s | Taxa de Erro (%) |
|---------|----------|---------------------|----------------------|-------|------------------|
| **Leve** | 50 | 19.74 | 1,463.74 | 24.76 | 0.00 |
| **Moderado** | 100 | 50.20 | 10,082.75 | 48.75 | 53.99 |
| **Pico** | 200 | 81.81 | 10,174.99 | 96.09 | 68.87 |

### 📈 Interpretação

- ✅ **Cenário Leve**: Sistema estável, sem erros
- ⚠️ **Cenário Moderado**: Degradação significativa com 54% de falhas
- ❌ **Cenário Pico**: Sistema saturado com 69% de taxa de erro

### Estrutura de Arquivos

```
results/
├── leve/
│   ├── leve_stats_run_1_stats.csv
│   ├── leve_stats_run_2_stats.csv
│   └── ...
├── medio/
│   ├── medio_stats_run_1_stats.csv
│   └── ...
└── pico/
    ├── pico_stats_run_1_stats.csv
    └── ...

resultados_consolidados.csv  # Relatório final
```

---

## 🧪 Testes Manuais

### Criar Proprietários

```bash
curl -X POST http://localhost:8080/api/customer/owners \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Daniel",
    "lastName": "Rodrigues",
    "address": "Avenida Sul 3101",
    "city": "Picos",
    "telephone": "999999999"
  }'
```

### Consultar Dados

```bash
# Listar proprietários
curl http://localhost:8080/api/customer/owners

# Listar veterinários
curl http://localhost:8080/api/vet/vets

# Listar visitas
curl http://localhost:8080/api/visit/visits
```

---

## 🔍 Troubleshooting

### Containers não inicializam

```bash
# Verificar status
docker ps

# Verificar logs
docker logs <container-name>

# Reiniciar ambiente
cd spring-petclinic-microservices
sudo docker-compose down
sudo docker-compose up -d
```

### Alta taxa de erros

- Aumente o tempo de estabilização no script (padrão: 120s)
- Verifique recursos do sistema (CPU, RAM)
- Confirme que todos os serviços estão registrados no Eureka

### Conexão recusada

```bash
# Verifique se o API Gateway está respondendo
curl -I http://localhost:8080/api/customer/owners

# Aguarde mais tempo para inicialização
sleep 60
```

---

## 🛠️ Customização

### Adicionar Novos Endpoints

Edite `locustfile.py`:

```python
@task(2)
def get_pets(self):
    owner_id = random.randint(1, 200)
    self.client.get(f"/api/customer/owners/{owner_id}/pets", 
                    name="GET /owners/[id]/pets")
```

### Modificar Parâmetros de Carga

Edite `run_all_scenarios.sh`:

```bash
# Exemplo: 150 usuários, ramp-up 30/s, duração 15 minutos
locust -f $LOCUST_FILE --headless \
  -u 150 -r 30 --run-time 15m \
  --csv "results/custom/run_$i" \
  --host $HOST
```

---

## 📝 Notas Importantes

1. **Tempo de Execução**: O script completo leva ~3-4 horas (15 reinicializações + testes)
2. **Recursos**: Recomendado 8GB RAM e 4 CPUs para testes de pico
3. **Consistência**: Cada teste reinicia o Docker para garantir estado limpo
4. **Análise**: Use `analyze_results.py` apenas após conclusão de todos os testes

---

## 📄 Licença

Este projeto segue a licença do Spring PetClinic original.

---

## 👥 Contribuição

Desenvolvido para análise de performance de arquiteturas de microserviços baseadas em Spring Cloud.
Daniel Rodrigues
Rita Rodrigues
Walison Weudes

**Localização**: Picos, Piauí, BR

---

<div align="center">

**[⬆ Voltar ao topo](#-testes-de-performance---spring-petclinic-microservices)**

</div>