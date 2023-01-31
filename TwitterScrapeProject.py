import dataset as dataset
import tweepy, datetime
import time as t
import pandas as pd
from datetime import datetime

auth = tweepy.OAuthHandler('yourapikey',
                           'yourapikeysecret')
auth.set_access_token('youracesstoken',
                      'youraccesstokensecret')
api = tweepy.API(auth)

user_name = ['zg_ops', 'elonmusk']
# replace ‘twitter account’ with your target twitter account
counter = 0
timeline_ids = {}
start_time = datetime.now()
for i in user_name:
 user_object = api.get_user(id = i)
print(f'User screen name is: , {user_object.screen_name}')
print(f'Users id in twitter db is: , {user_object.id}')
print(f'Users info shown on twitter is: , {user_object.name}')
print(f'User was created at: , {user_object.created_at}')
user_id = user_object.id
timeline_ids[user_id] = list()
print(timeline_ids)

# to iterate through each account
for i in timeline_ids:
# scraping the status id and insert it to a list
  for status in tweepy.Cursor(api.user_timeline, user_id = i).items(1000):
# process status here
    timeline_ids[i].append(status.id)
    counter += 1
    print(timeline_ids)

t.sleep(60*15)

# Set looping params
start_time = datetime.now()
raw_tweets = list()
count = 0
for key, values in timeline_ids.items():
 for i in values:
  try:
   res = api.get_status(id = i, tweet_mode = "extended")
   raw_tweets.append({
   "username": key,
   "accident_id": i,
   "created_at": res.created_at,
   "text": res.full_text,
   "len": len(res.full_text),
   "source": res.source,
    })
  except tweepy.TooManyRequests as r:
   print(count)
# check the number of requests
   count += 1
# return error after reached request limit
   print(f'{count}: Rate limit error exceed 900 requests')
   end_time = datetime.now()
   print(end_time-start_time)
   start_time = datetime.now()
# put to sleep for 15 min
   t.sleep(60 * 15)
   end_time = datetime.now()
   print(end_time-start_time)
   end_time = datetime.now()
   print(end_time-start_time)
   print(raw_tweets)

df = pd.DataFrame(raw_tweets)
df.info()
df.to_csv('./dataset/df.csv')
