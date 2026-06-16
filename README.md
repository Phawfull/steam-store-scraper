# Steam Data Analyzer

A Python-based web scraping and data analysis project that collects game information from the Steam Store, stores it in PostgreSQL, and performs analytics on pricing, discounts, ratings, and reviews.

## Features

* Scrapes Steam Store game data using Requests and BeautifulSoup
* Uses Steam's paginated API endpoint to collect large datasets
* Stores data in PostgreSQL
* Extracts:

  * Game Title
  * Current Price
  * Original Price
  * Discount Percentage
  * Positive Review Percentage
  * Review Count
* Performs analytics such as:

  * Highest Discounted Game
  * Most Expensive Game Before Discount
  * Most Expensive Game After Discount
  * Highest Rated Game
  * Lowest Rated Game
  * Most Reviewed Game

## Technologies Used

* Python
* Requests
* BeautifulSoup4
* PostgreSQL
* psycopg2

## Database Schema

| Column              | Type               |
| ------------------- | ------------------ |
| id                  | SERIAL PRIMARY KEY |
| title               | TEXT               |
| current_price       | TEXT               |
| old_price           | TEXT               |
| discount_percentage | TEXT               |
| positive_percentage | INTEGER            |
| review_count        | INTEGER            |

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the PostgreSQL table:

```sql
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    title TEXT,
    current_price TEXT,
    old_price TEXT,
    discount_percentage TEXT,
    positive_percentage INTEGER,
    review_count INTEGER
);
```

Update the PostgreSQL connection details in the script before running.

## Running the Project

```bash
python scraper.py
```

## Sample Analytics Output

```text
Highest Discount: Destiny 2: The Witch Queen (95%)

Most Expensive Before Discount:
Digimon Story Time Stranger (₹6399)

Most Expensive After Discount:
RealFlight Evolution (₹10874)

Highest Rated Game:
Example Game (100%)

Lowest Rated Game:
Example Game (24%)

Most Reviewed Game:
Counter-Strike 2 (2,556,743 reviews)
```

## Learning Outcomes

This project demonstrates:

* Web Scraping
* HTML Parsing
* JSON API Handling
* Data Cleaning
* PostgreSQL Integration
* SQL Operations
* Data Analysis with Python
* Pagination and Large Dataset Collection
