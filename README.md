# Tweet sentiment analysis

Project fetches Elon Musk's tweets and decides according to sentiment analysis if we should buy or sell fictional Tesla shares.

### Task  
Write a simple Python 3 application which is supposed to trade Tesla stock based on Elon Musk's latest tweets.
Details:
- Once executed, application should wait for a new tweet by Elon
- Once retrieved, sentiment analysis should be performed.
- When sentiment is positive, we buy and vice versa. If the sentiment is neutral, do nothing.
- Instead of actual trading, application should just print "I'm buying" or "I'm selling"
- Once done, wait for another tweet.
- The approach to fetch tweets and how the sentiment analysis is done is up to you.
- Any library can be used.
- The code should be production ready. Include tests in pytest.

### Implementation
Framework [Tweepy](https://docs.tweepy.org/en/stable/) is used to fetch tweets using [Twitter API](https://developer.twitter.com/en/docs/twitter-api). Fetching is implemented by using of streaming and rules for streaming. With the use of bearer token the application authenticates itself with Twitter API and then waits for new incoming tweets from Elon Musk, which are not retweets or replies. When a new tweet is created, sentiment analysis is performed.

For sentiment analysis the framework called [TextBlob](https://textblob.readthedocs.io/en/dev/) is used. It checks for text's sentiment polarity. If the polarity is in interval (0, 1> then it's positive and the program prints "We buy!", if it's in interval <-1, 0) then it's negative and the program prints "We sell!". For polarity equal to 0, the program prints "Neutral, do nothing.".
