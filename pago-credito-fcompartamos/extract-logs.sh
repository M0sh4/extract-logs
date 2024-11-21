cd /var/opt/extract-logs-dry-run/

logfile="/var/opt/extract-logs-dry-run/pago-credito-fcompartamos/logs/logs_extract_$(date +%Y%m%d).log"

source ./var/opt/env/bin/activate

/usr/bin/python3.9 /var/opt/extract-logs-dry-run/pago-credito-fcompartamos/extract-logs.py >> "$logfile" 2>&1