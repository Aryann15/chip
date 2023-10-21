from requests_html import HTMLSession

product= "Macbook air m1"
url_product = ""

for letter in product:
    letter = str.lower(letter)
    if letter != " ":
        url_product = url_product + letter
    else:
        url_product = url_product + "+"

url = "https://www.amazon.in/s?k="+ url_product
print(url)

s = HTMLSession()
r=s.get(url)
r.html.render(sleep=1)

products= r.html.find('div[data-asin]')

