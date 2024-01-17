import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def scrape_property_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Your scraping logic to extract property details
    property_data = []

    # Example: Extract property names and bedrooms
    property_names = soup.find_all("p", class_="styles-module_content__location__bNgNM")
    property_prices = soup.find_all("p", class_="styles-module_content__price__SgQ5p")
    property_bedrooms = get_text_after_tag("use", href="/static/icons/pf-icons-sprite.svg#area_size")

    for name, bedrooms, prices in zip(
        property_names, property_bedrooms, property_prices
    ):
        property_data.append(
            {
                "Name": name.text.strip(),
                "Bedrooms": get_text_after_tag(bedrooms),
                "Prices": prices.text.strip(),
            }
        )

    return property_data


def get_text_after_tag(html_content):
    pattern = r'<use href="/static/icons/pf-icons-sprite\.svg#area_size">(.+?)</use>'
    match = re.search(pattern, str(html_content))
    if match:
        return match.group(1).split("</use>")[-1]
    else:
        return None


def create_spreadsheet(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)
    print(f"Spreadsheet created: {output_file}")


def main():
    # Specify the URL of the property listings page
    property_url = "https://example.com/property-listings"

    # Scrape property data
    property_data = scrape_property_data(property_url)

    # Create a spreadsheet
    create_spreadsheet(property_data, "property_listings.xlsx")


if __name__ == "__main__":
    main()
