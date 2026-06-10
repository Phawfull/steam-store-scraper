import requests
from bs4 import BeautifulSoup
import psycopg2

url = "https://store.steampowered.com/search/?term=action"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

titles = soup.find_all("span", class_="title")
prices = soup.find_all("div", class_="discount_final_price")

conn = psycopg2.connect(
    host="localhost",
    database="steamdb",
    user="postgres",
    password="your_password",
    port="5432"
)

cursor = conn.cursor()

cursor.execute("DELETE FROM games")

for title, price in zip(titles, prices):
    cursor.execute(
        "INSERT INTO games (title, price) VALUES (%s, %s)",
        (title.text.strip(), price.text.strip())
    )

conn.commit()

cursor.execute("SELECT * FROM games")

for game_id, title, price in cursor.fetchall():
    print(f"{game_id} | {title} | {price}")

print(f"\nTotal Games: {len(titles)}")

cursor.close()
conn.close()