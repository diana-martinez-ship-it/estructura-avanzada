# Docker RabbitMQ Project

This project sets up a RabbitMQ server using Docker Compose with management capabilities. Below are the details for each component of the project.

## Project Structure

```
docker-rabbitmq-project
├── docker-compose.yml       # Defines the RabbitMQ service and its configuration
├── .env                     # Environment variables for the project
├── .gitignore               # Files and directories to be ignored by Git
├── rabbitmq
│   ├── definitions.json     # RabbitMQ definitions (exchanges, queues, bindings)
│   └── enabled_plugins      # List of enabled RabbitMQ plugins
├── scripts
│   └── setup.sh             # Shell script for setting up the RabbitMQ environment
├── tests
│   └── integration          # Directory for integration tests
└── README.md                # Documentation for the project
```

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd docker-rabbitmq-project
   ```

2. Configure environment variables in the `.env` file as needed.

3. Start the RabbitMQ service:
   ```
   docker-compose up -d
   ```

4. Access the RabbitMQ management interface at `http://localhost:15672` using the credentials defined in the `docker-compose.yml` file.

### Usage

- Use the RabbitMQ management interface to create exchanges, queues, and bindings as needed.
- Modify the `definitions.json` file to pre-load configurations into RabbitMQ.

### Running Tests

Integration tests can be found in the `tests/integration` directory. Ensure the RabbitMQ service is running before executing the tests.

### Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.

### License

This project is licensed under the MIT License.