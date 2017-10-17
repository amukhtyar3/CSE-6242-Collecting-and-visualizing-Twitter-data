import csv
import json
import time
import tweepy


# You must use Python 2.7.x
# Rate limit chart for Twitter REST API - https://dev.twitter.com/rest/public/rate-limits

def loadKeys(key_file):
    with open(key_file,'r') as file:
        json_decode=json.load(file)
        
    api_key=str(json_decode['api_key'])
    api_secret=str(json_decode['api_secret'])
    token=str(json_decode['token'])
    token_secret=str(json_decode['token_secret'])
    # TODO: put your keys and tokens in the keys.json file,
    #       then implement this method for loading access keys and token from keys.json
    # rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>

    # Load keys here and replace the empty strings in the return statement with those keys
 
    return api_key,api_secret,token,token_secret

# Q1.b.(i) - 5 points
def getPrimaryFriends(api, root_user, no_of_friends):
   
    primary_friends = []
    friends_user = api.friends(root_user, count=no_of_friends)
    for friend in friends_user:
        primary_friends.append((root_user, friend._json['screen_name']))
    return primary_friends
# TODO: implement the method for fetching 'no_of_friends' primary friends of 'root_user'
# rtype: list containing entries in the form of a tuple (root_user, friend)


# Q1.b.(ii) - 7 points
def getNextLevelFriends(api, friends_list, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends for each entry in friends_list
    # rtype: list containing entries in the form of a tuple (friends_list[i], friend)
    next_level_friends = []
    
    for main_user, sec_user in friends_list:
        user_friends = [x[1] for x in getPrimaryFriends(api, sec_user, no_of_friends)]
        next_level_friends.append((user_friends, sec_user))
        
    # Add code here to populate next_level_friends
    return next_level_friends

# Q1.b.(iii) - 7 points
def getNextLevelFollowers(api, followers_list, no_of_followers):
    
   # primary_followers = []
   #followers = api.followers(root_user, count=no_of_followers)
    #for follower in followers:
        #primary_followers.append((follower._json['screen_name'], root_user))
    # TODO: implement the method for fetching 'no_of_followers' followers for each entry in followers_list
    # rtype: list containing entries in the form of a tuple (follower, followers_list[i])
     # Add code here to populate next_level_followers
    next_level_followers = []
    
    for user, root_user in followers_list:
        followers = api.followers(root_user, count=no_of_followers)
        
        for follower in followers:       
            next_level_followers.append((follower._json['screen_name'], root_user))

    return next_level_followers

# Q1.b.(i),(ii),(iii) - 4 points
def GatherAllEdges(api, root_user, no_of_neighbours):
   
    # TODO:  implement this method for calling the methods getPrimaryFriends, getNextLevelFriends
    #        and getNextLevelFollowers. Use no_of_neighbours to specify the no_of_friends/no_of_followers parameter.
    #        NOT using the no_of_neighbours parameter may cause the autograder to FAIL.
    #        Accumulate the return values from all these methods.
    # rtype: list containing entries in the form of a tuple (Source, Target). Refer to the "Note(s)" in the
    #        Question doc to know what Source node and Target node of an edge is in the case of Followers and Friends.
    all_edges = []
    

    primary_friends = getPrimaryFriends(api, root_user, no_of_neighbours)
    second_friends = getNextLevelFriends(api, primary_friends, no_of_neighbours)
    next_level_followers = getNextLevelFollowers(api,primary_friends, no_of_neighbours)
    
    

    # Add code here to populate primary_friends
    all_edges=primary_friends+second_friends+next_level_followers
    #Add code here to populate all_edges
    return all_edges


# Q1.b.(i),(ii),(iii) - 5 Marks
def writeToFile(data, output_file):
    file_list = []
    for x,y in data:
        if type(y) == list:
            for every_user in y:
                row = {}
                row['source'] = every_user
                row['target'] = x
                file_list.append(row)
        elif type(x) == list:
            for every_user in x:
                row = {}
                row['source'] = y
                row['target'] = every_user
                file_list.append(row)
        else:
            row = {}
            row['source'] = x
            row['target'] = y
            file_list.append(row)

    csvfile = open(output_file, 'w')
    fieldnames = ['source', 'target']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    for every_row in file_list:
        writer.writerow(every_row)
    csvfile.close()
    # write data to output_file
    # rtype: None





"""
NOTE ON GRADING:

We will import the above functions
and use testSubmission() as below
to automatically grade your code.

You may modify testSubmission()
for your testing purposes
but it will not be graded.

It is highly recommended that
you DO NOT put any code outside testSubmission()
as it will break the auto-grader.

Note that your code should work as expected
for any value of ROOT_USER.
"""

def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_GRAPH = 'graph.csv'
    NO_OF_NEIGHBOURS = 20
    ROOT_USER = 'PoloChau'
    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth, wait_on_rate_limit= True)

    edges = GatherAllEdges(api, ROOT_USER, NO_OF_NEIGHBOURS)

    writeToFile(edges, OUTPUT_FILE_GRAPH)


if __name__ == '__main__':
    testSubmission()
