# TweetCrawler

Tweet Crawler to get all the tweets from @realDonaldTrump. If only he still was POTUS. :/

## Docker

- Pull Repo

- Build: docker build -t tweet-crawler . 

- Run:  docker run -p 5000:5000 tweet-crawler python3 app.py penguinrage


## API

- Endpoint: 0.0.0.0:5000/tweets

## Manual Python

- Pull repo

- create virtual environment with Python 3

- Pip install requirements.txt into Virtual Environment

- Execute Program: python app.py realdonaldtrump (no @ required)

## Food for Thought

When working on this challenge, I was also considering using Selinium and PhantomJS (Headless Browser). Upon discovering syndicate.twitter.com I was able to use the iframe for Twitter widgets rolled nicely into JSON to extract info with Beautiful Soup.

From this point on I rolled what I got from the iframe up into my own objects to keep things structured nicely. 

For this challenge alone, I also didn't do much for Error Handling, testing or moving classes out into seperate python files and folders to structure the project in a neater way. Ideally I would by my behaviour want to have these things included.
