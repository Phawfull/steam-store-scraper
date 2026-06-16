import requests
from bs4 import BeautifulSoup
import psycopg2
import re
import time

TOTAL_GAMES = 10000
BATCH_SIZE = 50

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
conn = psycopg2.connect(
    host="localhost",
    database="steamdb",
    user="postgres",
    password="Ar13737$",
    port="5432"
)

cursor = conn.cursor()

cursor.execute("DELETE FROM games")

highest_discount = 0
highest_discount_game = ""

highest_old_price = 0
highest_old_price_game = ""

highest_current_price = 0
highest_current_price_game = ""

highest_rating = 0
highest_rating_game = ""

lowest_rating = 100
lowest_rating_game = ""

most_reviews = 0
most_reviews_game = ""

for start in range(0, TOTAL_GAMES, BATCH_SIZE):

    url = (
        f"https://store.steampowered.com/search/results/"
        f"?query&start={start}&count={BATCH_SIZE}"
        f"&dynamic_data=&sort_by=_ASC"
        f"&snr=1_7_7_230_7"
        f"&supportedlang=english"
        f"&infinite=1"
    )

    response = requests.get(
        url,
        headers=headers
    )
    time.sleep(2)

    try:
        data = response.json()
    except:
        print("Failed at start =", start)
        print(response.text[:500])
        break

    html = data["results_html"]

    soup = BeautifulSoup(html, "html.parser")

    games = soup.find_all(
        "a",
        class_="search_result_row"
    )

    for game in games:

        title = game.find("span", class_="title")
        current_price = game.find("div", class_="discount_final_price")
        old_price = game.find("div", class_="discount_original_price")
        discount = game.find("div", class_="discount_pct")

        title_text = title.text.strip() if title else None

        current_price_text = (
            current_price.text.strip()
            if current_price else None
        )

        old_price_text = (
            old_price.text.strip()
            if old_price else None
        )

        discount_text = (
            discount.text.strip()
            if discount else None
        )

        review = game.find(
            "span",
            class_="search_review_summary"
        )

        positive_percentage = None
        review_count = None

        if review:

            tooltip = review.get(
                "data-tooltip-html",
                ""
            )

            percentage_match = re.search(
                r"(\d+)%",
                tooltip
            )

            review_count_match = re.search(
                r"of the ([\d,]+) user reviews",
                tooltip
            )

            if percentage_match:
                positive_percentage = int(
                    percentage_match.group(1)
                )

            if review_count_match:
                review_count = int(
                    review_count_match.group(1)
                    .replace(",", "")
                )

        cursor.execute(
            """
            INSERT INTO games
            (
                title,
                current_price,
                old_price,
                discount_percentage,
                positive_percentage,
                review_count
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                title_text,
                current_price_text,
                old_price_text,
                discount_text,
                positive_percentage,
                review_count
            )
        )

        if discount_text:

            try:

                discount_number = int(
                    discount_text
                    .replace("-", "")
                    .replace("%", "")
                )

                if discount_number > highest_discount:
                    highest_discount = discount_number
                    highest_discount_game = title_text

            except:
                pass

        if old_price_text:

            try:

                old_price_number = float(
                    old_price_text
                    .replace("₹", "")
                    .replace(",", "")
                )

                if old_price_number > highest_old_price:
                    highest_old_price = old_price_number
                    highest_old_price_game = title_text

            except:
                pass

        if current_price_text:

            try:

                current_price_number = float(
                    current_price_text
                    .replace("₹", "")
                    .replace(",", "")
                )

                if current_price_number > highest_current_price:
                    highest_current_price = current_price_number
                    highest_current_price_game = title_text

            except:
                pass

        if positive_percentage is not None:

            if positive_percentage > highest_rating:
                highest_rating = positive_percentage
                highest_rating_game = title_text

            if positive_percentage < lowest_rating:
                lowest_rating = positive_percentage
                lowest_rating_game = title_text

        if review_count is not None:

            if review_count > most_reviews:
                most_reviews = review_count
                most_reviews_game = title_text

conn.commit()

print("\nRESULTS\n")

print(
    f"Highest Discount: "
    f"{highest_discount_game} ({highest_discount}%)"
)

print(
    f"Most Expensive Before Discount: "
    f"{highest_old_price_game} (₹{highest_old_price})"
)

print(
    f"Most Expensive After Discount: "
    f"{highest_current_price_game} (₹{highest_current_price})"
)

print(
    f"Highest Rated Game: "
    f"{highest_rating_game} ({highest_rating}%)"
)

print(
    f"Lowest Rated Game: "
    f"{lowest_rating_game} ({lowest_rating}%)"
)

print(
    f"Most Reviewed Game: "
    f"{most_reviews_game} ({most_reviews:,} reviews)"
)

cursor.close()
conn.close()