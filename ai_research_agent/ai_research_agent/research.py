from duckduckgo_search import DDGS
import wikipedia
import time

def search_company(company_name: str, max_results: int = 8) -> str:
    """Search DuckDuckGo for company information."""
    results_text = ""
    queries = [
        f"{company_name} company overview business",
        f"{company_name} recent news 2024 2025",
        f"{company_name} expansion plans projects",
        f"{company_name} challenges problems issues",
    ]

    try:
        with DDGS() as ddgs:
            for i, query in enumerate(queries):
                try:
                    results = list(ddgs.text(query, max_results=3))
                    if results:
                        results_text += f"\n--- Search: {query} ---\n"
                        for r in results:
                            title = r.get("title", "")
                            body  = r.get("body", "")
                            href  = r.get("href", "")
                            results_text += f"• {title}\n  {body}\n  Source: {href}\n\n"
                    time.sleep(0.3)
                except Exception:
                    continue
    except Exception as e:
        results_text += f"\nDuckDuckGo search error: {e}\n"

    return results_text.strip() if results_text else f"Limited search results for {company_name}."


def get_wikipedia_summary(company_name: str) -> str:
    """Fetch Wikipedia summary for the company."""
    try:
        wikipedia.set_lang("en")
        search_results = wikipedia.search(company_name, results=3)

        for title in search_results:
            try:
                page = wikipedia.page(title, auto_suggest=False)
                summary = wikipedia.summary(title, sentences=10, auto_suggest=False)
                return f"Title: {page.title}\nURL: {page.url}\n\nSummary:\n{summary}"
            except wikipedia.exceptions.DisambiguationError as e:
                try:
                    page = wikipedia.page(e.options[0], auto_suggest=False)
                    summary = wikipedia.summary(e.options[0], sentences=10, auto_suggest=False)
                    return f"Title: {page.title}\nURL: {page.url}\n\nSummary:\n{summary}"
                except Exception:
                    continue
            except Exception:
                continue

        return f"No Wikipedia article found for {company_name}."

    except Exception as e:
        return f"Wikipedia lookup error: {e}"
