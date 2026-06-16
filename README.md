Steam Data Analyzer

A Python-based web scraping and data analysis project that collects game information from the Steam Store, stores it in PostgreSQL, and performs analytics on pricing, discounts, ratings, and reviews.

Features
Scrapes Steam Store game data using Requests and BeautifulSoup
Uses Steam's paginated API endpoint to collect large datasets
Stores data in PostgreSQL
Extracts:
Game Title
Current Price
Original Price
Discount Percentage
Positive Review Percentage
Review Count
Performs analytics such as:
Highest Discounted Game
Most Expensive Game Before Discount
Most Expensive Game After Discount
Highest Rated Game
Lowest Rated Game
Most Reviewed Game
Average Game Price
Average Discount Percentage
Technologies Used
Python
Requests
BeautifulSoup4
PostgreSQL
psycopg2
Installation

Clone the repository:

git clone <repository-url>
cd <repository-name>

Install dependencies:

pip install -r requirements.txt
Database Setup

Create a PostgreSQL database named:

steamdb

Create the required table:

DROP TABLE IF EXISTS games;

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    title TEXT,
    current_price TEXT,
    old_price TEXT,
    discount_percentage TEXT,
    positive_percentage INTEGER,
    review_count INTEGER
);

Update the PostgreSQL connection details inside scraper.py:

conn = psycopg2.connect(
    host="localhost",
    database="steamdb",
    user="postgres",
    password="YOUR_PASSWORD",
    port="5432"
)
Running the Project
python scraper.py
Analytics Generated

The program automatically calculates:

Highest Discounted Game
Most Expensive Game Before Discount
Most Expensive Game After Discount
Highest Rated Game
Lowest Rated Game
Most Reviewed Game
Average Game Price
Average Discount Percentage
Sample Output
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

Average Price:
₹1245.67

Average Discount:
42.18%
Learning Outcomes

This project demonstrates:

Web Scraping
HTML Parsing
JSON API Handling
PostgreSQL Integration
SQL Operations
Data Cleaning
Data Analysis
Pagination
API Rate Limiting Considerations