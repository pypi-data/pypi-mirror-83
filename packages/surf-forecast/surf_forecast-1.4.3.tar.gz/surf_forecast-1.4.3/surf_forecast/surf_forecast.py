import json 
from mechanize import Browser
from bs4 import BeautifulSoup

def getCity(city=""):
    
    if city != "":
        if city.lower() == "de haan" or city.lower() == "den haan":
            city = "Den Haan"

        # Selects city
        browser = Browser()
        browser.open('https://www.surf-forecast.com')

        def select_form(form):
            return form.attrs.get('action', None) == '/breaks/catch'

        browser.select_form(predicate=select_form)
        
        browser.form["query"] = city

        res = browser.submit()
        
        # Requests data from page
        content = res.read()
        soup = BeautifulSoup(content, 'html.parser')

        # Checks for errors
        errors = len(soup.select("#flash_errors"))
        
        if errors != 0:
            raise ValueError("City does not exist.")
        if errors == 0:
            if soup.find("span", {"class": "tempu"}).text == "C":
                temp_unit = "Celsius"
            elif soup.find("span", {"class": "tempu"}).text == "F":
                temp_unit = "Fahrenheit"

            if city != "Den Haan":
                city_name = soup.find("span", itemprop="name").text[:-1]
            else:
                city_name = "De Haan"
            
            temp = soup.select(".temp")[0].text
            temp_mean = soup.select(".temp")[1].text
            temp_min = soup.select(".temp")[3].text
            temp_max = soup.select(".temp")[2].text
            wind = soup.find("span", {"class": "wind"}).text
            wind_unit = soup.select(".windu")[0].text
            wind_dir = soup.find("div", class_="wind-dir").text
            wind_type = soup.find("div", class_="offshoreness").text

            # Returns json of data
            data = {
                'city': city_name,
                'main': {
                    'temp': float(temp),
                    'temp_mean': float(temp_mean),
                    'temp_min': float(temp_min),
                    'temp_max': float(temp_max),
                    'temp_unit': temp_unit
                },
                'wind': {
                    'wind': float(wind),
                    'wind_unit': wind_unit,
                    'wind_type': wind_type,
                    'wind_dir': wind_dir
                }
            }

            data = json.dumps(data, indent=4, ensure_ascii=False)

            return data

    else:
        raise ValueError("City is not defined.")