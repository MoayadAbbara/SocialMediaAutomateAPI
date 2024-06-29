import requests
from bs4 import BeautifulSoup
from datetime import datetime
import consts

def LastFiveAnnouncements():
    duyurular_list = []
    # URL of the webpage to scrape
    

    response = requests.get(consts.AnnouncementsURL)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        cards = soup.find_all("div", class_="card")

        for card in cards[:5]:  # Loop through only the first 5 cards found
            title = card.find("h6", class_="card-title").a.get_text()
            link = consts.BSEU + card.find("h6", class_="card-title").a["href"]
            if card.find("img", class_="card-img-top"):
                image = consts.BSEU + card.find("img", class_="card-img-top")["src"]
            else:
                image = consts.DefaultImg
            date_str = card.find('small', class_='text-muted').get_text(strip=True)
            date = datetime.strptime(date_str.split()[0], "%d.%m.%Y")
            duyurular_list.append((title, link, image, date))  # Append to list as tuple
        return duyurular_list
    else:
        return {'error': 'Failed to retrieve webpage'}

def AnnouncementsDetails(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all div elements with class="col-2 p-1" within the specified div
        content = soup.find("div", class_="row d-flex justify-content-center")
        icerik_govde_div = soup.find('div', class_='col-md-12 px-1 text-justify icerik-govde')
        text_content = ''
        image_names = []
        if icerik_govde_div:
            paragraphs = icerik_govde_div.find_all(['p', 'li'])
            for element in paragraphs:
                text_content += element.get_text() + '\n'
        # Initialize an empty list to store image names
        
        if content :
            divs = content.find_all("div", class_="col-2 p-1")
            # Loop through each div and extract image names
            for div in divs:
                image_names.append(consts.BSEU + div.img["src"])

            # Return the list of image names
            return text_content,image_names
        else :
            return text_content , [consts.DefaultImg]