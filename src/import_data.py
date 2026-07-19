import os
from google.cloud import bigquery
import pandas as pd
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("GCP_DATASET_ID")

# Инициализируем клиент BigQuery
client = bigquery.Client(project=PROJECT_ID)

def upload_huge_csv_to_bigquery(file_path, table_name, chunk_size=100000):
    dataset_ref = client.dataset(DATASET_ID)
    table_ref = dataset_ref.table(table_name)
    
    # Конфигурация загрузки
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND", 
        autodetect=True  # Автоматически определит типы колонок
    )
    
    print(f"Начинаем обработку большого файла: {file_path}")
    
    chunk_count = 0
    # Читаем файл порциями по chunk_size строк
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunk_count += 1
        print(f"Отправляем чанк №{chunk_count} ({len(chunk)} строк) в BigQuery...")
        
        # Загружаем текущий кусочек в BigQuery
        job = client.load_table_from_dataframe(chunk, table_ref, job_config=job_config)
        job.result()  # Ждем завершения загрузки текущего чанка
        
    print(f"🎉 Успех! Все чанки загружены в таблицу {DATASET_ID}.{table_name}")

if __name__ == "__main__":
    # Указываем путь к первому распакованному файлу
    csv_path = "data/raw/2019-Oct.csv" 
    table_name = "raw_clickstream"
    
    # Вызов функции без комментариев
    upload_huge_csv_to_bigquery(csv_path, table_name)