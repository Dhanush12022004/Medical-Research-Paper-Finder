Medical Research Paper Finder: Enhancing Search with Sentiment Analysis and Clustering
Overview
The Medical Research Paper Finder is a web application designed to streamline the search and exploration of medical research papers. It leverages PubMed's API for accessing vast repositories of medical literature and integrates advanced natural language processing techniques such as sentiment analysis, keyword extraction, and clustering to provide an enriched search experience.

Key Features
Voice and Text Search

Allows users to input queries via text or voice for added convenience.
Sentiment Analysis

Analyzes the sentiment of abstracts to classify them as Positive, Negative, or Neutral.
Provides a 5-star sentiment rating for easy interpretation.
Keyword Extraction

Highlights key terms and phrases from the abstracts using the RAKE algorithm.
Clustering

Groups similar research papers into clusters using K-Means clustering to enhance organization and navigation.
Interactive User Interface

Displays results with detailed summaries, sentiment scores, keywords, and direct links to PubMed.
Text-to-Speech Support

Users can listen to the abstract summaries for better accessibility.
Tech Stack
Backend: Flask (Python)
Frontend: HTML, CSS, JavaScript
APIs: PubMed API
Libraries/Tools:
TextBlob for sentiment analysis
RAKE for keyword extraction
Scikit-learn for clustering with K-Means
Speech Recognition and Speech Synthesis APIs for voice interaction
Installation
Prerequisites
Python 3.x installed
API access to PubMed
Steps
Clone the repository:
git clone https://github.com/your-username/medical-research-paper-finder.git  
cd medical-research-paper-finder  
Install the required dependencies:
pip install -r requirements.txt  
Run the Flask application:
python app.py  
Access the application in your browser at http://127.0.0.1:5000.

Usage
Enter a search query (e.g., "Cancer" or "Diabetes") or use the voice input button to speak your query.
Specify the number of papers to retrieve.
View the results, organized by clusters, along with sentiment ratings, keywords, and summaries.
Click the provided PubMed link for detailed information on a specific paper.
Contribution
Contributions are welcome! If you'd like to improve this project:

Fork the repository.
Create a new branch: git checkout -b feature-name.
Commit your changes: git commit -m 'Add feature'.
Push to the branch: git push origin feature-name.
Open a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
PubMed: For providing access to a vast repository of medical research papers.
TextBlob: For enabling sentiment analysis.
RAKE: For keyword extraction.
Scikit-learn: For clustering algorithms.
