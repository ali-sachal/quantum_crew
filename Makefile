.PHONY: help install seed run-backend run-frontend run test docker-up docker-down

help:
	@echo "FoodMatch Makefile Commands:"
	@echo "  make install        - Install backend and frontend dependencies"
	@echo "  make seed           - Seed database with demo farmers, stores, listings"
	@echo "  make run-backend    - Start FastAPI backend server"
	@echo "  make run-frontend   - Start Vite React frontend"
	@echo "  make test           - Run backend unit and integration tests"
	@echo "  make docker-up      - Launch full stack via docker-compose"
	@echo "  make docker-down    - Stop docker-compose services"

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

seed:
	cd backend && python -m app.seed

run-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-frontend:
	cd frontend && npm run dev

test:
	cd backend && pytest -v tests/

docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down

