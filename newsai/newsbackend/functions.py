import json
import traceback
import openai
from apify_client import ApifyClient
from newsbackend.models import ScrapedArticle, GeneratedArticle  # Replace `your_app` with the actual name of your Django app.
from newsbackend.views import generate_article, generate_image
from PIL import Image



def generate_and_save_articles():
    generated_articles = []
    
    # Prepare the Actor input
    run_input = {
        "startUrls": [{"url": "https://www.ctvnews.ca/"}],
        "maxArticlesPerCrawl": 100,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("zuzka/ctv-news-scraper").call(run_input=run_input)

    # Fetch Actor results from the run's dataset
    news_articles = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    
    # Save to the database
    for _, news_article in enumerate(news_articles):
        try:
            scraped_article, created = ScrapedArticle.objects.get_or_create(
                title=news_article.get('title'),
                date=news_article.get('date'),
                defaults={
                    'url': news_article.get('url'),
                    'loaded_url': news_article.get('loadedUrl'),
                    'loaded_domain': news_article.get('loadedDomain'),
                    'referrer': news_article.get('referrer'),
                    'start_url': news_article.get('startUrl'),
                    'depth': news_article.get('depth'),
                    'soft_title': news_article.get('softTitle'),
                    'author': news_article.get('author'),
                    'publisher': news_article.get('publisher'),
                    'copyright': news_article.get('copyright'),
                    'favicon': news_article.get('favicon'),
                    'description': news_article.get('description'),
                    'lang': news_article.get('lang'),
                    'canonical_link': news_article.get('canonicalLink'),
                    'tags': news_article.get('tags'),
                    'image': news_article.get('image'),
                    'videos': news_article.get('videos'),
                    'links': news_article.get('links'),
                    'text': news_article.get('text'),
                    'screenshot_url': news_article.get('screenshotUrl'),
                }
            )

            if not created:
                scraped_article = None
                continue

        except Exception as e:
            scraped_article = None
            print(f"Exception occurred: {e}")
            print(traceback.format_exc())

        generated_image = None

        try:
            if scraped_article and scraped_article.id:
                print(scraped_article)
                generated_article_json = generate_article(news_article)
                generated_article = json.loads(generated_article_json)
                print(generated_article)
                generated_articles.append(generated_article)

                image_file = generate_image(generated_article['title'])

                if image_file:
                    GeneratedArticle.objects.create(
                        original_article=scraped_article,
                        generated_title=generated_article['title'],
                        generated_text=generated_article['article'],
                        generated_image=image_file  # Assigning the image file here
                    )

        except Exception as e:
            print(f"Exception occurred: {e}")
            print(traceback.format_exc())

    print(generated_articles)
    return generated_articles

