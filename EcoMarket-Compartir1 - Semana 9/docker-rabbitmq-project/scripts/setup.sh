#!/bin/bash

# This script sets up the RabbitMQ environment and performs initial configuration tasks.

# Start RabbitMQ service
docker-compose up -d rabbitmq

# Wait for RabbitMQ to start
echo "Waiting for RabbitMQ to start..."
sleep 10

# Load definitions into RabbitMQ
if [ -f ../rabbitmq/definitions.json ]; then
  echo "Loading RabbitMQ definitions..."
  curl -u user:pass -H "Content-Type: application/json" -X POST -d @../rabbitmq/definitions.json http://localhost:15672/api/definitions
else
  echo "Definitions file not found."
fi

echo "RabbitMQ setup completed."