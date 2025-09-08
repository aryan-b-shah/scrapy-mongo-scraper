#!/usr/bin/env bash
set -euo pipefail

# 1) Python env
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

# 2) Deps
pip install -U pip
pip install -r requirements.txt

# 3) Local Mongo via Docker (optional)
if command -v docker >/dev/null 2>&1; then
  echo "Starting local MongoDB with Docker Compose..."
  docker compose up -d
else
  echo "Docker not found. Assuming MongoDB is already running locally."
fi

# 4) Env
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

# 5) Crawl
pushd scraper >/dev/null
mkdir -p output
scrapy crawl quotes
popd >/dev/null

echo "Done. Check 'scraper/output/quotes.json' and MongoDB 'scrapy_demo.quotes'."
