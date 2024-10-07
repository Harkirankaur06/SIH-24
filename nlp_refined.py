import scrapy
from pymongo import MongoClient
import requests
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
from pathlib import Path

# MongoDB client and database
client = MongoClient('mongodb+srv://disasterData:sihdata2024@techtitans.jnat6.mongodb.net/')
db = client['disasterData']
regions_collection = db['Regions']  # Single collection for regions

# Weather API and Facebook API credentials
weather_api_key = '8D7MK5WEBZNC6BW2FCHVMFN7Z'
weather_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'
facebook_token = 'EAAS4lSZAw7PUBO084REr3KgVj06WVzL09yZBLEY2jhaxM0NVSTUTmuiLUkDl0n97pv1xHzwNZBVkwpZADYr1FsAfHNarZBQriL9Ob8Qq0riTRZBRYDYjrou4amsTQOO3VKTpbxgs1BF5u0isGllKZArOvbYVHcnK2hALmK4XfHnZCJTsRPptATj80AtRZBmUaXir94HJX8sDazhtE468xO4aznqeeSiZAb39gO8Kdk4GKLSWEld7eS8FZCoBFs6ZCGoxRBgefI3gx7AZD'
facebook_url = 'https://graph.facebook.com/v11.0/me/feed'

# NLP and Sentiment Analyzer setup
nlp = spacy.load('en_core_web_sm')
analyzer = SentimentIntensityAnalyzer()

# NDRF battalion mapping to regions/states
ndrf_battalions = {
    1: ["Assam", "Meghalaya", "Nagaland", "Manipur", "Mizoram", "Tripura", "Arunachal Pradesh"],
    2: ["West Bengal", "Sikkim"],
    3: ["Odisha", "Andaman and Nicobar Islands"],
    4: ["Tamil Nadu", "Karnataka", "Kerala"],
    5: ["Maharashtra", "Goa", "Madhya Pradesh"],
    6: ["Gujarat"],
    7: ["Punjab", "Haryana", "Chandigarh", "Himachal Pradesh", "Jammu & Kashmir"],
    8: ["Uttar Pradesh"],
    9: ["Bihar", "Jharkhand"],
    10: ["Andhra Pradesh", "Telangana"],
    11: ["Uttar Pradesh"],
    12: ["Arunachal Pradesh"],
    13: ["Punjab", "Jammu & Kashmir"],
    14: ["Himachal Pradesh"],
    15: ["Uttarakhand"],
    16: ["Delhi", "Haryana"]
}

class DisasterSpider(scrapy.Spider):
    name = "disaster_spider"
    
    start_urls = [
        # 'https://www.ndtv.com/latest',
        # 'https://timesofindia.indiatimes.com/',
        # 'https://www.hindustantimes.com/latest-news',
        # 'https://mausam.imd.gov.in/',
        # 'https://reliefweb.int/disaster/fl-2024-000109-ind',
        # 'https://reliefweb.int/disaster/tc-2024-000083-bgd'
        'https://gist.github.com/Rashi1575/20f26918f1ff71c6d25355c2cd81a1b0.js' #Flood
    ]
    
    keywords = ['earthquake', 'flood', 'cyclone', 'landslide', 'tsunami', 'drought']
    
    def parse(self, response):
        # Extracting articles from the webpage
        for article in response.xpath('//a/@href').extract():
            if any(keyword in article.lower() for keyword in self.keywords):
                yield scrapy.Request(response.urljoin(article), callback=self.parse_article)

    def parse_article(self, response):
        # Extract title and body of the article
        title = response.xpath('//title/text()').get()
        body = response.xpath('//p/text()').getall()
        body_text = ' '.join(body)

        # Text preprocessing and NER extraction
        preprocessed_text = self.preprocess_text(body_text)
        sentiment = self.analyze_sentiment(preprocessed_text)
        entities = self.extract_entities(preprocessed_text)

        # Separate and store data by battalion (NDRF region)
        self.store_data_by_battalion(response.url, title, body_text, preprocessed_text, sentiment, entities)

        # Optional: Fetching real-time weather and social media data
        self.fetch_weather_data()
        self.fetch_facebook_data()

    def preprocess_text(self, text):
        # Tokenization, lemmatization, and stopword removal
        doc = nlp(text)
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return ' '.join(tokens)

    def analyze_sentiment(self, text):
        # Sentiment analysis using VADER
        sentiment_scores = analyzer.polarity_scores(text)
        return sentiment_scores

    def extract_entities(self, text):
        # Named Entity Recognition (NER) to extract locations
        doc = nlp(text)
        entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
        return entities

    def store_data_by_battalion(self, url, title, body, preprocessed_text, sentiment, entities):
        # Group the data based on NDRF battalions
        for entity in entities:
            if entity['label'] == 'GPE':  # GPE: Geopolitical entity (states, cities, etc.)
                state_name = entity['text']
                for battalion, states in ndrf_battalions.items():
                    if state_name in states:
                        # Create the data to be stored
                        article_data = {
                            'url': url,
                            'title': title,
                            'body': body,
                            'preprocessed_text': preprocessed_text,
                            'sentiment': sentiment,
                            'entities': entities
                        }

                        # Step 1: Write this data into a JSON file
                        self.create_json_file(battalion, article_data)

                        # Step 2: Push this data into MongoDB
                        regions_collection.update_one(
                            {'battalion': battalion},
                            {'$push': {'articles': article_data}},
                            upsert=True
                        )
                        break


    def fetch_weather_data(self):
        # Fetch real-time weather data from Visual Crossing
        location = 'India'
        response = requests.get(f'{weather_url}/{location}?key={weather_api_key}')
        weather_data = response.json()
        # Store weather data in the general collection
        db['WeatherData'].insert_one(weather_data)

    def fetch_facebook_data(self):
        # Fetch social media data from Facebook
        response = requests.get(f'{facebook_url}?access_token={facebook_token}')
        fb_data = response.json()
        for post in fb_data['data']:
            post_data = {
                'message': post.get('message', ''),
                'created_time': post.get('created_time', '')
            }
            # Store Facebook post data in the general collection
            db['FacebookData'].insert_one(post_data)

    def fetch_instagram_data(self):
        # Fetch Instagram media data
        instagram_token = 'EAAS4lSZAw7PUBO7etXirCUzVqILefGbWHpAoKux5wr6YiIbDtPSMseuWyFlDqMQNGFD68kHItobIoyjXTzziJBbNBgjgltUQQ0gKI0U5Khfqv94jZC0aaHH5rDMdLGbbm2rmq2bmbN1eOjeZA78AqGIykZA4N8OZARBIbXV2ZBR1mrW5MQ0FBwD8CGKFYd5ZC1OfYZAAv5zHU3Olx0fV9z3B50Y4oQZDZD'
        instagram_url = 'https://graph.instagram.com/me/media'
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
            # Store Instagram data in the general collection
            db['InstagramData'].insert_one(media_data)


print('Data processed successfully')

