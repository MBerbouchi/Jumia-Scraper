import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import sys
import matplotlib.pyplot as plt

url = "https://www.jumia.ma/iphone/"
headers = {
    "access-control-allow-origin": "*",
    "content-type": "text/html; charset=utf-8",
    "accept-language": "en-US,en;q=0.9,ar;q=0.8",
}


# --------------------


def convert_price(text):
    # Remove currency and spaces
    t = re.sub(r"[A-Za-z\s]+", "", text)
    # Replace comma with dot
    t = t.replace(",", "")
    # Remove .00 or unnecessary trailing zeros
    t = re.sub(r"\.00$", "", t)
    return float(t)


def get_conversion_rates(url, retries=3, timeout=5):
    """Handles API failures with retries + fallback."""
    for attempt in range(retries):
        try:
            response = requests.get(url).json()
            if response.get("result") == "success":
                return response
            print(f"[{attempt+1}/{retries}] - {response.get("error-type")}")
        except Exception as e:
            print(f"API failed… retrying [{attempt+1}/{retries}] - error type   {e}")
        time.sleep(1)

    print("🚫 can't fitched the conversation rate after retries")
    return None


def get_page(url, retries=3, timeout=5):
    for attemp in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                return response
            # If server responded but not 200
            print(
                f"[{attemp+1}]/{retries} - server error - status : {response.status_code}"
            )

        except requests.exceptions.RequestException as e:
            # Connection errors, timeout, DNS failure, etc.
            print(f"[{attemp+1}]/{retries} - Request failed: {e}")

        time.sleep(1)
    print("❌ failed to fetch the page after retries")
    return None


# --------------------


page = get_page(url)
if page:
    soup = BeautifulSoup(page.content, "html.parser")
else:
    print("❌can't continue without the page")
    sys.exit()
EXCHANGE_API = "https://v6.exchangerate-api.com/v6/00d3f190a7d788a409b6e14c/latest/USD"
USD_TO_MAD = 10

print("\nfetching USD -> MAD conversation rate...")
conversion_rates = get_conversion_rates(EXCHANGE_API)
if conversion_rates:
    conversion_rates = conversion_rates["conversion_rates"]["MAD"]
    print(f"\n✅ API success  1 USD -> {conversion_rates} MAD")
else:
    conversion_rates = USD_TO_MAD
    print(f"\n✅ API failed usifn fallback   1 USD -> {conversion_rates} MAD")


products = soup.find_all("article", attrs={"class": "prd _fb col c-prd"})

df = pd.DataFrame([])

for product_card in products:
    product_title = product_card.find("h3", class_="name")
    product_img = product_card.find("img", class_="img")
    price = product_card.find("div", class_="prc").text
    price = convert_price(price)

    price_in_usd = price / USD_TO_MAD
    new_product = {
        "title": product_title.text,
        "price_MAD": price,
        "price_USD": round(price_in_usd, 2),
        "image": product_img.get("data-src"),
    }
    df = pd.concat([df, pd.DataFrame([new_product])], ignore_index=True)

# Calcul the average price  in MAD and USD
avg_mad = df["price_MAD"].mean()
avg_usd = df["price_USD"].mean()


# add average to csv via new row
summary_row = {
    "title": "AVERAGE PRICE",
    "price_MAD": round(avg_mad, 2),
    "price_USD": round(avg_usd, 2),
    "image": "",
}
df = pd.concat([df, pd.DataFrame([summary_row])], ignore_index=True)


# ============================
#         SAVE CSV FILE
# ============================

df.to_csv("jumia_product.csv", index=False)
print("\n📁 CSV file saved: jumia_product.csv")


# ============================
#         DRAW BAR CHART
# ============================

print("📊 Generating bar chart...")

plt.figure(figsize=(12, 6))
plt.bar(df["title"][:-1], df["price_MAD"][:-1])
plt.xticks(rotation=90)
plt.title("iPhone Prices in MAD (Jumia)")
plt.xlabel("Product Name")
plt.ylabel("Price (MAD)")
plt.tight_layout()
plt.show()


# ============================
#         FINAL MESSAGE
# ============================

print("\n-----------------------------------")
print("Products report saved successfuly to jumia_product.csv")
print(f"Products founds : {len(products)}")
print(f"Average price in Dirhams : {avg_mad:.2f} MAD")
print(f"Average price in Dollar : {avg_usd:.2f} USD")
print("-----------------------------------")
