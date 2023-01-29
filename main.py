import tweepy
from textblob import TextBlob

bearer_token = "AAAAAAAAAAAAAAAAAAAAALkMlgEAAAAAyxxUFodsMp0hTCvS6d%2FLLyUzoys%3Dq0X80xScx1avqTKpIRISOd4r59gDRox8RbjMtLr8Bm0ISMaV22"

client = tweepy.Client(bearer_token=bearer_token)

def get_user_id(username):
    response = client.get_user(username=username)

    return response.data.id


def fetch_last_tweet(user_id):
    tweet = client.get_users_tweets(id=user_id, exclude="retweets,replies", max_results=5)

    return tweet.data[3]


def analyze_text_sentiment(text):
    analyzer = TextBlob(text)
    # print("polarity value:", analyzer.sentiment.polarity)
    if analyzer.sentiment.polarity > 0:
        print("We buy!")
    elif analyzer.sentiment.polarity < 0:
        print("We sell!")
    else:
        print("Neutral, do nothing.")


def main():
    user_id = get_user_id("elonmusk")

    last_tweet = fetch_last_tweet(user_id)
    print("Tweet:", last_tweet.text)
    analyze_text_sentiment(last_tweet.text)


if __name__ == '__main__':
    main()
