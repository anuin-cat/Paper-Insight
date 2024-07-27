import requests
import xml.etree.ElementTree as ET
import sys
import io

# 设置默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_arxiv_papers(query, max_results=100):
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results
    }
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)
    papers = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        paper = {
            "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
            "authors": [author.find("{http://www.w3.org/2005/Atom}name").text for author in entry.findall("{http://www.w3.org/2005/Atom}author")],
            "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text,
            "published": entry.find("{http://www.w3.org/2005/Atom}published").text,
            "updated": entry.find("{http://www.w3.org/2005/Atom}updated").text,
            "id": entry.find("{http://www.w3.org/2005/Atom}id").text,
            "categories": [category.attrib['term'] for category in entry.findall("{http://arxiv.org/schemas/atom}category")],
            "comments": entry.find("{http://arxiv.org/schemas/atom}comment").text if entry.find("{http://arxiv.org/schemas/atom}comment") is not None else '',
            "doi": entry.find("{http://arxiv.org/schemas/atom}doi").text if entry.find("{http://arxiv.org/schemas/atom}doi") is not None else '',
            "pdf_url": entry.find("{http://www.w3.org/2005/Atom}link[@type='application/pdf']").attrib['href']
        }
        papers.append(paper)
    return papers

# 示例：获取关于CVPR的论文列表
cvpr_papers = get_arxiv_papers("all:CVPR")
for paper in cvpr_papers:
    print(f"Title: {paper['title']}")
    print(f"Authors: {paper['authors']}")
    print(f"Summary: {paper['summary']}")
    print(f"Published: {paper['published']}")
    print(f"Updated: {paper['updated']}")
    print(f"ID: {paper['id']}")
    print(f"Categories: {paper['categories']}")
    print(f"Comments: {paper['comments']}")
    print(f"DOI: {paper['doi']}")
    print(f"PDF URL: {paper['pdf_url']}")
    print()
