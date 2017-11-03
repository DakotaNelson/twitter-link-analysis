import time

import tweepy
import dataset

from config import config

db = dataset.connect('sqlite:///tweet_data.db')
followees_table = db['followees']
links_table = db['links']

class LinkStreamer(tweepy.StreamListener):
    def on_status(self, status):
        # do this to every tweet we recieve
        if 'urls' in status.entities:
            # has a URL!
            for url in status.entities['urls']:
                link = {"time": time.time(), "link": url['expanded_url']}
                links_table.insert(link)
                print(url['expanded_url'])
        else:
            # does not have a URL :(
            print("[!] Found a Tweet without any URLs. Weird.")
            pass

    def on_error(self, status_code):
        if status_code == 420:
            # code 420 means we are exceeding the rate limit
            #returning False disconnects the stream
            return False

def limit_handled(cursor):
    """ iterate through a list returned by Tweepy, sleeping each time it hits
    the rate limit """
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print("[!] Rate limit error, sleeping...")
            time.sleep(15 * 60)

def getFolloweeIds(api):
    followees = []
    for followee in limit_handled(tweepy.Cursor(api.friends_ids, user_id=config['user']).items()):
        followees.append(str(followee))
    return followees

if __name__ == "__main__":
    # auth with Twitter
    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])
    api = tweepy.API(auth)

    # get a list of user IDs of the people you follow
    followees = getFolloweeIds(api)
    for followee in followees:
        followees_table.insert({'time': time.time(), 'user_id':followee})
    print("User to analyze has {} followees.".format(len(followees)))

    # set up the streamer
    linkStreamer = LinkStreamer()
    linkStream = tweepy.Stream(auth=api.auth, listener=linkStreamer)

    # only return tweets with links
    # https://developer.twitter.com/en/docs/tweets/rules-and-filtering/overview/basic-operators
    track_terms = ['filter:links']
    linkStream.filter(follow=followees, track=track_terms)
