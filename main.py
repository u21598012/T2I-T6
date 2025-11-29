from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import requests
import datetime
import os

app = FastAPI(title="Health News API")

# Your NewsAPI key
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "1fc94ffb09bf4e76ba73ab6e0c7827b1")

@app.get("/v1/news")
def get_news(topic: str = Query(..., description="The topic you want news for, e.g. diabetes")):
    """
    Fetch recent news articles for a given topic from NewsAPI.
    Returns title, description, url, and image URL.
    """
    if not NEWS_API_KEY:
        raise HTTPException(status_code=500, detail="Missing NEWS_API_KEY")

    # Dates
    current_date = datetime.date.today()
    date_string = current_date.strftime("%Y-%m-%d")

    # Build NewsAPI URL
    main_url = (
        f"https://newsapi.org/v2/everything?"
        f"q={topic}&"
        f"from=2023-01-01&"
        f"to={date_string}&"
        f"sortBy=publishedAt&"
        f"apiKey={NEWS_API_KEY}"
    )

    try:
        news = requests.get(main_url, timeout=10).json()
        articles = news.get("articles", [])
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching news: {e}")

    # Collect article details
    results = []
    for a in articles:
        results.append({
            "title": a.get("title"),
            "description": a.get("description"),
            "url": a.get("url"),
            "image": a.get("urlToImage")
        })

    return JSONResponse(content={"topic": topic, "articles": results})
