from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv
import codecs
import argparse

s = HTMLSession()


def getdata(url: str) -> BeautifulSoup:
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup


def scrape_stars(soup: BeautifulSoup) -> dict:
    stars = soup.findAll("div", class_="col-12 d-block width-full py-4 border-bottom color-border-muted")
    links = list(map(lambda x: f"https://github.com{x}", [star.div.h3.a["href"] for star in stars]))
    descriptions = [des.p.text.strip() if des.p else "" for des in [star.find("div", class_="py-1") for star in stars]]
    return {link: description for link, description in zip(links, descriptions)}


def scrape_repos(soup: BeautifulSoup) -> dict:
    repos = soup.findAll("div", class_="d-inline-block mb-1")
    names = [repo.h3.a.text.strip() for repo in repos]
    descriptions = soup.findAll("p", class_="col-9 d-inline-block color-fg-muted mb-2 pr-4")
    descriptions = [des.text.strip() if des else "0" for des in descriptions]
    return {link: description for link, description in zip(names, descriptions)}


def write_csv(stars: list, user_name, option):
    with codecs.open(f"{user_name}_{option}.csv", "w", "utf-8") as f_obj:
        writer = csv.writer(f_obj)
        writer.writerow(["Link or Name", "Description"])  # header
        for data in stars:
            [writer.writerow([key, value]) for key, value in data.items()]

    print(f"{user_name}_{option}.csv: Done!!!!")


def get_next_page(soup: BeautifulSoup) -> str | None:
    page = soup.find('div', class_="BtnGroup")
    if page:
        if not page.button.text == "Next" and page.button["disabled"] == "disabled":
            url = page.a["href"] if page.a.text == "Next" else None
            return url
    return None


def get_next_page_repo(soup: BeautifulSoup) -> str | None:
    page = soup.find('a', class_="next_page")
    if page:
        url = "https://github.com" + page["href"]
        return url
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Starred Repos Scraping")
    parser.add_argument('-u', '--user_name', type=str, required=True, help='username')
    parser.add_argument('-o', '--option', type=str, required=True, help='repos or stars')
    args = parser.parse_args()

    username = args.user_name
    option = "repositories" if args.option == "repos" else "stars"
    url = f"https://github.com/{username}?tab={option}"

    result = []
    while True:
        soup = getdata(url)
        if args.option == "stars":
            result.append(scrape_stars(soup))
            url = get_next_page(soup)
        elif args.option == "repos":
            result.append(scrape_repos(soup))
            print(scrape_repos(soup))
            url = get_next_page_repo(soup)
        if not url:
            break

    write_csv(result, username, option)

##    while True:
##        soup = getdata(url)
##        print(scrape_repos(soup))
##        url = get_next_page_repo(soup)
##        if not url:
##            break
##        print(url)
