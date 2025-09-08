# Scrapy + MongoDB (Local) Demo

A simple Scrapy spider that crawls [quotes.toscrape.com], extracts quotes, and stores them locally in MongoDB with idempotent upserts. Also exports `scraper/output/quotes.json` for quick inspection.

## Author
- Aryan Shah

## Stack
- Scrapy (crawling & parsing)
- MongoDB (local via Docker Compose or native install)
- Upserts + index (no duplicates on re-run)
- AutoThrottle + polite delays + HTTP cache

## Run locally

### Quick Start
```bash
# from repo root
chmod +x run_local.sh
./run_local.sh
```

### Manual Steps
```bash
# 1. Setup Python environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start MongoDB (choose one)
# Option A: Docker Compose (recommended)
docker compose up -d

# Option B: Native MongoDB
# Install MongoDB locally and start the service

# 4. Configure environment
cp .env.example .env
# Edit .env if needed

# 5. Run the scraper
cd scraper
scrapy crawl quotes
```

## What it does

1. **Crawls** quotes.toscrape.com with pagination
2. **Extracts** for each quote:
   - `text`: The quote text
   - `author`: Author name
   - `tags`: List of tags
   - `source_url`: Page URL where quote was found
3. **Stores** in MongoDB with upsert (no duplicates)
4. **Exports** JSON file to `scraper/output/quotes.json`

## Project Structure

```
scrapy-mongo-scraper/
├─ README.md
├─ requirements.txt
├─ .env.example
├─ docker-compose.yml
├─ run_local.sh
└─ scraper/
   ├─ scrapy.cfg
   └─ scraper/
      ├─ __init__.py
      ├─ items.py
      ├─ pipelines.py
      ├─ settings.py
      ├─ middlewares.py
      └─ spiders/
         └─ quotes_spider.py
```

## Configuration

### Environment Variables (.env)
```bash
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=scrapy_demo
MONGODB_COLLECTION=quotes
```

### Scrapy Settings
- **DOWNLOAD_DELAY**: 0.25s between requests
- **AUTOTHROTTLE**: Adaptive delays based on response times
- **HTTPCACHE**: Enabled for development (disable in production)
- **ROBOTSTXT_OBEY**: Respects robots.txt

## MongoDB

### View Data
```bash
# Connect to MongoDB
mongosh

# Switch to database
use scrapy_demo

# View quotes
db.quotes.find().pretty()

# Count quotes
db.quotes.countDocuments()

# Find by author
db.quotes.find({"author": "Albert Einstein"})
```

### Indexes
- Compound index on `(text, author)` for duplicate prevention
- Automatically created on first run

## Output Files

- `scraper/output/quotes.json`: JSON export of all scraped quotes
- `scraper/httpcache/`: HTTP cache directory (can be deleted)

## Ethical Notes

- ✅ Uses polite delays (0.25s minimum)
- ✅ Respects robots.txt
- ✅ Adaptive throttling
- ✅ Only scrapes public practice site
- ✅ No personal data collection
- ✅ Local-only storage

## Development

### Run with custom settings
```bash
cd scraper
scrapy crawl quotes -s DOWNLOAD_DELAY=1.0
```

### Debug mode
```bash
cd scraper
scrapy crawl quotes -L DEBUG
```

### Check MongoDB connection
```python
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client.scrapy_demo
print(db.quotes.count_documents({}))
```

## Troubleshooting

### MongoDB Connection Issues
1. Ensure MongoDB is running: `docker compose ps`
2. Check connection: `mongosh mongodb://localhost:27017`
3. Verify .env file exists and has correct URI

### Scrapy Issues
1. Check logs for specific errors
2. Verify internet connection
3. Try running with `-L DEBUG` for verbose output

### Permission Issues
1. Make run script executable: `chmod +x run_local.sh`
2. Check Python virtual environment activation
