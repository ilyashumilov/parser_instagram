import instaloader

class parser:
    def __init__(self):
        self.loader = instaloader.Instaloader()
        username = "siesdemayo"
        password = "misa09misa09"
        self.loader.login(username, password)  # (login)

    def get(self,target):
        profile = instaloader.Profile.from_username(self.loader.context, target)
        follower = profile.get_followers()
        followee = profile.get_followees()

        post = profile.get_posts()

        result = {
            'username':target,
            'followers':[],
            'followees':[],
            'posts':0
        }

        for i in follower:
            result['followers'].append(i.username)

        for i in followee:
            result['followees'].append(i.username)
        for i in post:
            result['posts']+=1

        return result

print(parser().get('siesdemayo'))

