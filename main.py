import sys
import tweepy
from textblob import TextBlob

bearer_token = "AAAAAAAAAAAAAAAAAAAAALkMlgEAAAAAyxxUFodsMp0hTCvS6d%2FLLyUzoys%3Dq0X80xScx1avqTKpIRISOd4r59gDRox8RbjMtLr8Bm0ISMaV22"

# Tweepy client creates session connection to twitter
client = tweepy.Client(bearer_token=bearer_token)


def get_user_id(username):
    """
    Gets unique twitter user id by their username.
    :param username:
    :return: user id from endpoint call which is associated with this twitter username
    """

    response = client.get_user(username=username)
    if response.data is None:
        raise Exception("User with specified username doesn't exist.")

    return response.data.id


def fetch_latest_tweet(user_id):
    """
    Gets latest user tweet which is not a retweets or a reply.
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


def main():
    try:
        user_id = get_user_id("elonmusk")

        last_tweet = fetch_latest_tweet(user_id)
        print("Tweet:", last_tweet.text)

        analysis_result = analyze_text_sentiment(last_tweet.text)
        print(analysis_result)

    except Exception as e:
        print("Exception:", e)
        sys.exit(1)


if __name__ == '__main__':
    main()
