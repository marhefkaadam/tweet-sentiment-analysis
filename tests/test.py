import pytest
from mock import Mock
import tweepy
from tweepy import Response

from main import *

bearer_token = "AAAAAAAAAAAAAAAAAAAAALkMlgEAAAAAyxxUFodsMp0hTCvS6d%2FLLyUzoys%3Dq0X80xScx1avqTKpIRISOd4r59gDRox8RbjMtLr8Bm0ISMaV22"
client = tweepy.Client(bearer_token=bearer_token)


def test_get_user_id_fail():
    with pytest.raises(Exception):
        get_user_id(client, "testtest-nonexistent")
    with pytest.raises(Exception):
        get_user_id(client, "")


def test_get_user_id_success():
    assert get_user_id(client, "elonmusk") == 44196397
    assert get_user_id(client, "general_pavel") == 4136554833


def test_fetch_latest_tweet_fail():
    with pytest.raises(Exception):
        fetch_latest_tweet(client, 0)

    with pytest.raises(Exception):
        fetch_latest_tweet(client, 10)


def test_fetch_latest_tweet_success():
    tweet = fetch_latest_tweet(client, 992889944048840706)
    assert tweet.text == "Let me google that for you!"


def test_analyze_text_sentiment():
    positive = "We buy!"
    negative = "We sell!"
    neutral = "Neutral, do nothing."

    assert analyze_text_sentiment("Success!") == positive
    assert analyze_text_sentiment("What a great day today.") == positive
    assert analyze_text_sentiment("Horrible day today!") == negative
    assert analyze_text_sentiment("I hate when somebody makes a mess!") == negative
    assert analyze_text_sentiment("Well..") == neutral
    assert analyze_text_sentiment("Yo soy Peter") == neutral
    assert analyze_text_sentiment("") == neutral
    assert analyze_text_sentiment("Einundzwanzig luftbalons") == neutral


def test_my_streaming_client_on_tweet(capfd, mocker):
    streaming_client = MyStreamingClient(bearer_token=bearer_token)

    mocker.patch("main.analyze_text_sentiment", return_value="Mocked")

    tweet_text = "Testing tweet."
    streaming_client.on_tweet(tweepy.Tweet({"id": 0, "text": tweet_text}))

    stdout = capfd.readouterr()
    assert stdout.out == "New tweet: " + tweet_text + "\nDecision based on sentiment analysis: Mocked\n"


def test_my_streaming_client_on_error(capfd):
    streaming_client = MyStreamingClient(bearer_token=bearer_token)

    status_code = 409
    streaming_client.on_request_error(status_code)

    stdout = capfd.readouterr()
    assert stdout.out == "Error on request, status code: " + str(status_code) + "\nConnection closed...\n"

