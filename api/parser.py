import requests
import urllib.parse
import time
import random

class inst_parser:
    def __init__(self):
        self.session = requests.Session()
        self.proxies = [{
            "https": 'http://wsmnsp:y5oPmM@45.155.202.141:8000',
        },
            {
                "https":'http://5Xyja7:xCMhBm@181.177.84.199:9891'
            }
        ]

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'
        }

        self.cookies = [{
            "csrftoken": 'OpPclisiGGuTD1nAfMbdNywt6Rzrqr5o',
            "sessionid": '53040905701%3ABmn03S1JnWMo4u%3A15'
        },
            {
                "csrftoken": '1LjkYhxytrrQT9AMlgbTae2pu9cK7wDs',
                "sessionid": '53046025259%3A364uTZJmce9JTY%3A8'
            },
            {
                "csrftoken": 'eehM8wEtTM3svRQU822U6shS25SMZrxR',
                "sessionid": '52683570214%3AKgz1fC9lu9Sa0E%3A1'
            }
        ]

    def get_page(self,username):
        self.start = time.time()

        self.session.proxies.update(self.proxies[0])
        self.session.cookies.update(self.cookies[1])
        self.session.headers.update(self.headers)
        result = {}

        response = self.session.get(f'https://www.instagram.com/{username}/?__a=1')
        # print(response.json())

        # result['posts amount'] = response.json()['graphql']['user']['edge_owner_to_timeline_media']['count']
        id = response.json()['graphql']['user']['id']

        has_next_page = True
        variables = '{"id":"' + str(id) +'","first":50}'
        result['followers']=[]
        turn = 1

        while has_next_page:
            response = self.session.get(f'https://www.instagram.com/graphql/query/?query_hash=37479f2b8209594dde7facb0d904896a&variables={urllib.parse.quote(variables)}').json()
            # print(response)
            has_next_page = response['data']['user']['edge_followed_by']['page_info']['has_next_page']

            end_cursor = response['data']['user']['edge_followed_by']['page_info']['end_cursor']
            # print(end_cursor)

            variables = '{"id":"' + str(id) + '","first":50,"after":"'+end_cursor+'"}'
            # print(variables)
            # print(response['data']['user']['edge_followed_by']['edges'])
            for i in response['data']['user']['edge_followed_by']['edges']:
                print(len(result['followers']))
                result['followers'].append({'username':i['node']['username'],'id':i['node']['id']})

                if len(result['followers']) == 50 or len(result['followers']) == 100 or len(result['followers']) == 500:
                    print(time.time() - self.start, '   ', len(result['followers']))
                    time.sleep(0.1)

                if len(result['followers'])%1000 == 0:
                    print(time.time()-self.start,'   ',len(result['followers']))
                    time.sleep(random.uniform(0.5, 2.5))

                if len(result['followers']) % 5124:
                    time.sleep(random.uniform(5,15))

                if len(result['followers'])%8940 == 0:
                    self.session.proxies.update(self.proxies[turn])
                    if turn == 1:
                        turn = 0
                    else:
                        turn = 1

                # if len(result['followers']) == (int(str(len(result['followers'][0])))+stopper):
                #     time.sleep(random.uniform(3, 5))


        # import random
        # import time
        # for i in range(10):
        #     a = random.uniform(0.5, 2.5)
        #     print(a)
        #     time.sleep(a)
        # has_next_page = True
        # variables = '{"id":"' + str(id) +'","first":12}'
        # result['followees'] = []

        # while has_next_page:
        #     response = self.session.get(f'https://www.instagram.com/graphql/query/?query_hash=58712303d941c6855d4e888c5f0cd22f&variables={urllib.parse.quote(variables)}').json()
        #     has_next_page = response['data']['user']['edge_follow']['page_info']['has_next_page']
        #     end_cursor = response['data']['user']['edge_follow']['page_info']['end_cursor']
        #     variables = '{"id":"' + str(id) + '","first":12,"after":"'+end_cursor+'"}'
        #     for i in response['data']['user']['edge_follow']['edges']:
        #         result['followees'].append(i['node']['username'])
        #     time.sleep(randint(0, 2))

        return result

start = time.time()
inst_parser().get_page('daddyyankee')
print(time.time()-start)

#
# if __name__ == '__main__':
#     print(inst_parser().get_page('the_tyrant_eye'))


#
# start = time()
# print(requests.get('https://instaparserapi.herokuapp.com/?username=siesdemayo').json())
# print(time()-start)