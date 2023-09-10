from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.generic.detail import DetailView
from .models import ScrapedArticle, GeneratedArticle
from apify_client import ApifyClient
import openai
import json
import traceback

openai.api_key = ''
client = ApifyClient("")


def generate_article(scraped_article: list) -> list:
    messages = [
        {"role": "system", "content": "You are a helpful assistant. I want you to read the following article title and content, understand the main details and events reported, and then compose a catchy title (no more than 10 words) and a unique article based on your understanding of the news. Please make the article longer than one paragraph. Return your response in JSON format."},
        {"role": "user", "content": f"Original Title: {scraped_article['title']}\n\nText: {scraped_article['text']}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k", 
        messages=messages,
        max_tokens=5000
    )

    return response.choices[0].message['content'].strip()

def generate_image(article_title):
    try:
        response = openai.Image.create(
            prompt=article_title,
            n=1,
            size="256x256",
            response_format="b64_json"
        )
        image_b64_json = response['data'][0]['b64_json']
        return image_b64_json
    except Exception as e:
        print(f"Error generating image: {e}")
        return None


class GenerateAndSaveArticleView(View):

    def get(self, request):
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

                    generated_image = generate_image(generated_article['title'])

                if generated_image:
                    GeneratedArticle.objects.create(
                        original_article=scraped_article,
                        generated_title=generated_article['title'],
                        generated_text=generated_article['article'],
                        generated_image=generated_image
                    )
            except Exception as e:
                print(f"Exception occurred: {e}")
                print(traceback.format_exc())


        return JsonResponse(generated_articles, safe=False)



class DisplayArticlesView(View):
    template_name = 'display_articles.html'

    def get(self, request):
        articles = GeneratedArticle.objects.all()
        return render(request, self.template_name, {'articles': articles})

class ArticleDetailView(DetailView):
    model = GeneratedArticle
    template_name = 'article_detail.html'  # This is the new template you will create.
    context_object_name = 'article'