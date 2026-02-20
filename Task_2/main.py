import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"  # creating BASE_URL as cycle will occur by url and when next page, url will change
url = BASE_URL

quotes_data = []
authors_data = []
authors_cache = set()

page_number = 1

print("Start")  # log to see what is happening

while url:  # cycle
    print(f"\n📄 Processing page {page_number}: {url}")  # log

    try:
        response = requests.get(url, timeout=10)
        print(f"Status code: {response.status_code}")  # 200

        if response.status_code != 200:  # if not 200 - shut down
            print("HTML is not 200")
            break

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        break

    soup = BeautifulSoup(response.text, "lxml")

    quotes = soup.find_all("div", class_="quote")

    for i, quote in enumerate(quotes, start=1):

        text = quote.find("span", class_="text").text
        author = quote.find("small", class_="author").text
        tags = [tag.text for tag in quote.find_all("a", class_="tag")]

        quotes_data.append({"tags": tags, "author": author, "quote": text})

        if author not in authors_cache:
            print(f"New author: {author}")  # log

            author_link = quote.find("a")["href"]
            author_url = BASE_URL + author_link

            try:
                author_response = requests.get(author_url, timeout=10)
            except requests.exceptions.RequestException as e:
                print(f"Author page error: {e}")
                continue

            author_soup = BeautifulSoup(author_response.text, "lxml")

            fullname = author_soup.find("h3", class_="author-title").text.strip()
            born_date = author_soup.find("span", class_="author-born-date").text
            born_location = author_soup.find("span", class_="author-born-location").text
            description = author_soup.find(
                "div", class_="author-description"
            ).text.strip()

            authors_data.append(
                {
                    "fullname": fullname,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description,
                }
            )

            authors_cache.add(author)

    next_button = soup.find("li", class_="next")  # next page
    if next_button:
        next_page = next_button.find("a")["href"]
        url = BASE_URL + next_page
        page_number += 1
        print("Next Page")
    else:
        print("that is all")
        url = None

print("printing json")

with open("quotes.json", "w", encoding="utf-8") as f:  # write text
    json.dump(quotes_data, f, ensure_ascii=False, indent=2)

with open("authors.json", "w", encoding="utf-8") as f:  # write authors
    json.dump(authors_data, f, ensure_ascii=False, indent=2)

print("DONE!")
