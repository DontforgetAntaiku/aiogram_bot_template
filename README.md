# Aiogram Bot Template

A starter template for building Telegram bots using the Aiogram framework with webhook mode. This template provides a clean project structure, environment configuration, and Docker support for containerized deployment.

## Features

- Asynchronous bot powered by Aiogram (asyncio & aiohttp)
- Webhook mode with aiohttp web server
- Environment variable management with `.env`
- PostgreSQL database with Tortoise ORM and Aerich migrations
- Redis-based FSM storage
- Docker and Docker Compose for containerized deployment
- Structured project layout for handlers, middlewares, dialogs, and utilities
- aiogram-dialog support

## Requirements

- Python 3.9 or higher
- PostgreSQL
- Redis
- Git

## Installation

### Using pip

1. Clone the repository:
   ```bash
   git clone https://github.com/DontforgetAntaiku/aiogram_bot_template.git
   cd aiogram_bot_template
   ```
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

### Using uv

1. Clone the repository:
   ```bash
   git clone https://github.com/DontforgetAntaiku/aiogram_bot_template.git
   cd aiogram_bot_template
   ```
2. Install dependencies (uv will create the virtual environment automatically):
   ```bash
   uv sync
   ```
   Or if you only have `requirements.txt`:
   ```bash
   uv pip install -r requirements.txt
   ```

### Using Poetry

1. Clone the repository:
   ```bash
   git clone https://github.com/DontforgetAntaiku/aiogram_bot_template.git
   cd aiogram_bot_template
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```

## Configuration

1. Copy the example environment file and edit:
   ```bash
   cp .env.example .env
   ```
2. Set the required variables in `.env`:
   ```dotenv
   # bot
   BOT_TOKEN=
   # redis
   REDIS_HOST=
   REDIS_PORT=
   # database
   DB_USER=
   DB_PASSWORD=
   DB_HOST=
   DB_PORT=
   DB_NAME=
   # webhook
   WEBHOOK_HOST=
   WEBHOOK_PORT=
   WEBHOOK_PATH=
   WEBHOOK_BASE_URL=
   WEBHOOK_X_Telegram_Bot_Api_Secret_Token=
   ```

## Usage

### Running locally

1. Ensure your server is reachable via HTTPS (use [ngrok](https://ngrok.com/) for local testing).
2. Run the bot:
   ```bash
   python main.py
   ```
3. The bot will set up the webhook at the URL defined in `.env`.

### Running with Docker Compose

1. Make sure Docker and Docker Compose are installed.
2. Configure your `.env` file (see [Configuration](#configuration)).
3. Start all services:
   ```bash
   docker compose up -d
   ```
   This will start the bot along with PostgreSQL and Redis containers.

4. View logs:
   ```bash
   docker compose logs -f bot
   ```

5. Stop all services:
   ```bash
   docker compose down
   ```

## Project Structure

```
aiogram_bot_template
├── app
│   ├── bot
│   │   ├── dialogs
│   │   │   └── states.py
│   │   ├── filters
│   │   │   └── filters.py
│   │   ├── handlers
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   └── keyboards
│   │       ├── inline.py
│   │       └── reply.py
│   ├── core
│   │   └── __init__.py
│   ├── database
│   │   ├── __init__.py
│   │   └── models.py
│   ├── site
│   │   └── routers
│   │       └── main
│   │           └── view.py
│   └── utils
│       ├── classes
│       │   ├── config_factory.py
│       │   ├── config.py
│       │   ├── dynamicattrs.py
│       │   ├── __init__.py
│       │   └── services.py
│       ├── exceptions
│       │   └── __init__.py
│       └── middlewares
│           ├── bot
│           │   ├── errors.py
│           │   └── __init__.py
│           └── site
│               ├── __init__.py
│               └── inject.py
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── main.py
├── README.md
└── requirements.txt
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for bug fixes, enhancements, or documentation improvements.
