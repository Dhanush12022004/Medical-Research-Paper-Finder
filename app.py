from flask import Flask, render_template, request, jsonify
import requests
import xml.etree.ElementTree as ET
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from rake_nltk import Rake

app = Flask(__name__)

# PubMed API URLs
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def classify_sentiment(polarity):
    """Classify sentiment based on polarity score."""
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

def calculate_sentiment(text):
    """Calculates the sentiment polarity and category of the text."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    category = classify_sentiment(polarity)
    rating = round((polarity + 1) * 2.5)  # Convert polarity to a 5-star rating
    return polarity, category, rating

def extract_keywords(text):
    """Extracts keywords from text using RAKE."""
    rake = Rake()
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()

def search_pubmed(query, count):
    """Searches PubMed for research papers based on the query and processes them."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": count,
        "retmode": "xml"
    }
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    
    root = ET.fromstring(response.content)
    ids = [id_elem.text for id_elem in root.findall(".//Id")]
    
    if not ids:
        return []
    
    summary_params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml"
    }
    summary_response = requests.get(PUBMED_SUMMARY_URL, params=summary_params)
    summary_root = ET.fromstring(summary_response.content)
    
    papers = []
    for docsum in summary_root.findall("DocSum"):
        paper_id = docsum.find("Id").text
        title = docsum.find("Item[@Name='Title']").text
        source = docsum.find("Item[@Name='Source']").text
        
        fetch_params = {
            "db": "pubmed",
            "id": paper_id,
            "retmode": "xml"
        }
        fetch_response = requests.get(PUBMED_FETCH_URL, params=fetch_params)
        fetch_root = ET.fromstring(fetch_response.content)
        abstract_element = fetch_root.find(".//Abstract/AbstractText")
        
        if abstract_element is None or not abstract_element.text:
            continue  # Skip papers without abstracts
        
        abstract = abstract_element.text
        polarity, sentiment_category, rating = calculate_sentiment(abstract)
        keywords = extract_keywords(abstract)
        link = f"https://pubmed.ncbi.nlm.nih.gov/{paper_id}/"
        
        papers.append({
            "title": title,
            "summary": abstract,
            "keywords": keywords,
            "link": link,
            "source": source,
            "rating": rating,
            "sentiment": {
                "polarity": polarity,
                "category": sentiment_category
            }
        })
    
    return papers

def group_papers_by_similarity(papers, n_clusters=5):
    """Groups papers based on similarity using KMeans clustering."""
    abstracts = [paper['summary'] for paper in papers]
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    X = tfidf_vectorizer.fit_transform(abstracts)
    
    kmeans = KMeans(n_clusters=n_clusters, n_init=10)
    kmeans.fit(X)
    
    labels = kmeans.labels_.astype(int)
    for paper, label in zip(papers, labels):
        paper['cluster'] = int(label)
    
    return papers

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    count = int(request.form['count'])
    papers = search_pubmed(query, count)
    
    if papers:
        papers = group_papers_by_similarity(papers)
        return jsonify(papers)
    else:
        return jsonify({"error": "No research papers found for your query."})

if __name__ == "__main__":
    app.run(debug=True)
