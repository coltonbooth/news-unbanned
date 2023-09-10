from django.db import models

class ScrapedArticle(models.Model):
    url = models.URLField()
    loaded_url = models.URLField(null=True, blank=True)
    loaded_domain = models.CharField(max_length=100, null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)
    start_url = models.URLField(null=True, blank=True)
    depth = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    soft_title = models.CharField(max_length=500, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    author = models.JSONField(null=True, blank=True)  # To accommodate list of authors
    publisher = models.CharField(max_length=100, null=True, blank=True)
    copyright = models.TextField(null=True, blank=True)
    favicon = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    lang = models.CharField(max_length=5, null=True, blank=True)
    canonical_link = models.URLField(null=True, blank=True)
    tags = models.JSONField(null=True, blank=True) # As it might be a list of tags
    image = models.URLField(null=True, blank=True)
    videos = models.JSONField(null=True, blank=True)  # Assuming it might be a list of video URLs
    links = models.JSONField(null=True, blank=True)  # Assuming it might be a list of links
    text = models.TextField(null=True, blank=True)
    screenshot_url = models.URLField(null=True, blank=True)
    scraped_at = models.DateTimeField(auto_now_add=True)

class GeneratedArticle(models.Model):
    original_article = models.ForeignKey(ScrapedArticle, on_delete=models.CASCADE)
    generated_title = models.CharField(max_length=300)
    generated_text = models.TextField()
    generated_image = models.TextField()  # Saving base64 encoded image as text
    generated_at = models.DateTimeField(auto_now_add=True)

