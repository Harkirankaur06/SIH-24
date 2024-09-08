use('disasterData');

// insert documents into the collection
db.getCollection('TechTitans').insertMany([
  {
    url: 'https://example.com/article1',
    title: 'Sample Article Title 1',
    body: 'This is a sample body of the article 1.',
  },
  {
    url: 'https://example.com/article2',
    title: 'Sample Article Title 2',
    body: 'This is a sample body of the article 2.',
  }
]);

// eg data for Weather API 
db.getCollection('TechTitans').insertMany([
  {
    location: 'India',
    temperature: 30, 
    humidity: 80,    
    description: 'Clear sky', 
    date: new Date() 
  }
]);

// eg data for Facebook 
db.getCollection('TechTitans').insertMany([
  {
    message: 'Sample Facebook post message.',
    created_time: new Date() 
  }
]);

// eg data for Instagram 
db.getCollection('TechTitans').insertMany([
  {
    id: '1234567890',
    caption: 'Sample Instagram caption',
    media_type: 'IMAGE',
    media_url: 'https://example.com/media.jpg',
    permalink: 'https://example.com/post',
    timestamp: new Date() 
  }
]);

const articles = db.getCollection('TechTitans').find({
  title: { $regex: /Sample Article/ } // query to find articles with Sample Article in the title
}).toArray();

console.log(`Found ${articles.length} articles.`);

const totalWeatherData = db.getCollection('TechTitans').aggregate([
  {
    $match: {
      temperature: { $exists: true } // Match documents with temperature field
    }
  },
  {
    $group: {
      _id: null,
      averageTemperature: { $avg: '$temperature' }
    }
  }
]).toArray();

console.log(`Average temperature: ${totalWeatherData.length > 0 ? totalWeatherData[0].averageTemperature : 'No data available'}`);
