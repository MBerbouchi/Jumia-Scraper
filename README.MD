 

# 📊 Jumia iPhone Price Scraper + USD Conversion + CSV Export + Bar Chart

## 🧾 **Project Description**

This Python script scrapes iPhone product prices from **Jumia Morocco**, fetches the **USD → MAD exchange rate** from an external API, converts prices to both currencies, and generates a **CSV report**.
Additionally, it creates a **bar chart visualization** of the collected prices.

This tool is useful for **market research, price monitoring, competitor analysis, and e-commerce automation**.

---

## ✨ **Features**

* 🛒 Scrapes iPhone product cards from Jumia
* 🌍 Fetches live USD → MAD rate using ExchangeRate API
* 🔁 Retry system for both webpage scraping & API calls
* 💰 Converts all prices from MAD to USD
* 📦 Saves all data to `jumia_product.csv`
* 📉 Adds an automatic **average price summary row**
* 📊 Generates a **bar chart** of product prices (MAD)
* 🖼️ Extracts product image URLs

---

## 📦 **Requirements**

Install all dependencies using:

```bash
pip install requests beautifulsoup4 pandas matplotlib
```

---

## ▶️ **How to Run the Script**

1. Create a file named:

```
main.py
```

2. Paste the project code into the file.

3. Run it with:

```bash
python main.py
```

4. After running, the script will generate:

### ✅ **1. CSV File**

```
jumia_product.csv
```

Containing:

* Product title
* Price in MAD
* Price in USD
* Image URL
* A final row showing average prices

---

### ✅ **2. Bar Chart**

A pop-up window will show a bar chart of the iPhone prices in MAD.

Example title:

```
iPhone Prices in MAD (Jumia)
```

---

## 📁 **CSV Output Example**

| title         | price_MAD | price_USD | image     |
| ------------- | --------- | --------- | --------- |
| iPhone 11     | 4500      | 450       | https://… |
| iPhone 13     | 6200      | 620       | https://… |
| ...           | ...       | ...       | ...       |
| AVERAGE PRICE | 5120      | 512       | —         |

---

## 🧠 **Notes & Recommendations**

* If the API fails, the script automatically uses the fallback rate: **1 USD = 10 MAD**
* Jumia may change HTML structure; update the selectors (`class="prd _fb col c-prd"`) if scraping stops working
* You can replace the URL to scrape other categories
* Chart display requires a GUI environment (won’t show in some servers)

 