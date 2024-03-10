import requests
from bs4 import BeautifulSoup
import csv
from os import path
import json

# Standard path definition
paths = {
    "data": path.join(path.dirname(__file__), "data"),
    "csv": path.join(path.dirname(__file__), "data", "article_texts.csv")
}

def get_archive_urls(base_url, from_date, to_date, limit=100):
    params = {
        'url': 'https://ft.com/content/*',
        'output': 'json',
        'from': from_date,
        'to': to_date,
        'filter': 'statuscode:200',
        'limit': limit
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  
        json_response = response.json()
        if not json_response:
            print("Empty JSON response")
            return []
        urls = [item[2] for item in json_response if isinstance(item, list) and len(item) > 2]
        print(f"Retrieved {len(urls)} URLs:", urls)  
        return urls
    except requests.RequestException as e:
        print(f"Failed to retrieve URLs: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return []
# In the above code I had to add some error handling/messaging since I had major issues with the URLs and the HTTP at the start, these made me help find the problems
# This raisal of a status error regarding the HTTP also appears in other parts of the code and as I will also explain, some minor adjustment needed to be made in the limits part at least

def get_article_data(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        y
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                if data.get('@type') == 'NewsArticle' and 'headline' in data:
                    return data['headline']
            except json.JSONDecodeError:
                continue
        
        # Minor html adjustment to make sure the url are found and scraped from the archive
        headline = soup.find('h1')
        if headline:
            return headline.get_text(strip=True)
        title_tag = soup.title
        if title_tag:
            return title_tag.get_text(strip=True)
    except requests.RequestException as e:
        print(f"Failed to retrieve article data from {url}: {e}")
    return None

# then follows the definition of the 'base url' (the archive) as the well as the dates.
def main():
    base_url = 'http://web.archive.org/cdx/search/cdx'
    from_date_2020 = '20200301000000'
    to_date_2020 = '20200307235959'
    from_date_2022 = '20220301000000'
    to_date_2022 = '20220307235959'

    urls_2020 = get_archive_urls(base_url, from_date_2020, to_date_2020, limit=118)
    urls_2022 = get_archive_urls(base_url, from_date_2022, to_date_2022, limit=215)
    # Lines 78 & 79 might look a bit interesting since they are using different limits (neither of which are 100). The reason for this is that the code I created also scraped all duplicate articles which made it quite useless in a way
    # So what you can see is actually the "magic numbers" for each of the months, that when used as the limit have enough articles show up that each of the months print out exactly 100 articles in the csv (have a look :) )

    articles_data = []
    seen_headlines = set()  # This is to make sure only 'unique' headlines are being tracked (see explanation on line 80 & 81)

    # 03/2020 scraping first
    for url in urls_2020:
        print("Processing URL:", url)  
        headline = get_article_data(url)
        if headline and headline not in seen_headlines:
            articles_data.append(('03/2020', headline))
            seen_headlines.add(headline)
        
    # Followed by 03/2022 scraping
    for url in urls_2022:
        print("Processing URL:", url)  
        headline = get_article_data(url)
        if headline and headline not in seen_headlines:
            articles_data.append(('03/2022', headline))
            seen_headlines.add(headline)

    # Saving to a csv to then complete the project in the 'Analys.py' file
    save_to_csv(articles_data, paths['csv'])

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['MM/YYYY', 'Headline'])
        writer.writerows(data)

if __name__ == "__main__":
    main()











