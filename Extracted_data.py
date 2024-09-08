import scrapy
from pymongo import MongoClient
import requests
import json

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

# Scrapy Spider Class
class DisasterSpider(scrapy.Spider):
    name = "disaster_spider"
    
    start_urls = [
        # Add your news channels and IMD URLs here
        'https://www.ndtv.com/latest',
        'https://timesofindia.indiatimes.com/', 
        'https://www.hindustantimes.com/latest-news',
        'https://mausam.imd.gov.in/'  # Indian Meteorological Department
        'https://reliefweb.int/disaster/fl-2024-000109-ind'
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

        # Store scraped data in MongoDB
        article_data = {
            'url': response.url,
            'title': title,
            'body': body_text
        }
        collection.insert_one(article_data)
        yield article_data

        # Fetch data from other APIs
        # self.fetch_twitter_data()
        self.fetch_weather_data()
        self.fetch_facebook_data()

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
        # Replace 'fields' with the fields you need
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

    print("Data imported successfully!")