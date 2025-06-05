.PHONY: help build up down logs clean install test format lint

# デフォルトターゲット
help:
	@echo "Available commands:"
	@echo "  build    - Build Docker containers"
	@echo "  up       - Start services with Docker Compose"
	@echo "  down     - Stop services"
	@echo "  logs     - Show logs"
	@echo "  clean    - Clean up containers and volumes"
	@echo "  install  - Install dependencies locally"
	@echo "  test     - Run tests"
	@echo "  format   - Format code"
	@echo "  lint     - Run linter"
	@echo "  dev      - Start development server locally"
	@echo ""
	@echo "Troubleshooting:"
	@echo "  status   - Show container status"
	@echo "  check    - Test API health"
	@echo "  debug    - Show detailed logs"
	@echo "  reset    - Complete reset and rebuild"
	@echo "  test-api - Test API endpoints"
	@echo ""
	@echo "Database:"
	@echo "  db-connect - Connect to PostgreSQL"
	@echo "  db-status  - Show database tables"
	@echo "  db-backup  - Backup database"

# Docker関連
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

# ローカル開発
install:
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# テスト・品質
test:
	pytest

format:
	black app/
	isort app/

lint:
	flake8 app/

# データベース関連
db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

db-reset:
	docker-compose down
	docker volume rm sample-fastapi_postgres_data
	docker-compose up -d

# 完全セットアップ
setup:
	cp .env.example .env
	$(MAKE) install
	$(MAKE) build
	$(MAKE) up
	@echo "Setup complete! API is running at http://localhost:8000"
	@echo "API docs available at http://localhost:8000/docs"

# トラブルシューティング
status:
	docker-compose ps

check:
	curl -f http://localhost:8000/health || echo "API not responding"

reset:
	docker-compose down -v
	docker system prune -f
	$(MAKE) build
	$(MAKE) up

debug:
	@echo "=== Container Status ==="
	docker-compose ps
	@echo "\n=== Application Logs ==="
	docker-compose logs --tail=20 app
	@echo "\n=== Database Logs ==="
	docker-compose logs --tail=10 db

test-api:
	@echo "Testing API endpoints..."
	curl -s http://localhost:8000/health && echo " ✅ Health check OK"
	curl -s http://localhost:8000/ && echo " ✅ Root endpoint OK"

# データベース関連
db-connect:
	docker-compose exec db psql -U postgres -d sample_db

db-status:
	docker-compose exec db psql -U postgres -d sample_db -c "\dt"

db-backup:
	docker-compose exec db pg_dump -U postgres sample_db > backup.sql
