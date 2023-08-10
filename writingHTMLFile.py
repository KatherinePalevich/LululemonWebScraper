from bs4 import BeautifulSoup
import requests
import webbrowser

url = input("Enter your URL:")
size = input("Enter your desired size:")
#md = input("Do you want to view the marked down version?:")
if "sz" not in url:
    url = url + "?&sz=" + size
    print(url)
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Creating an HTML file
with open("LLLWebScraper.html","w") as out:

    # Adding input data to the HTML file
    out.write("<html>\n<head>\n<title> \nOutput Data in an HTML file \
                    </title>\n</head> <body><h1>Welcome to <font color =#c91a1a>Lululemon Web Scraper</font></h1>\
                    \n<h2>By Katherine Palevich</h2> \n")

    #Finds/adds the item name
    list = []
    names = soup.find_all('div', attrs={'class': 'OneLinkNoTx'})
    for name in names:
        text = name.text.strip()
        list.append(text)
    out.write('<p>Item Name: <a href="' + url + '">' + " ".join(list[1:2]) + '</a> </p>')


    #Finds/adds the price
    price = soup.find_all('span', attrs={'class': 'price-1jnQj price'})
    for tag in price:
        out.write("<p>Item Price: " + tag.text.strip() + "</p>")

    #Display the size specified
    out.write("<p>Item Size: " + size + "</p>")
    
    #Finds/adds the colors available
    tags = []
    available = []
    not_available = []
    available_pic = []
    not_available_pic = []
    collection = soup.findAll("img")
    for img in collection:
        if 'alt' in img.attrs:
            if "not available" in img.attrs['alt']:
                not_available.append(img.attrs['alt'])
                imgs = img['srcset'].split(",")
                #print(imgs[0:1])
                not_available_pic.append(imgs[0:1])
            else:
                available.append(img.attrs['alt'])
                imgs = img['srcset'].split(",")
                available_pic.append(imgs[0:1])

    out.write("<p>Item Colors Available: " + " , ".join(available[1:]) + "</p>")
    for color in available_pic[1:]:
        out.write('<img src="' + "".join(color) + '" >')

    out.write("<p>Item Colors Not Available: " + " , ".join(not_available[0:]) + "</p>")
    for color in not_available_pic:
        out.write('<img src="' + "".join(color) + '" >')

    # Saving the data into the HTML file
    out.write("</body></html>")

chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

webbrowser.get(chrome_path).open("LLLWebScraper.html")
