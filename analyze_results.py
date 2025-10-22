import pandas as pd
import glob
import os
import numpy as np
from tabulate import tabulate

# Definindo a contagem de usuários diretamente para evitar o KeyError
# O valor é fixo por cenário (50, 100, 200) e não está no aggregated stats CSV
SCENARIOS = {
    "Leve": {"pattern": "results/leve/*_stats.csv", "users": 50},
    "Moderado": {"pattern": "results/medio/*_stats.csv", "users": 100},
    "Pico": {"pattern": "results/pico/*_stats.csv", "users": 200}
}
RESULT_METRICS = []

for scenario, data in SCENARIOS.items():
    pattern = data["pattern"]
    users = data["users"]
    
    all_files = glob.glob(pattern)
    
    if not all_files:
        print(f"Nenhum arquivo encontrado para o cenário {scenario}. Pulando.")
        continue

    # Filtrar a linha 'Aggregated' de cada CSV
    df_list = []
    for f in all_files:
        try:
            df = pd.read_csv(f)
            # Seleciona apenas a linha de agregação (resumo de todo o teste)
            aggregated_row = df.loc[df['Name'] == 'Aggregated']
            if not aggregated_row.empty:
                df_list.append(aggregated_row)
        except Exception as e:
            print(f"Aviso: Erro ao processar o arquivo {f}. {e}")
            
    if not df_list:
        continue

    combined_df = pd.concat(df_list)

    # Força a conversão de colunas para numérico
    combined_df['Average Response Time'] = pd.to_numeric(combined_df['Average Response Time'], errors='coerce')
    combined_df['Max Response Time'] = pd.to_numeric(combined_df['Max Response Time'], errors='coerce')
    combined_df['Requests/s'] = pd.to_numeric(combined_df['Requests/s'], errors='coerce')
    combined_df['Failure Count'] = pd.to_numeric(combined_df['Failure Count'], errors='coerce')
    combined_df['Request Count'] = pd.to_numeric(combined_df['Request Count'], errors='coerce')

    # Cálculos de Agregação
    avg_latency = combined_df['Average Response Time'].mean().round(2)
    # Usamos o MÁXIMO entre as 5 execuções para o pior caso
    max_latency = combined_df['Max Response Time'].max().round(2) 
    avg_req_s = combined_df['Requests/s'].mean().round(2)
    
    # Cálculo da taxa de erro baseada na soma total
    total_requests = combined_df['Request Count'].sum()
    total_failures = combined_df['Failure Count'].sum()
    
    if total_requests > 0:
        avg_failure_rate = (total_failures / total_requests) * 100
    else:
        avg_failure_rate = 0.0

    avg_data = {
        'Cenário': scenario,
        'Usuários': users, # Valor fixo inserido
        'Média Latência (ms)': avg_latency,
        'Máxima Latência (ms)': max_latency,
        'Requisições/s': avg_req_s,
        'Erros (%)': round(avg_failure_rate, 4) 
    }
    RESULT_METRICS.append(avg_data)

final_df = pd.DataFrame(RESULT_METRICS)

print("\n--- Tabela de Resultados Consolidados (Média das 5 Repetições) ---")
print(tabulate(final_df, headers='keys', tablefmt='pipe', showindex=False))

# Salva em um CSV final
final_df.to_csv("resultados_consolidados.csv", index=False)