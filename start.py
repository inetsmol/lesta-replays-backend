# Создание структуры проекта
import os


def create_project_structure():
    """Создаёт базовую структуру проекта для сайта реплеев Мир Танков Lesta (.mtreplay)"""

    directories = [
        "./backend",
        "./backend/app",
        "./backend/app/api",
        "./backend/app/api/v1",
        "./backend/app/core",
        "./backend/app/db",
        "./backend/app/models",
        "./backend/app/services",
        "./backend/app/parsers",
        "./backend/app/utils",
        "./backend/app/schemas",
        "./backend/tests",
        "./frontend",
        "./frontend/src",
        "./frontend/src/components",
        "./frontend/src/pages",
        "./frontend/src/services",
        "./frontend/src/utils",
        "./frontend/public",
        "./uploads",
        "./static",
        "./static/images",
        "./static/maps",
        "./static/tanks"
    ]

    # Создаём директории
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Создана директория: {directory}")

    # Создаём основные файлы
    files_content = {
        "./requirements.txt": """# Backend зависимости
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
redis==5.0.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
aiofiles==23.2.0
Pillow==10.1.0
pydantic==2.5.0
pydantic-settings==2.1.0
pytest==7.4.3
pytest-asyncio==0.21.1
python-dotenv==1.0.0

# Специфичные зависимости для парсинга .mtreplay файлов
struct2==1.3.0
zlib2==1.0.0
json5==0.9.14
lxml==4.9.3
requests==2.31.0
""",

        "./docker-compose.yml": """version: '3.8'

services:
  # PostgreSQL база данных для Мир Танков Lesta
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: mt_replays_lesta
      POSTGRES_USER: mt_user
      POSTGRES_PASSWORD: mt_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  # Redis для кэширования
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  # FastAPI Backend
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://mt_user:mt_password@postgres:5432/mt_replays_lesta
      - REDIS_URL=redis://redis:6379
      - ALLOWED_EXTENSIONS=.mtreplay
    volumes:
      - ./uploads:/app/uploads
      - ./static:/app/static
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

volumes:
  postgres_data:
""",

        "./backend/Dockerfile": """FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем Python зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Создаём непривилегированного пользователя
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Запускаем приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
""",

        "./.env.example": """# База данных
DATABASE_URL=postgresql://wot_user:wot_password@localhost:5432/mt_replays_lesta

# Redis
REDIS_URL=redis://localhost:6379

# JWT настройки
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Файлы
UPLOAD_DIR=./uploads
STATIC_DIR=./static
MAX_FILE_SIZE=50000000  # 50MB
ALLOWED_EXTENSIONS=.mtreplay  # Только .mtreplay файлы Мир Танков Lesta

# API настройки
API_V1_STR=/api/v1
PROJECT_NAME=Мир Танков Lesta - Сайт Реплеев

# Lesta Games специфичные настройки
LESTA_API_URL=https://api.lesta.ru
SUPPORTED_GAME_VERSIONS=1.29.1,1.29.0,1.28.1  # Поддерживаемые версии МТ
""",

        "./.gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
.env

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Uploads
uploads/*
!uploads/.gitkeep

# Database
*.db
*.sqlite3

# Logs
*.log

# OS
.DS_Store
Thumbs.db

# Node.js (для фронтенда)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
""",

        "./README.md": """# Мир Танков Lesta - Сайт Реплеев

Веб-сайт для загрузки, просмотра и анализа реплеев Мир Танков от Lesta Games.

## Функционал

- 🔐 Аутентификация пользователей
- 📤 Загрузка .mtreplay файлов (Мир Танков Lesta)
- 📊 Парсинг и анализ реплеев MT
- 🔍 Поиск и фильтрация реплеев
- 👤 Профили игроков
- 📈 Статистика и рейтинги
- 🌍 Поддержка серверов Lesta Games

## Технологии

- **Backend**: FastAPI + PostgreSQL + Redis
- **Frontend**: React.js / HTML+JS
- **Контейнеризация**: Docker
- **Парсинг**: Специальные парсеры для .mtreplay

## Быстрый старт

1. Клонируйте репозиторий
2. Скопируйте `.env.example` в `.env` и настройте
3. Запустите: `docker-compose up -d`
4. Откройте http://localhost:8000

## Разработка

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск в режиме разработки
uvicorn app.main:app --reload
```

## Поддерживаемые форматы

- **.mtreplay** - основной формат реплеев Мир Танков Lesta
- Автоматическое определение версии клиента MT
- Поддержка всех серверов Lesta Games
"""
    }

    # Создаём файлы
    for file_path, content in files_content.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Создан файл: {file_path}")

    # Создаём пустые __init__.py файлы
    init_files = [
        "./backend/app/__init__.py",
        "./backend/app/api/__init__.py",
        "./backend/app/api/v1/__init__.py",
        "./backend/app/core/__init__.py",
        "./backend/app/db/__init__.py",
        "./backend/app/models/__init__.py",
        "./backend/app/services/__init__.py",
        "./backend/app/parsers/__init__.py",
        "./backend/app/utils/__init__.py",
        "./backend/app/schemas/__init__.py"
    ]

    for init_file in init_files:
        with open(init_file, 'w') as f:
            f.write("")
        print(f"Создан __init__.py: {init_file}")

    # Создаём .gitkeep файлы для пустых директорий
    gitkeep_dirs = [
        "./uploads",
        "./static/images",
        "./static/maps",
        "./static/tanks"
    ]

    for gitkeep_dir in gitkeep_dirs:
        with open(f"{gitkeep_dir}/.gitkeep", 'w') as f:
            f.write("")
        print(f"Создан .gitkeep в: {gitkeep_dir}")


if __name__ == "__main__":
    create_project_structure()
    print("\n✅ Базовая структура проекта для Мир Танков Lesta создана!")
    print("📂 Основные директории и файлы готовы")
    print("🐳 Docker-compose конфигурация настроена")
    print("📋 Requirements.txt с зависимостями для .mtreplay подготовлен")
    print("🎮 Поддержка файлов .mtreplay от Lesta Games")