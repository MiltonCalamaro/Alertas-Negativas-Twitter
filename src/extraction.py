import datetime as dt
import pandas as pd
from twitterscraper.query import query_tweets
from twitterscraper.query import query_user_info

global today,tomorrow,meses

today = dt.date.today()
tomorrow = dt.date.today() + dt.timedelta(days=1)
meses={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

def get_tweet(query,limit=None,begindate=today,enddate=tomorrow,poolsize=20,lang=" "):
  list_tweet=[]
  if enddate != tomorrow:
    enddate=enddate + dt.timedelta(days=1)
  list_text=query_tweets(query, limit=limit,begindate=begindate ,enddate=enddate, poolsize=poolsize, lang=lang) ## es 
  hour_per = dt.timezone(dt.timedelta(hours=-5))#Configurar la zona horaria 
  for tweet in list_text:
        dict_ = {# user name & id
                "screen_name":tweet.screen_name,
                "username":tweet.username,
                "user_id":tweet.user_id,
                # tweet basic data
                "tweet_id":tweet.tweet_id,
                "tweet_url":tweet.tweet_url,
                "timestamp":tweet.timestamp.astimezone(hour_per),
                "timestamp_epochs":tweet.timestamp_epochs,
                # tweet text
                "text":tweet.text,
                "text_html":tweet.text_html,
                "links":tweet.links,
                "hashtags":tweet.hashtags,
                # tweet media
                "has_media":tweet.has_media,
                "img_urls":tweet.img_urls,
                "video_url":tweet.video_url,
                # tweet actions numbers
                "likes":tweet.likes,
                "retweets":tweet.retweets,
                "replies":tweet.replies,
                "is_replied":tweet.is_replied,
                # detail of reply to others
                "is_reply_to":tweet.is_reply_to,
                "parent_tweet_id":tweet.parent_tweet_id,
                "reply_to_users":tweet.reply_to_users
                }
        list_tweet.append(dict_)
  df=pd.DataFrame(list_tweet).sort_values(by="timestamp",ascending=False)
  df.drop_duplicates(subset=["user_id","tweet_id"],keep="first",inplace=True)
  df.index=[i for i in range(0,len(df))]
  return df

def replace(x):
  val=x.split("-")[1].split()[1]
  x=x.split("-")[1].replace(val,str(meses[val])).strip().replace(" ","/")
  return x

def get_user_info(twitter_user):
    try:
      user_info = query_user_info(user= twitter_user)
      twitter_user_data = {}
      twitter_user_data["screen_name"] = user_info.user
      twitter_user_data["username"] = user_info.full_name
      twitter_user_data["location"] = user_info.location
      twitter_user_data["blog"] = user_info.blog
      twitter_user_data["date_joined"] = dt.datetime.strptime(replace(user_info.date_joined),'%d/%m/%Y')
      twitter_user_data["user_id"] = user_info.id
      twitter_user_data["num_tweets"] = user_info.tweets
      twitter_user_data["following"] = user_info.following
      twitter_user_data["followers"] = user_info.followers
      twitter_user_data["likes"] = user_info.likes
      twitter_user_data["lists"] = user_info.lists
    except:
      twitter_user_data="None"
    return twitter_user_data

 
    
    
    
    
    
    
    
    
    
    
    
    