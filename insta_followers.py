import json
import requests
import argparse
import logging as log

INSTA_FOLLOWINGS = "https://www.instagram.com/graphql/query/?query_hash=3dec7e2c57367ef3da3d987d89f9dbc8&variables=%7B%22id%22%3A%221557645453%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3a10%2c%22after%22%3a%22{}%22%7d"
INSTA_FOLLOWERS = "https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&variables=%7B%22id%22%3A%221557645453%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A10%2C%22after%22%3A%22{}%22%7D"


class instagram_user():

    def __init__(self, csrf_token, sessionid):
        self.cookies = {"csrf_token":csrf_token, "sessionid":sessionid}

    def get_following(self):
        following = []
        has_next_page = True
        end_cursor = ""
        while has_next_page:

            # Send the web request to get the following accounts.
            data = json.loads(requests.get(INSTA_FOLLOWINGS.format(end_cursor), cookies=self.cookies).text)

            # Parse the results from the web.
            has_next_page = data["data"]["user"]["edge_follow"]["page_info"]["has_next_page"]
            end_cursor = data["data"]["user"]["edge_follow"]["page_info"]["end_cursor"]
            edges = data["data"]["user"]["edge_follow"]["edges"]

            # Iterate over the users and insert them to a list.
            for user in edges:
                following.append(user["node"]["username"])

        return following
            
        
    def get_followers(self):
        followers = []
        has_next_page = True
        end_cursor = ""
        while has_next_page:

            # Send the web request to get the followers accounts.
            data = json.loads(requests.get(INSTA_FOLLOWERS.format(end_cursor), cookies=self.cookies).text)

            # Parse the results from the web.
            has_next_page = data["data"]["user"]["edge_followed_by"]["page_info"]["has_next_page"]
            end_cursor = data["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"]
            edges = data["data"]["user"]["edge_followed_by"]["edges"]

            # Iterate over the users and insert them to a list.
            for user in edges:
                followers.append(user["node"]["username"])

        return followers
            

if __name__ == "__main__":

    BANNER = """ __  __   __  ______  ______ ______                                          
/\ \/\ "-.\ \/\  ___\/\__  _/\  __ \                                         
\ \ \ \ \-.  \ \___  \/_/\ \\ \  __ \                                        
 \ \_\ \_\\"\_\/\_____\ \ \_\\ \_\ \_\                                       
 ______/______/\______/ __/_/ \/______  __     __  ______  ______  ______    
/\  ___/\  __ \/\ \    /\ \    /\  __ \/\ \  _ \ \/\  ___\/\  == \/\  ___\   
\ \  __\ \ \/\ \ \ \___\ \ \___\ \ \/\ \ \ \/ ".\ \ \  __\\ \  __<\ \___  \  
 \ \_\  \ \_____\ \_____\ \_____\ \_____\ \__/".~\_\ \_____\ \_\ \_\/\_____\ 
  \/_/   \/_____/\/_____/\/_____/\/_____/\/_/   \/_/\/_____/\/_/ /_/\/_____/ 
   By Yoav Shaharabani
   https://github.com/yoavshah
"""

    print(BANNER)

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    parser.add_argument("--csrf_token", dest='csrf_token', type=str, required=True, help="Csrf_token of your account.")
    parser.add_argument("--sessionid", dest='sessionid', type=str, required=True, help="Sessionid of your account.")
    parser.add_argument("--following_output", dest='following_output', type=str, default=None, help="Path for output file containing all your followings.")
    parser.add_argument("--followers_output", dest='followers_output', type=str, default=None, help="Path for output file containing all your followers.")
    parser.add_argument("--ff_intersection_output", dest='ff_intersection_output', type=str, default="output.txt", help="Path for output file containing those who doesn't follow you while you follow them (Assholes).")
    args = parser.parse_args()

    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.INFO)
        log.info("Verbose output.")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")

    i_user = instagram_user(args.csrf_token, args.sessionid)

    log.info("Creating Instagram Class.")
    log.info("Extracting Account Followers.")
    followers = i_user.get_followers()

    log.info("Extracting Account Following.")
    following = i_user.get_following()

    log.info("Adding those who you follow but do not follow you to the file {}".format(args.ff_intersection_output))
    f = open(args.ff_intersection_output, "w")
    following_not_followers = [item for item in following if item not in followers]
    for i in following_not_followers:
        f.write(i + "\n")
    f.close()

    if args.following_output is not None:
        log.info("Adding accounts you follow to file {}".format(args.following_output))
        f = open(args.following_output, "w")
        for i in following:
            f.write(i + "\n")
        f.close()
    else:
        log.info("Doesn't adding the accounts you follow because --following_output did not specified")

    if args.followers_output is not None:
        log.info("Adding accounts who follow you to file {}".format(args.followers_output))
        f = open(args.followers_output, "w")
        for i in followers:
            f.write(i + "\n")
        f.close()
    else:
        log.info("Doesn't adding the accounts who follow you because --followers_output did not specified")

    log.info("Progress Finished :)")