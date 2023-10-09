import requests
from bs4 import BeautifulSoup
import json
import html

base_url = 'https://www.vatican.va/archive/bible/nova_vulgata/documents/'
vetus_testamentum_url = base_url + 'nova-vulgata_vetus-testamentum_lt.html'
novum_testamentum_url = base_url + 'nova-vulgata_novum-testamentum_lt.html'
bible = []   

def get_soup_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_verses(soup):
    verses = []
    p_elements = soup.find_all('p')
    for p_element in p_elements:
        a_element = p_element.find('a', attrs={'name': True})
        if a_element:
            chapter = a_element['name']
            #print(chapter)
            br_tag = p_element.find('br')
            if br_tag:
                next_br = br_tag.nextSibling
                while next_br is not None:
                    if isinstance(next_br, str):
                        sspp = next_br.split()
                        if len(sspp):
                            verse_number = sspp[0]
                            unscape = html.unescape(next_br.strip())
                            verses.append({
                                'chapter': chapter,
                                'verse_number': verse_number,
                                'verse': unscape.replace('\n', ' ')
                            })
                    next_br = next_br.nextSibling
    return verses

def vt_extract_and_struct(soup):
    hrefs = soup.find_all(href=lambda href: href and href.startswith('nova-vulgata_vt_'))
    library = 'Vetus testamentum'
    print(library)
    for href in hrefs:
        link = href['href']
        book = href.get_text()
        print(book)
        verses_url = base_url + link
        verses_soup = get_soup_from_url(verses_url)
        verses = get_verses(verses_soup)
        for v in verses:
            verse_object = {
                'library': library,
                'book': book,
                'chapter': v['chapter'],
                'verse_number': v['verse_number'],
                'verse': v['verse']
            }
            bible.append(verse_object)
    return

def nt_extract_and_struct(soup):
    hrefs = soup.find_all(href=lambda href: href and href.startswith('nova-vulgata_nt_'))
    library = 'Novum testamentum'
    print(library)
    for href in hrefs:
        link = href['href']
        book = href.get_text()
        print(book)
        verses_url = base_url + link
        verses_soup = get_soup_from_url(verses_url)
        verses = get_verses(verses_soup)
        for v in verses:
            verse_object = {
                'library': library,
                'book': book,
                'chapter': v['chapter'],
                'verse_number': v['verse_number'],
                'verse': v['verse']
            }
            bible.append(verse_object)
    return

vetus_testamentum_soup = get_soup_from_url(vetus_testamentum_url)
vt_extract_and_struct(vetus_testamentum_soup)
novum_testamentum_soup = get_soup_from_url(novum_testamentum_url)
nt_extract_and_struct(novum_testamentum_soup)

output_file = 'Vulgata-toTrain.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(bible, f, indent=4, ensure_ascii=False)

print(f"Los datos se han guardado exitosamente en el archivo '{output_file}'.")
