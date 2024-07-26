import requests

def get_papers_from_conference(conference_name, year, limit=100):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": f"{conference_name} {year}",
        "fields": "title,authors,abstract,year,venue,doi,citations,references,fieldsOfStudy,url,journal,externalIds,topics,influentialCitationCount,corpusId",
        "limit": limit
    }
    response = requests.get(url, params=params)
    return response.json()

def get_all_papers(conference_name, year):
    papers = []
    offset = 0
    limit = 100
    while True:
        response = get_papers_from_conference(conference_name, year, limit)
        if not response or 'data' not in response:
            break
        papers.extend(response['data'])
        if len(response['data']) < limit: break
        if len(papers) >= 1000: break
        offset += limit
    return papers

# 示例：获取CVPR 2024年所有论文的详细信息
conference_name = "CVPR"
year = 2024
cvpr_papers = get_all_papers(conference_name, year)

for paper in cvpr_papers:
    print(f"Title: {paper['title']}")
    print(f"Authors: {[author['name'] for author in paper['authors']]}")
    print(f"Abstract: {paper.get('abstract', 'N/A')}")
    print(f"Year: {paper['year']}")
    print(f"Venue: {paper['venue']}")
    print(f"DOI: {paper.get('doi', 'N/A')}")
    print(f"Citations: {paper.get('numCitedBy', 'N/A')}")
    print(f"References: {[reference.get('title', 'N/A') for reference in paper.get('references', [])]}")
    print(f"Fields of Study: {paper.get('fieldsOfStudy', 'N/A')}")
    print(f"PDF URL: {paper.get('url', 'N/A')}")
    print(f"Journal: {paper.get('journal', {}).get('name', 'N/A')}")
    print(f"Volume: {paper.get('journal', {}).get('volume', 'N/A')}")
    print(f"Issue: {paper.get('journal', {}).get('issue', 'N/A')}")
    print(f"Pages: {paper.get('journal', {}).get('pages', 'N/A')}")
    print(f"Publisher: {paper.get('journal', {}).get('publisher', 'N/A')}")
    print(f"External IDs: {paper.get('externalIds', 'N/A')}")
    print(f"Topics: {[topic['topic'] for topic in paper.get('topics', [])]}")
    print(f"Influential Citations: {paper.get('influentialCitationCount', 'N/A')}")
    print(f"Corpus ID: {paper.get('corpusId', 'N/A')}")
    print("\n")