from bs4 import BeautifulSoup
import requests
import csv
import codecs
import argparse


def scrape_stars(url: str) -> list:
    html_text = requests.get(url).text
    soup: BeautifulSoup = BeautifulSoup(html_text, 'lxml')
    stars = soup.findAll("div", class_="col-12 d-block width-full py-4 border-bottom color-border-muted")
    names = list(map(lambda x: f"https://github.com{x}", [star.div.h3.a["href"] for star in stars]))
    descriptions = [des.p.text.strip() if des.p else "" for des in [star.find("div", class_="py-1") for star in stars]]
    return {key: value for key, value in zip(names, descriptions)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Starred Repos Scraping")
    parser.add_argument('-u', '--user_name', type=str, required=True , help='username')
    args = parser.parse_args()
    
    website = f"https://github.com/{args.user_name}?tab=stars"
    data = scrape_stars(website)

    with codecs.open(f"github_stars_{args.user_name}.csv", "w", "utf-8") as f_obj:
        writer = csv.writer(f_obj)
        writer.writerow(["link", "description"])    # header
        [writer.writerow([key, value]) for key, value in data.items()]

    print("Done!!!!")
