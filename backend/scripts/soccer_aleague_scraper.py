import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def get_total_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pagination = soup.find('ul', class_='pagination')
    if pagination:
        pages = pagination.find_all('li')
        if pages:
            return int(pages[-1].text)
    return 1  # Default to 1 if we can't find pagination

def scrape_page(url):
    print(f"Scraping {url}...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    matches = soup.find_all('div', class_='club-gamelist-match')
    
    print(f"Found {len(matches)} matches")
    
    data = []
    current_date = None
    
    for match in matches:
        date_header = match.find_previous('h4')
        if date_header:
            try:
                current_date = datetime.strptime(date_header.text, '%d %B %Y')
            except ValueError:
                print(f"Warning: Could not parse date '{date_header.text}'. Skipping.")
                continue
        
        if current_date:
            teams = match.find_all('div', class_='club-gamelist-match-clubs')
            score_div = match.find('div', class_='club-gamelist-match-score')
            if score_div:
                scores = score_div.text.strip().split(' - ')
                if len(scores) == 2:
                    try:
                        home_score, away_score = map(int, scores)
                        data.append({
                            'commence_datetime': current_date.strftime('%Y-%m-%d'),
                            'home_team': teams[0].text.strip(),
                            'home_team_score': home_score,
                            'away_team_score': away_score,
                            'away_team': teams[1].text.strip()
                        })
                    except ValueError:
                        print(f"Warning: Could not parse scores '{scores}'. Skipping.")
                else:
                    print(f"Warning: Unexpected score format '{score_div.text}'. Skipping.")
            else:
                print("Warning: Could not find score div. Skipping.")
    
    return data

def scrape_all_pages(base_url) -> list:

    all_data = []
    total_pages = get_total_pages(base_url + "/1")
    
    for page in range(1, total_pages + 1):
        url = f"{base_url}/{page}"
        print(f"Scraping page {page} of {total_pages}...")
        page_data = scrape_page(url)
        all_data.extend(page_data)
    
    return all_data

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['commence_datetime', 'home_team', 'home_team_score', 'away_team_score', 'away_team']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Main execution
base_url = 'https://footballdatabase.com/league-scores'

# Leagues to scrape
leagues = [
    'australia-a-league-2023-2024',
    'australia-a-league-2022-2023',
    'australia-a-league-2021-2022',
    'australia-a-league-2020-21',
    'australia-a-league-2019-20',
]

# Scrape all pages for each league
data = []
for league in leagues:
    print(f"Scraping {league}...")
    league_url = f"{base_url}/{league}"
    scraped_data = scrape_all_pages(league_url)
    data.extend(scraped_data)
    
save_to_csv(data, 'data/a_league_scores.csv')

print(f"Scraping complete. Data saved to a_league_scores.csv")