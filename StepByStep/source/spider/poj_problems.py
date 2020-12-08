import requests
from source.models import Problem, Source
from bs4 import BeautifulSoup


def poj_problems():
    resp = requests.get("http://poj.org/problemlist?volume=1")
    soup = BeautifulSoup(resp.content, 'html.parser')
    pages = len(soup.find('body').find('center').find_all('a'))
    result = []
    for i in range(pages):
        page = i + 1
        print(f'get page {page}')
        url = f'http://poj.org/problemlist?volume={page}'
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        table = soup.find_all('table')[-1]
        trs = table.find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            problem_id = tds[0].text
            title = tds[1].text
            link = f'http://poj.org/problem?id={problem_id}'
            result.append({
                'problem_id': problem_id,
                'title': title,
                'link': link
            })

    source, _ = Source.objects.get_or_create(name="poj")
    for item in result:
        problem_id = str(item["problem_id"])
        title = item["title"]
        link = item['link']
        Problem.objects.update_or_create(
            source=source,
            problem_id=problem_id,
            defaults={"title": title, "link": link},
        )
