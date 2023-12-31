# Generated by Django 4.2.5 on 2023-09-07 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapedArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('loaded_url', models.URLField()),
                ('loaded_domain', models.CharField(max_length=100)),
                ('referrer', models.URLField()),
                ('start_url', models.URLField()),
                ('depth', models.IntegerField()),
                ('title', models.CharField(max_length=500)),
                ('soft_title', models.CharField(max_length=500)),
                ('date', models.DateTimeField()),
                ('author', models.JSONField()),
                ('publisher', models.CharField(max_length=100)),
                ('copyright', models.TextField()),
                ('favicon', models.URLField(blank=True, null=True)),
                ('description', models.TextField()),
                ('lang', models.CharField(max_length=5)),
                ('canonical_link', models.URLField()),
                ('tags', models.JSONField()),
                ('image', models.URLField(blank=True, null=True)),
                ('videos', models.JSONField()),
                ('links', models.JSONField()),
                ('text', models.TextField()),
                ('screenshot_url', models.URLField(blank=True, null=True)),
                ('scraped_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GeneratedArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generated_title', models.CharField(max_length=300)),
                ('generated_text', models.TextField()),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('original_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsbackend.scrapedarticle')),
            ],
        ),
    ]
