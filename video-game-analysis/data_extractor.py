import random
import warnings
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# ignore warnings
warnings.filterwarnings('ignore')

header_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
]

def get_game_links(base_url, num_pages):
    game_links = set()  # initialize a set to store unique game links
    exceptions = {}  # initialize a dictionary to store exceptions and status codes

    print("\nGetting game links.")

    # iterate over page numbers
    for page_no in tqdm(range(1, num_pages + 1)):
        page_url = f"{base_url}?page={page_no}"  # update page_url to include the page number

        # select a random user agent from the header list
        user_agent = random.choice(header_list)
        header = {"User-Agent": user_agent}

        # send a request to the page URL with the selected user agent
        webpage = requests.get(page_url, headers=header)

        # check if the webpage response is successful (status code 200)
        if webpage.status_code == 200:
            try:
                soup1 = BeautifulSoup(webpage.content, 'html.parser')
                soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

                # find the div element with class 'row show-release toggle-fade'
                g = soup2.find('div', {'class': 'row show-release toggle-fade'})

                if g:
                    # find all div elements with class 'col-2 my-2 px-1 px-md-2'
                    games = g.find_all('div', {'class': 'col-2 my-2 px-1 px-md-2'})

                    # extract the href attribute from the anchor tags and construct the complete game links
                    game_ref = [game.find('a').get('href') for game in games]
                    game_links.update(['https://www.backloggd.com' + ref for ref in game_ref])
                else:
                    print("Div element 'row show-release toggle-fade' not found.")

            except Exception as e:
                # record the game link and webpage status code in the exceptions dictionary
                exceptions[page_url] = webpage.status_code
        else:
            # record the game link and webpage status code in the exceptions dictionary
            exceptions[page_url] = webpage.status_code

    # print number of links retrieved
    print("\nNumber of links retrieved:", len(game_links))

    # print all exceptions and their status codes
    if exceptions:
        print("Exceptions:")
        for link, status_code in exceptions.items():
            print(f"\tGame Link: {link}, Status Code: {status_code}")

    return list(game_links)

def get_data(game_links):

    # create a data frame with specified column headers
    df = pd.DataFrame(columns=['Title', 'ParentGame', 'ReleaseDate', 'Team', 'Rating', 'xListed', 'xReviewed', 'Platforms', 'Genres', 'Summary', 'Reviews', 'Plays', 'Playing', 'Backlogs', 'Wishlist'])

    print('\n\nGetting data.')

    if game_links:
        for link in tqdm(game_links):
            user_agent = random.choice(header_list)
            header = {"User-Agent": user_agent}
            webpage = requests.get(link, headers=header)

            if webpage.status_code == 200:
                soup1 = BeautifulSoup(webpage.content, 'html.parser')
                soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

                # get game title
                try:
                    title = soup2.find('div', {'class': 'col-auto pr-1'}).get_text().strip()
                except:
                    title = np.nan

                # get parent game
                try:
                    parent_game = soup2.find('a', {'class': 'col px-3 mt-lg-2 my-3 my-md-1'})
                    parent_game = parent_game.get_text().strip()

                except:
                    parent_game = np.nan


                # get release date
                try:
                    release_date = ' '.join(soup2.find('div', {'class': 'col-auto mt-auto pr-0'}).get_text().strip().split()[-3:])
                except:
                    release_date = np.nan

                # get development team
                try:
                    teams = soup2.find('div', {'class': 'col-auto pl-lg-1 sub-title'})
                    teams = teams.find_all('a')
                    teams = [t.get_text().strip() for t in teams]
                except:
                    teams = np.nan

                # get average rating
                try:
                    rating = float(soup2.find(id='score').get_text().strip()[-3:])
                except:
                    rating = np.nan

                # get text strip data
                table = soup2.find_all('div', {'class': 'col-12 mb-1'})  # find all the div elements with the given class
                feats = [f.get_text().strip().split('\n')[0].strip() for f in table]  # extract the text for each element
                results = [r.get_text().strip().split('\n')[-1].strip() for r in table]  # extract the text for each element

                # get list count
                try:
                    nlists = soup2.find('p', {'class': 'game-page-sidecard'}).get_text().strip().split()[0]
                except:
                    nlists = np.nan

                # get review count
                try:
                    nreviews = soup2.find('p', {'class': 'game-page-sidecard'}).find_next().find_next().get_text().strip().split()[0]
                except:
                    nreviews = np.nan

                # get list of release platforms
                try:
                    platforms = soup2.find_all('a', {'class': 'game-page-platform'})
                    platforms = [platform.get_text().strip() for platform in platforms]
                except:
                    platforms = np.nan

                # get list of genres
                try:
                    genres = soup2.find_all('p', {'class': 'genre-tag'})
                    genres = [genre.get_text().strip() for genre in genres]
                except:
                    genres = np.nan

                # get summary
                try:
                    summary = soup2.find(id='collapseSummary').get_text().strip()
                except:
                    summary = np.nan

                # get reviews
                try:
                    review_section = soup2.find(id='game-reviews-section')
                    reviews = review_section.find_all('div', {'class': 'row pt-2 pb-1 review-card'})
                    reviews = [r.find('div', {'class': 'formatted-text'}).get_text().strip() for r in reviews]
                except:
                    reviews = np.nan

                # create a row with all the extracted data
                row = [title, parent_game, release_date, teams, rating, nlists, nreviews, platforms, genres, summary, reviews]
                row.extend(results)
                df.loc[len(df.index)] = row
    else:
        print("No game links found.")

    # print message upon completion
    print("Data retrieval complete.")

    # print the shape of the DataFrame
    print("\nThe DataFrame has {} rows and {} columns.".format(df.shape[0], df.shape[1]))

    # print message
    print("\nProcessing data")
    for column in ['xListed', 'xReviewed', 'Plays', 'Playing', 'Backlogs', 'Wishlist']:
        df[column] = df[column].apply(lambda x: float(x[:-1]) * 1000 if x.endswith('K') else x)
        df[column] = df[column].astype(int)

    # export DataFrame to flat file
    df.to_csv('dataset.csv', sep=',')

    # print message upon export
    print("\nData export complete.")

def main():
    base_link = input("Enter the base link: ")
    num_pages = int(input("Enter the number of pages: "))

    # get game links
    game_links = get_game_links(base_link, num_pages)

    # get game data
    get_data(game_links)

if __name__ == '__main__':
    main()