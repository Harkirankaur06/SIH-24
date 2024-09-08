import scrapy
from pymongo import MongoClient
import requests
import json
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# MongoDB connection
client = MongoClient('mongodb+srv://disasterData:sihdata2024@techtitans.jnat6.mongodb.net/')
db = client['disasterData']
collection = db['TechTitans']

# Visual Crossing Weather API
weather_api_key = '8D7MK5WEBZNC6BW2FCHVMFN7Z'
weather_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'

# Facebook API Token
facebook_token = 'EAAS4lSZAw7PUBO084REr3KgVj06WVzL09yZBLEY2jhaxM0NVSTUTmuiLUkDl0n97pv1xHzwNZBVkwpZADYr1FsAfHNarZBQriL9Ob8Qq0riTRZBRYDYjrou4amsTQOO3VKTpbxgs1BF5u0isGllKZArOvbYVHcnK2hALmK4XfHnZCJTsRPptATj80AtRZBmUaXir94HJX8sDazhtE468xO4aznqeeSiZAb39gO8Kdk4GKLSWEld7eS8FZCoBFs6ZCGoxRBgefI3gx7AZD'
facebook_url = 'https://graph.facebook.com/v11.0/me/feed'

# Instagram API Token and URL
instagram_token = 'EAAS4lSZAw7PUBO7etXirCUzVqILefGbWHpAoKux5wr6YiIbDtPSMseuWyFlDqMQNGFD68kHItobIoyjXTzziJBbNBgjgltUQQ0gKI0U5Khfqv94jZC0aaHH5rDMdLGbbm2rmq2bmbN1eOjeZA78AqGIykZA4N8OZARBIbXV2ZBR1mrW5MQ0FBwD8CGKFYd5ZC1OfYZAAv5zHU3Olx0fV9z3B50Y4oQZDZD'
instagram_url = 'https://graph.instagram.com/me/media'

# Load SpaCy Model and Sentiment Analyzer
nlp = spacy.load('en_core_web_sm')
analyzer = SentimentIntensityAnalyzer()

# Scrapy Spider Class
class DisasterSpider(scrapy.Spider):
    name = "disaster_spider"
    
    start_urls = [
        'https://www.ndtv.com/latest',
        'https://timesofindia.indiatimes.com/',
        'https://www.hindustantimes.com/latest-news',
        'https://mausam.imd.gov.in/',
        'https://reliefweb.int/disaster/fl-2024-000109-ind',
        'https://reliefweb.int/disaster/tc-2024-000083-bgd'
    ]
    
    # List of natural disaster keywords
    keywords = ['earthquake', 'flood', 'cyclone', 'landslide', 'tsunami', 'drought']
    
    def parse(self, response):
        for article in response.xpath('//a/@href').extract():
            if any(keyword in article.lower() for keyword in self.keywords):
                yield scrapy.Request(response.urljoin(article), callback=self.parse_article)
    
    def parse_article(self, response):
        title = response.xpath('//title/text()').get()
        body = response.xpath('//p/text()').getall()
        body_text = ' '.join(body)

        # Text Preprocessing and NLP tasks
        preprocessed_text = self.preprocess_text(body_text)
        sentiment = self.analyze_sentiment(preprocessed_text)
        entities = self.extract_entities(preprocessed_text)

        # Store data in MongoDB
        article_data = {
            'url': response.url,
            'title': title,
            'body': body_text,
            'preprocessed_text': preprocessed_text,
            'sentiment': sentiment,
            'entities': entities
        }
        collection.insert_one(article_data)
        yield article_data

        # Fetch data from other APIs
        self.fetch_weather_data()
        self.fetch_facebook_data()

    def preprocess_text(self, text):
        """
        Function to preprocess text (tokenization, lemmatization, removing stopwords).
        """
        doc = nlp(text)
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return ' '.join(tokens)

    def analyze_sentiment(self, text):
        """
        Function to perform sentiment analysis using VADER.
        """
        sentiment_scores = analyzer.polarity_scores(text)
        return sentiment_scores

    def extract_entities(self, text):
        """
        Function to extract named entities from the text using SpaCy NER.
        """
        doc = nlp(text)
        entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
        return entities

    def fetch_weather_data(self):
        location = 'India'
        response = requests.get(f'{weather_url}/{location}?key={weather_api_key}')
        weather_data = response.json()
        collection.insert_one(weather_data)
    
    def fetch_facebook_data(self):
        response = requests.get(f'{facebook_url}?access_token={facebook_token}')
        fb_data = response.json()
        for post in fb_data['data']:
            post_data = {
                'message': post.get('message', ''),
                'created_time': post.get('created_time', '')
            }
            collection.insert_one(post_data)

    def fetch_instagram_data(self):
        response = requests.get(f'{instagram_url}?fields=id,caption,media_type,media_url,permalink,timestamp&access_token={instagram_token}')
        instagram_data = response.json()
        for media in instagram_data.get('data', []):
            media_data = {
                'id': media.get('id'),
                'caption': media.get('caption', ''),
                'media_type': media.get('media_type'),
                'media_url': media.get('media_url', ''),
                'permalink': media.get('permalink'),
                'timestamp': media.get('timestamp')
            }
            collection.insert_one(media_data)

print('data processed successfully')