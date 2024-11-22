import os
import boto3
from datetime import datetime, timedelta
import time

bucket_name = 'pdp-exported-logs'
log_directory = 'log'
service_name = 'cashin_prod'

now = datetime.now()
print(now)
cut_off_time = now - timedelta(hours=1)
log_name_filter = f"log_mdw_pdp.log.{cut_off_time.year}-{cut_off_time.month:02}-{cut_off_time.day:02}"
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '/dev/null' #ayuda a no usar ninguna credencial configurada por default en la pc/servidor

s3_client = boto3.client('s3')
prefix = f"{service_name}/{cut_off_time.year}/{cut_off_time.month:02}/{cut_off_time.day:02}/{cut_off_time.hour}/"

def upload_to_s3(file_path, bucket_name):
    try:
        file_name = os.path.basename(file_path)
        s3_client.upload_file(file_path, bucket_name, prefix + file_name)
    except Exception as e:
        print(now, f"Ocurrió un error al cargar el archivo: {str(e)}")

def upload_logs_to_s3(log_directory, bucket_name):
    try:
        start_time = time.time()
        files_count = 0
        errors_count = 0
        for root, dir, files in os.walk(log_directory):
            for file in files:
                if file.startswith(log_name_filter):
                    hour = get_hour_minute(file)
                    if int(hour) == cut_off_time.hour:
                        try:
                            files_count+=1
                            print(os.path.join(root, file))
                            file_path = os.path.join(root, file)
                            upload_to_s3(file_path, bucket_name)
                        except e:
                            errors_count+=1
                            print(e)
                            
        print(now,"Archivos subidos: ",files_count)
        print(now, "Archivos errados: ", errors_count)
        print(now, "Time: ", time.time() - start_time)
    except Exception as e:
        print(now, f"Ocurrio un error al filtrar archivos: {str(e)}")

def get_hour_minute(log_name):
    hour_minute = log_name[-5:]
    return hour_minute.split("-")[0]

if __name__ == "__main__":
    upload_logs_to_s3(log_directory, bucket_name)
