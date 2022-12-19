from bs4 import BeautifulSoup
import requests
import os


def server_connection(my_url):
    header = {
        "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" +
                      "108.0.0.0 Safari/537.36",
        "SEC-CH-UA-PLATFORM": "Windows",
        "HOST": "www.amazon.com",
        "ACCEPT-ENCODING": "gzip, deflate, br",
        "ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q" +
                  "=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    page = requests.get(my_url, headers=header)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
    else:
        print(("Some problem with connection to server, "
              "\n status code is:{}").format(page.status_code))
    return soup


def get_pics_from_page(soup):
    save_path = './pics/'
    images = soup.find_all('img')
    for image in images:
        link = image['src']
        try:
            names = image['alt']
        except Exception:
            continue
            raise
        type_link = "".join(reversed(link[-1:-5:-1]))
        if (type_link == '.jpg' or type_link == '.png') and (type_link != '.gif'):
            name = replace_non_corr_symbol(names) + '.jpg'
            complete_name = os.path.join(save_path, name)
            with open(complete_name, 'wb') as f:
                img = requests.get(link)
                f.write(img.content)


def replace_non_corr_symbol(name):
    return name.translate({ord(c): " " for c in "\"!@#$%^&*()[]{};:,./<>?\|`\~-=_+"})


def get_pics_from_all_pages():
    for i in range(1, 7):
        url = f"https://www.amazon.com/s?k=synthesizer&page=" \
              f"{i}&crid=34KGAREDOKW77&qid=1670899460&sprefix=synthesizer%2Caps%2C229&ref=sr_pg_1"
        get_pics_from_page(server_connection(url))


def main():
    get_pics_from_all_pages()


if __name__ == "__main__":
    main()
