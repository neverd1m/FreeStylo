from bs4 import BeautifulSoup


def get_page_tags(page):
    """
    Функция, возвращающая структуру HTML-страницы в формате
    {'tag': n, ...}
    """
    data = page.content
    soup = BeautifulSoup(data, 'html5lib')
    tags = [tag.name for tag in soup.find_all(True)]
    unique_tags = set(tags)
    result_structure = {}
    for tag in unique_tags:
        result_structure[tag] = tags.count(tag)
    return result_structure
