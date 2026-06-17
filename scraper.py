import requests
from bs4 import BeautifulSoup
import psycopg2
import re   #regular expressions (used to search and filter text)
import time

TOTAL_GAMES = 10000
BATCH_SIZE = 50

headers = {   #a dictionary is created which is used to contact steam, If not used steam detects it as bot.
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
conn = psycopg2.connect(
    host="localhost",
    database="steamdb",
    user="postgres",
    password="YOUR_PASSWORD",
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

for start in range(0, TOTAL_GAMES, BATCH_SIZE):   #takes 50 games at a time

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
        headers=headers   #passing the header dictionary we made into the header parameter of request.get to avoid bot detection
    )
    time.sleep(1)  #1 second given btw every set of request to avoid bot detection

    try:
        data = response.json()    #STEAM returns response.txt which is a string, this converts the string into a dictionary.
    
    except:
        print("Failed at start =", start)  #prints which number of game it failed at.
        print(response.text[:500])  #returns what steam returns in the case of failure. 500 words cuz the error statement might be very long.
        break

    html = data["results_html"]    #gives the value pair of results_html, which is a big HTML line with all the data.

    soup = BeautifulSoup(html, "html.parser")  #we parse the HTML data.

    games = soup.find_all(
        "a",
        class_="search_result_row" #In the list games, it finds all the games using soup inside the class "search_result_row", IT CONTAINS all information about the game. 
    )                              #name, price, discount etc

    for game in games:

        title = game.find("span", class_="title")  #looks for "title" in the games HTML to find the name                                           
        current_price = game.find("div", class_="discount_final_price")  #looks for discount_final_price in games html 
        old_price = game.find("div", class_="discount_original_price")  #these 4 lines still return HTML string just filtered. it shows 
        discount = game.find("div", class_="discount_pct")  

        title_text = title.text.strip()    #.text gives back only text to it removes the <span> and <a> and all.
                                                             # .strip() just strips down the spaces on both sides just giving the name.
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

        if review is not None:

            tooltip = review.get(                #we use .get() as it returns the attribute which is inside "data-tooltip-html" and .find() returns the whole HTML tag
                "data-tooltip-html",             #we do not need the whole HTML tag as it is already stored inside review.
                ""                               #empty string cuz if data-tooltip-html is empty, it returns emptry string rather than error.
            )                                    #Now tooltip has the string "Very positive<br>95% of the 12,374 user reviews"

            percentage_match = re.search(        #re.search(pattern,text) so r"(\d+)% is the pattern and tooltop is the text. (search pattern from text.)
                r"(\d+)%",                       # r"" means raw string. (\d means any digit.) "+" means one or more digits.  "%" means a literal percentage sign.
                tooltip                          # so r"(\d+)%" matches 95%, d+ points to 95, % to % 
            )                                    # we put the () before % so it only stores the numerical part and not the %, so its easier for calculations.
                                                 # the () makes a group call it group(1). Which is just 95.
            review_count_match = re.search(
                r"of the ([\d,]+) user reviews",
                tooltip
            )

            if percentage_match:                 # checks if percentage_match contains a match object, if yes it runs
                positive_percentage = int(
                    percentage_match.group(1)    # calls group(1) which is 95 for the above example. originally a string but converted into int
                )

            if review_count_match:
                review_count = int(
                    review_count_match.group(1)
                    .replace(",", "")            #suppose group(1) returns 12,234, this replaces the , with empty so it becomes 12234. .replace(old,new)
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
