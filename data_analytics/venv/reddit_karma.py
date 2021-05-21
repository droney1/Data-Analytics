import praw

reddit = praw.Reddit(
     client_id = 'MlOYtpXekoiY5w',
     client_secret = 'lKVj3LXSyTU-1vo4ug9M1Ruz0eE',
     user_agent = 'my user agent')

reddits = open("reddit_results.txt", "r")
top_posts = open("top_posts.txt", "w+")
users_karma = open("users_karma.txt", "w+")

author_list = []

for line in reddits:
    try:
        line = line.split()
        top_posts.write("Subreddit: r/" + line[0] + "\n")
        users_karma.write("Subreddit: r/" + line[0] + "\n")
        
        for submission in reddit.subreddit(line[0]).hot(limit=10):   #limit should equal 10
            top_posts.write(submission.title + "\n")

            for comment in reddit.subreddit(line[0]).comments(limit = 5): #limit may be either 5 or 10
                user = comment.author
                if user.name not in author_list:
                    author_list.append(user.name)
                    redditor = reddit.redditor(user.name)
                    users_karma.write("User: " + str(user.name) + ", Comment Karma: " + str(redditor.comment_karma) + "\n")
                else:
                    limit += 1

            top_posts.write("-----------------------------\n")
            users_karma.write("-----------------------------\n")

    except Exception:
        pass

