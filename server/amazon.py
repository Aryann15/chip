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
     
    return productName

print (get_data('https://www.amazon.in/dp/B08N5W4NNB'))