import urllib.request
import xml.etree.ElementTree as ET
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv("my_key.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

# Initialize Chat Model
chat = ChatOpenAI(model="gpt-4", openai_api_key=OPENAI_API_KEY, temperature=0)

def fetch_arxiv_papers(query, max_results=5):
    """
    Fetch research papers from arXiv based on the query.
    :param query: The search query.
    :param max_results: Maximum number of results to fetch.
    :return: List of dictionaries containing paper details (title, summary, and URL).
    """
    base_url = "http://export.arxiv.org/api/query?"
    search_query = f"search_query=all:{urllib.parse.quote(query)}&start=0&max_results={max_results}"
    url = base_url + search_query

    try:
        # Fetch data from arXiv API
        response = urllib.request.urlopen(url)
        data = response.read().decode("utf-8")

        # Parse XML response
        root = ET.fromstring(data)
        papers = []
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            title = entry.find("{http://www.w3.org/2005/Atom}title").text
            summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
            link = entry.find("{http://www.w3.org/2005/Atom}id").text
            papers.append({"title": title.strip(), "summary": summary.strip(), "link": link.strip()})

        return papers
    except Exception as e:
        print(f"Error fetching data from ArXiv API: {e}")
        return []

def summarize_paper(title, summary):
    """
    Summarize a research paper using GPT-4.
    :param title: Title of the paper.
    :param summary: Abstract or summary of the paper.
    :return: Summarized text.
    """
    prompt = (
        f"Here is the title and abstract of a research paper:\n\n"
        f"Title: {title}\n\n"
        f"Abstract: {summary}\n\n"
        f"Please summarize this paper in 2-3 sentences, highlighting the key findings and contributions."
    )
    try:
        response = chat.predict(prompt)
        return response.strip()
    except Exception as e:
        return f"(Error summarizing paper: {str(e)})"

def query_documents(query, max_results=3):
    """
    Query ArXiv for research papers, summarize them, and return a GPT-4-based response with citations.
    :param query: User's query.
    :param max_results: Maximum number of papers to fetch.
    :return: Final response with citations.
    """
    # Fetch papers from ArXiv
    papers = fetch_arxiv_papers(query, max_results=max_results)

    if not papers:
        return (
            "I couldn't find any relevant research papers for your query. "
            "Please try rephrasing your question or providing more details."
        )

    # Summarize each paper
    for paper in papers:
        paper["summary"] = summarize_paper(paper["title"], paper["summary"])

    # Create a formatted response with citations
    summaries = []
    for i, paper in enumerate(papers):
        summaries.append(f"[{i + 1}] {paper['title']}: {paper['summary']} (Read more: {paper['link']})")

    # Join all paper summaries
    summaries_text = "\n\n".join(summaries)

    # Construct final prompt for GPT-4 to generate an answer
    final_prompt = (
        f"You are an academic assistant. Based on the following research paper summaries, "
        f"answer the query below and cite the summaries (e.g., [1], [2]):\n\n"
        f"Summaries:\n{summaries_text}\n\n"
        f"Query: \"{query}\"\n\n"
        f"Provide a detailed answer using the summaries provided above. Ensure proper citations."
    )

    try:
        final_response = chat.predict(final_prompt)
        return final_response.strip()
    except Exception as e:
        return f"An error occurred while generating the response: {str(e)}"
