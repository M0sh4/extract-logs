#!/bin/bash

# Define la ruta del log
cd /var/opt/extract-logs-dry-run/
logfile="/var/opt/extract-logs-dry-run/cashin-prod/logs/logs_extract_$(date +%Y%m%d).log"

# Ejecuta el script Python y redirige la salida al archivo de log
/usr/bin/python3.9 /var/opt/extract-logs-dry-run/cashin-prod/extract-logs.py >> "$logfile" 2>&1