import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from datetime import datetime, timedelta
import time
import pytz

# Parámetros de configuración
bucket_name = 'pdp-exported-logs'  # Cambia esto por tu bucket
log_directory = 'log'  # Ruta a los archivos de log
service_name = 'cashin_prod'

# Rango de horas (definir el rango como hora de inicio y fin)
now = datetime.now()
print(now)
cut_off_time = now - timedelta(hours=1)
log_name_filter = f"log_mdw_pdp.log.{cut_off_time.year}-{cut_off_time.month:02}-{cut_off_time.day:02}"

# Configurar el cliente de S3
s3_client = boto3.client('s3')
prefix = f"{service_name}/{cut_off_time.year}/{cut_off_time.month:02}/{cut_off_time.day:02}/{cut_off_time.hour}/"

# Función para cargar un archivo a S3
def upload_to_s3(file_path, bucket_name):
    try:
        # Obtener el nombre del archivo
        file_name = os.path.basename(file_path)
        s3_client.upload_file(file_path, bucket_name, prefix + file_name)
    except Exception as e:
        print(now, f"Ocurrió un error al cargar el archivo: {str(e)}")

# Función principal para recorrer los logs y subirlos
def upload_logs_to_s3(log_directory, bucket_name):
    try:
        start_time = time.time()
        files_count = 0
        for root, dirs, files in os.walk(log_directory):
            for file in files:
                files_count+=1
                if file.startswith(log_name_filter):
                    hour = get_hour_minute(file)
                    if int(hour) == cut_off_time.hour:
                        print(os.path.join(root, file))
                        file_path = os.path.join(root, file)
                        upload_to_s3(file_path, bucket_name)
        print(now,"Archivos subidos:",files_count)
        print(now, "Time: ", time.time() - start_time)
    except Exception as e:
        print(now, f"Ocurrio un error al filtrar archivos: {str(e)}")
                
def get_hour_minute(log_name):
    hour_minute = log_name[-5:]
    return hour_minute.split("-")[0]

# Ejecutar el script
if __name__ == "__main__":
    upload_logs_to_s3(log_directory, bucket_name)
