import sys
from time import sleep
import tweepy
from textblob import TextBlob
from tweepy import StreamRule

bearer_token = ""


def get_user_id(client, username):
    """
    Gets unique twitter user id by their username.
    :param client: used for connection using Twitter API
    :param username:
    :return: user id from endpoint call which is associated with this twitter username
    """

    response = client.get_user(username=username)
    if response.data is None:
        raise Exception("User with specified username doesn't exist.")

    return response.data.id


def fetch_latest_tweet(client, user_id):
    """
    Gets latest user tweet which is not a retweets or a reply.
    :param client: used for connection using Twitter API
    :param user_id: unique twitter user id
    :return: Last tweet posted by the user. Returns data from tweepy.Response.
    """
    response = client.get_users_tweets(id=user_id, exclude="retweets,replies", max_results=5)
    if response.data is None:
        raise Exception("There were no tweets found.")

    return response.data[0]


def analyze_text_sentiment(text):
    """
    Analyzes text sentiment using TextBlob. According to polarity determines if the text sentiment is positive,
    negative or neutral. Sentiment by polarity values: (0, 1> - positive, <-1, 0) - negative, 0 - neutral
    :param text: text to analyze sentiment on
    :return: text result depending on text sentiment
    """
    analyzer = TextBlob(text)
    # print("polarity value:", analyzer.sentiment.polarity)
    if analyzer.sentiment.polarity > 0:
        return "We buy!"
    elif analyzer.sentiment.polarity < 0:
        return "We sell!"
    else:
        return "Neutral, do nothing."


class MyStreamingClient(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        """
        Overridden method prints new incoming tweet and does sentiment analysis on text from the tweet.
        :param tweet:
        :return:
        """
        print("New tweet:", tweet.text)
        analysis_result = analyze_text_sentiment(tweet.text)
        print("Decision based on sentiment analysis:", analysis_result)

    def on_request_error(self, status_code):
        """
        Prints error code to output and safely disconnects from stream.
        :param status_code:
        :return:
        """
        print("Error on request, status code:", status_code)
        self.disconnect()
        print("Connection closed...")

    def on_closed(self, response):
        print("Connection closed...")


def main():
    try:
        # First approach: could be fetching tweets regularly in a loop and checking if the tweet is different from
        # previously fetched tweet - not as good as the second approach so i scraped it
        # Tweepy client creates session connection to twitter
        # client = tweepy.Client(bearer_token=bearer_token)
        # user_id = get_user_id(client, "elonmusk")
        # last_tweet = fetch_latest_tweet(client, user_id)
        # print("New tweet:", last_tweet.text)

        # analysis_result = analyze_text_sentiment(last_tweet.text)
        # print(analysis_result)

        # Second approach: constant waiting for new tweets using tweepy StreamingClient
        streaming_client = MyStreamingClient(bearer_token=bearer_token)
        # rules are defined to filter new incoming tweets by user and type of tweet
        rules = StreamRule("from:elonmusk -is:retweet -is:reply")
        streaming_client.add_rules(rules)

        print("Started client streaming...")
        streaming_client.filter(threaded=True)
        sleep(100)
        streaming_client.disconnect()

    except Exception as e:
        print("Exception:", e)
        sys.exit(1)


if __name__ == '__main__':
    main()
