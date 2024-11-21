cd /var/opt/extract-logs-dry-run/

logfile="/var/opt/extract-logs-dry-run/pago-credito-fcompartamos/logs/logs_extract_$(date +%Y%m%d).log"

source /var/opt/extract-logs-dry-run/env/bin/activate

python /var/opt/extract-logs-dry-run/pago-credito-fcompartamos/extract-logs.py >> "$logfile" 2>&1

deactive