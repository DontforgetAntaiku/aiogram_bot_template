# Aiogram Bot Template

A starter template for building Telegram bots using the Aiogram framework. This template provides a clean project structure, environment configuration, and optional Docker support for deploying bots with either long polling or webhook mode.

## Features

- Asynchronous bot powered by Aiogram (asyncio & aiohttp)
- Environment variable management with `.env`
- Docker and Docker Compose configuration for containerized deployment
- Structured project layout for handlers, middlewares, and utilities

## Requirements

- Python 3.8 or higher
- Git
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DontforgetAntaiku/aiogram_bot_template.git
   cd aiogram_bot_template
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the example environment file and edit:
   ```bash
   cp .env.example .env
   ```
2. Set the required variables in `.env`:
  ```dotenv
  # TgBot
  BOT_TOKEN=
  REDIS_HOST=
  REDIS_PORT=
  # DataBase
  DB_USER=
  DB_PASSWORD=
  DB_HOST=
  DB_PORT=
  DB_NAME=
  # Webhook
  WEB_SERVER_HOST=
  WEB_SERVER_PORT=
  WEBHOOK_PATH=
  BASE_URL=
  X_Telegram_Bot_Api_Secret_Token=
  ```

## Usage

### Webhook Mode

1. Ensure your server is reachable via HTTPS.
2. Run the bot:
   ```bash
   python main.py
   ```
3. The bot will set up the webhook at the URL defined in `.env`.


## Project Structure

```
aiogram_bot_template/
├── app/
│   ├── config.py
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   ├── dialogs/
│   │   ├── admin/
│   │   ├── states.py
│   │   └── user/
│   ├── filters/
│   │   └── filters.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── keyboards/
│   │   ├── inline.py
│   │   └── reply.py
│   ├── middlewares/
│   │   ├── config.py
│   │   └── errors.py
│   ├── services/
│   │   ├── classes/
│   │   │   ├── config_factory.py
│   │   │   ├── dynamicattrs.py
│   │   │   ├── errors.py
│   │   │   ├── __init__.py
│   │   │   └── singleton.py
│   │   └── services.py
│   └── site_functions/
│       ├── handlers/
│       │   └── handlers.py
│       └── middlewares/
│           └── inject.py
├── main.py
└── requirements.txt
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for bug fixes, enhancements, or documentation improvements.
