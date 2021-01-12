from textblob import TextBlob
import tweepy

api_key = ''
api_secret = ''
acces_token = ''
acces_token_secret = ''
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(acces_token, acces_token_secret)
api = tweepy.API(auth)

# initialize variables
tweet_count = 30
mood, opinion = 0.0, 0.0
mood_tweet_nbr = 0
user = api.me()


# extract tweets from timeline and make sentiment analysis on it
timeline_tweets = api.home_timeline(count=tweet_count)
for tweet in timeline_tweets:
    analysis = TextBlob(tweet.text)
    # some tweets in Chinese or other foreign languages cannot be parsed by textblob, and are given a value of 0.0, exclude those tweets from the results
    if(analysis.sentiment.polarity > 0.0):
        mood += analysis.sentiment.polarity
        opinion += analysis.sentiment.subjectivity
        mood_tweet_nbr += 1
        print(tweet.text)
# calculate the average sentiment and subjectivity of tweets on my time line
mood_avg = mood / mood_tweet_nbr
opinion_avg = opinion / mood_tweet_nbr


# evaluate timeline sentiment and subjectivity average on a scale of 1 to 5, 6 is for any numbers not in sentiment analysis range
def timeline_avg_scale(avg):

    index = 0

    # only evaluates floats
    if not isinstance(avg, float):
        index = 5
        return index

    if(avg < -0.6):
        if (avg < -1.0):
            index = 5
        else:
            index = 0
    elif(avg < -0.2):
        index = 1
    elif (avg < 0.2):
        index = 2
    elif (avg < 0.6):
        index = 3
    elif (avg < 1.0):
        index = 4
    else:
        index = 5

    return index


# on a scale of 0 to 5 what is my timeline's mood
mood_index = timeline_avg_scale(mood_avg)
opinion_index = timeline_avg_scale(opinion_avg)

# lists of words to desribe sentiment and subjectivity
mood_list = ["extremely negative", "negative", "moderate",
             "positive", "extremely positive", "unknown"]
opinion_list = ["totally objective", "objective",
                "neutral", "subjective", "highly subjective", "unknown"]


# data to be output on the user's screen
output_mood = mood_list[mood_index]
output_opinion = opinion_list[opinion_index]
output_str = 'Howdy, {}! Right now, tweets on your timeline are {} and {}.'

# print result on screen
print('average sentiment {} and average subjectivity {}'.format(mood_avg, opinion_avg))
print(output_str.format(user.screen_name, output_mood, output_opinion))
