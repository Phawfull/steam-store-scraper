# Steam Web Scraper

This project scrapes game titles and prices from the Steam Store using BeautifulSoup and stores them in PostgreSQL.

## Technologies
- Python
- BeautifulSoup
- PostgreSQL
- psycopg2

## How to Run

1. Install dependencies
2. Create PostgreSQL database `steamdb`
3. Create table `games`
4. Update database password in `scraper.py`
5. Run:

python scraper.py