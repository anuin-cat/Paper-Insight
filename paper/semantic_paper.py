import requests
import sys
import io

# 设置默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json

# 获取当前目录根路径
import os
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(root_path)


def get_bulk_by_venue_year(venue='cvpr', year='2024', fields="year,venue,title,abstract,authors,citationCount,openAccessPdf,paperId"):
    url = f"http://api.semanticscholar.org/graph/v1/paper/search/bulk?venue={venue}&fields={fields}&year={year}"
    r = requests.get(url, proxies={"http": None, "https": None}).json()

    data_dir = os.path.join(root_path, "paper", "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    path = os.path.join(data_dir, f"{venue}_{year}.jsonl")

    print(f"Will retrieve an estimated {r['total']} documents")
    retrieved = 0

    with open(path, "a", encoding='utf-8') as file:
        while True:
            if "data" in r:
                retrieved += len(r["data"])
                print(f"Retrieved {retrieved} papers...")
                for paper in r["data"]:
                    print(json.dumps(paper), file=file)
            if "token" not in r:
                break
            r = requests.get(f"{url}&token={r['token']}").json()

    print(f"Done! Retrieved {retrieved} papers total")

# 2024年CVPR会议的所有论文
year = "2024"
# venue = "cvpr"
# venue = "nips"
venue = "aaai"
fields = "year,venue,title,abstract,authors,citationCount,openAccessPdf,paperId"
get_bulk_by_venue_year(venue=venue, year=year, fields=fields)