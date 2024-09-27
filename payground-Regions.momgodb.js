use('Regions');

// Sample NDRF Battalion Articles data for Regions collection
db.getCollection('Regions').insertMany([
  {
    battalion: 1,
    articles: [
      {
        url: 'https://example.com/flood-article1',
        title: 'Floods in Assam: Situation Worsens',
        body: 'The flood situation in Assam has worsened due to heavy rains...',
        preprocessed_text: 'flood situation assam worsen heavy rain',
        sentiment: { pos: 0.2, neu: 0.7, neg: 0.1, compound: 0.5 },
        entities: [{ text: 'Assam', label: 'GPE' }]
      },
      {
        url: 'https://example.com/cyclone-article1',
        title: 'Cyclone Hits Tripura',
        body: 'Cyclone has caused damage to many parts of Tripura...',
        preprocessed_text: 'cyclone cause damage part tripura',
        sentiment: { pos: 0.1, neu: 0.6, neg: 0.3, compound: -0.4 },
        entities: [{ text: 'Tripura', label: 'GPE' }]
      }
    ]
  },
  {
    battalion: 5,
    articles: [
      {
        url: 'https://example.com/drought-article1',
        title: 'Drought in Maharashtra: Farmers Struggle',
        body: 'Farmers in Maharashtra are facing severe drought conditions...',
        preprocessed_text: 'farmer maharashtra face severe drought condition',
        sentiment: { pos: 0.05, neu: 0.75, neg: 0.2, compound: -0.3 },
        entities: [{ text: 'Maharashtra', label: 'GPE' }]
      }
    ]
  }
]);

// Sample Weather Data for WeatherData collection
db.getCollection('WeatherData').insertMany([
  {
    location: 'India',
    temperature: 32,
    humidity: 70,
    description: 'Sunny weather with mild clouds',
    date: new Date()
  },
  {
    location: 'Mumbai',
    temperature: 29,
    humidity: 85,
    description: 'Heavy rainfall expected',
    date: new Date()
  }
]);

// Sample Facebook Data for FacebookData collection
db.getCollection('FacebookData').insertMany([
  {
    message: 'Relief operations ongoing in Assam after severe floods.',
    created_time: new Date('2024-09-20T10:00:00Z')
  },
  {
    message: 'Emergency alert: Cyclone approaching the eastern coast of India.',
    created_time: new Date('2024-09-22T14:30:00Z')
  }
]);

// Sample Instagram Data for InstagramData collection
db.getCollection('InstagramData').insertMany([
  {
    id: '9876543210',
    caption: 'Cyclone aftermath in Kerala. Stay safe!',
    media_type: 'IMAGE',
    media_url: 'https://example.com/cyclone-image.jpg',
    permalink: 'https://example.com/instapost',
    timestamp: new Date('2024-09-23T16:45:00Z')
  },
  {
    id: '1234567890',
    caption: 'Drought conditions in Maharashtra affecting agriculture.',
    media_type: 'VIDEO',
    media_url: 'https://example.com/drought-video.mp4',
    permalink: 'https://example.com/instapost2',
    timestamp: new Date('2024-09-24T09:15:00Z')
  }
]);

// Query example: Find articles related to floods
const floodArticles = db.getCollection('Regions').find({
  'articles.title': { $regex: /Flood/, $options: 'i' }
}).toArray();

console.log(`Found ${floodArticles.length} articles related to floods.`);

// Aggregate average temperature from WeatherData collection
const avgTemperature = db.getCollection('WeatherData').aggregate([
  {
    $match: {
      temperature: { $exists: true }
    }
  },
  {
    $group: {
      _id: null,
      avgTemp: { $avg: '$temperature' }
    }
  }
]).toArray();

console.log(`Average temperature: ${avgTemperature.length > 0 ? avgTemperature[0].avgTemp : 'No data available'}`);

