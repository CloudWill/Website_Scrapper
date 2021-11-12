import multiprocessing
from bs4 import BeautifulSoup
import datetime
from pathlib import Path
import requests

session = None

def set_global_session():
    global session
    if not session:
        session = requests.Session()

def logs(txt):
    dt = datetime.datetime.now()
    date = f'{dt.year}-{dt.month}-{dt.day}'
    with open(f'{date}-logs.txt', 'a') as logs:
        print(f'{dt}-{txt}\n')
        logs.write(f'{dt}-{txt}\n')

def get_website(url):
    logs(f'currently loading {url}')
    # reads the website
    with session.get(url) as response:
        return response.content

def string_mutate(txt, after, before):
    return txt.translate({ord(c): after for c in before})

def save_website(title, data, metadata):
    #parses the title
    title = title[15:]
    title = string_mutate(title, '_', ' ')
    logs(f'saving: {title}')
    #creates the directory
    Path(f'stories/{title}').mkdir(parents=True, exist_ok=True)
    with open(f'stories/{title}/{title}.html', 'wb') as story:
        story.write(data)
    with open(f'stories/{title}/{title}-metadata.html', 'wb') as f:
        f.write(metadata)

def single_request(number):
    base_url = ''#get request here
    metadata_base_url = '' #get request here
    webContent = get_website(base_url)

    soup = BeautifulSoup(webContent, 'html.parser')
    # finds the title
    titles = soup.find_all('title')
    if len(titles) == 0:
        logs('dne')
        return 0
    else:
        # gets the metadata
        metadata = get_website(metadata_base_url)
        for title in titles:
            # removes unwanted characters from the title
            title = title.get_text()
            title = string_mutate(title, ' ', '!@#*$?:.\'\\\/\"')
            save_website(title, webContent, metadata)
            # only need the first occurrence of title
            break


def create_array(start, end):
    array = []
    for x in range(start, end):
        array.append(x)
    return array

def run_parser():
    array = create_array(0, 11000)

    # multi process
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        pool.map(single_request, array)


if __name__ == '__main__':
    logs('starting website parser')
    # creates the array
    run_parser()
    logs('done')


