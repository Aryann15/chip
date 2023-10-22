from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup

product = "Macbook air m1"
url_product = ""

for letter in product:
    letter = str.lower(letter)
    if letter != " ":
        url_product = url_product + letter
    else:
        url_product = url_product + "+"

url = "https://www.amazon.in/s?k=" + url_product
# print(url)
s = HTMLSession()


def get_asin(url):
    r = s.get(url)
    products = r.html.find("div[data-asin]")
    asins = []
    for product in products:
        if product.attrs["data-asin"] != "":
            asins.append(product.attrs["data-asin"])
    actual_url = asins[1]
    return actual_url


asin = get_asin(url)

def reviews(asin): 
    critical_reviewList = []
    all_reviewList= []
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    for x in range (1,11):
        critical = f'https://www.amazon.in/product-reviews/{asin}/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&reviewerType=all_reviews&filterByStar=critical&pageNumber=1&sortBy=helpful&pageNumber={x}'
        all_review = f"https://www.amazon.in/product-reviews/{asin}/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&reviewerType=all_reviews&pageNumber=1filterByStar=all_stars&sortBy=recent&pageNumber={x}"
        
        res = requests.get(critical, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        reviews = soup.find_all("div", {"data-hook": "review"})

        for item in reviews:
            review = {
                "title": item.find("a", {"data-hook": "review-title"}).text.strip("\n")[
                    19:
                ],
                "rating": float(
                    item.find("i", {"data-hook": "review-star-rating"})
                    .text.replace("out of 5 stars", "")
                    .strip()
                ),
                "body": item.find("span", {"data-hook": "review-body"}).text.replace("The media could not be loaded.\n                \n\n\n\n\xa0","").strip(),
            }
            critical_reviewList.append(review)


        res2 = requests.get(all_review, headers=headers)
        soup = BeautifulSoup(res2.text, "html.parser")
        reviews = soup.find_all("div", {"data-hook": "review"})

        for item in reviews:
            review = {
                "title": item.find("a", {"data-hook": "review-title"}).text.strip("\n")[
                    19:
                ],
                "rating": float(
                    item.find("i", {"data-hook": "review-star-rating"})
                    .text.replace("out of 5 stars", "")
                    .strip()
                ),
                "body": item.find("span", {"data-hook": "review-body"}).text.strip(),
            }
            all_reviewList.append(review)   
    combined_reviews = {
        "all reviews": all_reviewList,
        "crictical reviews": critical_reviewList
    }
    return combined_reviews

# print(asin)
print(reviews(asin))
