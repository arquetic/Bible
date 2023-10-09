import requests
from bs4 import BeautifulSoup
import json
import html

base_url = 'https://www.vatican.va/archive/ESL0506/'
index_url = base_url + '_INDEX.HTM'

def get_soup_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_verses(soup):
    verses = []
    verse_tags = soup.find_all('p', class_='MsoNormal')
    if verse_tags:
        for tag in verse_tags:
            verse_text = tag.get_text()
            sspp = verse_text.split()
            if len(sspp):
                verse_number = sspp[0]
                unscape = html.unescape(verse_text.strip())
                verses.append({
                    'verse_number': verse_number,
                    'verse': unscape.replace('\n', ' ')
                })
    return verses

def extract_and_struct(soup):
    # first second third
    print('START::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    bible = []
    first_ul = soup.find('ul')
    for li_1 in first_ul.find_all('li', recursive=False):
        font_tag = li_1.find('font', size='3')
        library = font_tag.get_text()
        print('Library: ', library)
        # Second loop: Run <li> from second <ul>
        second_ul = li_1.find('ul')
        for li_2 in second_ul.find_all('li', recursive=False):
            font_tag = li_2.find('font', size='3')
            link = font_tag.find('a', href=lambda href: href and href.startswith('__P'))
            if link:
                book_url = link['href']
                book_title = link.get_text()
            else:
                book_url = ''
                book_title = font_tag.get_text()
            if len(book_url):
                verses_url = base_url + book_url
                verses_soup = get_soup_from_url(verses_url)
                verses = get_verses(verses_soup)
                for v in verses:
                    verse_object = {
                        'library': library,
                        'book': book_title,
                        'chapter': 0,
                        'verse_number': v['verse_number'],
                        'verse': v['verse']
                    }
                    bible.append(verse_object)
            print('book_title: ', book_title)
            # Third loop: Run <li> from third <ul>
            third_ul = li_2.find('ul')
            if third_ul:
                for li_3 in third_ul.find_all('li'):
                    for a in li_3.find_all('a'):
                        chapter = a.get_text()
                        chapter_url = a['href']
                        verses_url = base_url + chapter_url
                        verses_soup = get_soup_from_url(verses_url)
                        verses = get_verses(verses_soup)
                        for v in verses:
                            verse_object = {
                                'library': library,
                                'book': book_title,
                                'chapter': chapter,
                                'verse_number': v['verse_number'],
                                'verse': v['verse']
                            }
                            bible.append(verse_object)
    return bible

index_soup = get_soup_from_url(index_url)
result = extract_and_struct(index_soup)

output_file = 'Vatican-Bible-toTrain.spa.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print(f"Los datos se han guardado exitosamente en el archivo '{output_file}'.")

