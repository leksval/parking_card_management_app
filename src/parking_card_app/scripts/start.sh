#!/bin/bash

# Run initial expiration check
python /app/scripts/expiration_check.py

# Setup daily cron job
echo "0 8 * * * cd /app && python /app/scripts/expiration_check.py >> /var/log/cron.log 2>&1" | crontab -

# Start cron service
service cron start

# Start the main application
uvicorn main:app --host 0.0.0.0 --port 8000
