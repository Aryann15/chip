from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup


product= "Macbook air m1"
url_product = ""

for letter in product:
    letter = str.lower(letter)
    if letter != " ":
        url_product = url_product + letter
    else:
        url_product = url_product + "+"

url = "https://www.amazon.in/s?k="+ url_product
# print(url)
s = HTMLSession()

# r.html.render(sleep=1)

def get_asin(url):
    r=s.get(url)
    products= r.html.find('div[data-asin]')
    asins = []
    for product in products:
        if product.attrs['data-asin'] != '':
            asins.append(product.attrs['data-asin'])
    actual_url= "https://www.amazon.in/dp/"+asins[0]
    return actual_url

asin= get_asin(url)



def get_data(actual_url):
    r=s.get(actual_url)
    productName = r.html.find('#productTitle', first = True).full_text.strip()
    ratingsCount = r.html.find('#crCustomerReviewText',first = True).full_text.strip()
    return productName

def reviews(review_url):
    headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    res = requests.get(review_url, headers=headers)
    soup = BeautifulSoup(res.text,"html.parser")
    reviews = soup.find_all("div",{"data-hook":"review"})

    reviewList = []

    for item in reviews:
        review = {
        'title' : item.find('a',{'data-hook':'review-title'}).text.strip('\n')[19:],
        'rating' : float(item.find('i',{'data-hook':'review-star-rating'}).text.replace('out of 5 stars' , '').strip()),
        'body' : item.find('span',{'data-hook':'review-body'}).text.strip(),
        }
        reviewList.append(review)
    return reviewList

print(reviews('https://www.amazon.in/product-reviews/B08N5T6CZ6/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1'))