from bs4 import BeautifulSoup
import requests
import csv

headers = { "accept-language": "en-GB,en;q=0.9",  
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"}

csv_field_names = ["Title", "Rating", "Price", "Seller", "SellerURL", "BulletPoints", "ImageURL", "FullDescription"]
csv_rows = []

urls_to_scrape = [
    "https://www.amazon.co.uk/GeekShare-Controller-Anti-Slip-Protector-Compatible/dp/B0C4L3FFCD",
    "https://www.amazon.co.uk/Trintion-Scratching-Scratcher-Activity-Dangling/dp/B08FT54NRM",
    "https://www.amazon.co.uk/dp/B08ZD7QGY7"
]

def remove_non_ascii(text):
    return text.encode("ascii", "ignore").decode("ascii")

# Scrape data from all urls
for url in urls_to_scrape:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    amazon_domain = url.split("www.amazon")[1].split("/")[0]

    title = remove_non_ascii(soup.select_one("#productTitle").text.strip())
    rating = remove_non_ascii(soup.select_one("#acrPopover").attrs.get("title").replace("out of 5 stars",""))
    price = remove_non_ascii(soup.select_one("span.a-offscreen").text)
    image_url = remove_non_ascii(soup.select_one("#landingImage").attrs.get("src"))
    bullets = remove_non_ascii(soup.select_one("#feature-bullets").text.replace("About this item", "").strip().replace("    ", "\n"))
    full_desc = remove_non_ascii(soup.select_one("#aplus").text.replace("Previous page", "").replace("Next page", "").replace("Product Description", "").strip().replace("\t", ""))
    seller = remove_non_ascii(soup.select_one("#bylineInfo").text.replace("Visit the ", "").replace(" Store", "").replace("Brand: ", ""))
    seller_url = remove_non_ascii("www.amazon" + amazon_domain + soup.select_one("#bylineInfo").attrs.get("href"))

    csv_rows.append([title, rating, price, seller, seller_url, bullets, image_url, full_desc])
    print("Finished scraping data from", url)


# Write to csv file
output_file = "Products"
with open(output_file + ".csv", "w+", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(csv_field_names)

    for row in csv_rows:
        writer.writerow(row)

print("CSV file created.")