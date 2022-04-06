import requests
import urllib.parse

class inst_parser:
    def __init__(self):
        self.session = requests.Session()
        self.proxies = {
            "https": 'http://wsmnsp:y5oPmM@45.155.202.141:8000',
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'
        }


        self.cookies = {
            "csrftoken": 'nErXhCyIvuZl3QDaHnh70ntZVlYvPeoD',
            "sessionid": '47338734226%3AvKJPWABt08bZDC%3A14'
        }

    def get_page(self,username):
        # self.session.proxies.update(self.proxies)
        self.session.cookies.update(self.cookies)
        self.session.headers.update(self.headers)
        result = {}

        response = self.session.get(f'https://www.instagram.com/{username}/?__a=1')
        print(response.text)

        result['posts amount'] = response.json()['graphql']['user']['edge_owner_to_timeline_media']['count']
        id = response.json()['graphql']['user']['id']

        has_next_page = True
        variables = '{"id":"' + str(id) +'","first":12}'
        result['followers']=[]

        while has_next_page:
            response = self.session.get(f'https://www.instagram.com/graphql/query/?query_hash=37479f2b8209594dde7facb0d904896a&variables={urllib.parse.quote(variables)}').json()
            # print(response)
            has_next_page = response['data']['user']['edge_followed_by']['page_info']['has_next_page']
            end_cursor = response['data']['user']['edge_followed_by']['page_info']['end_cursor']
            variables = '{"id":"' + str(id) + '","first":12,"after":"'+end_cursor+'"}'
            for i in response['data']['user']['edge_followed_by']['edges']:
                result['followers'].append(i['node']['username'])

        has_next_page = True
        variables = '{"id":"' + str(id) +'","first":12}'
        result['followees'] = []
        while has_next_page:
            response = self.session.get(f'https://www.instagram.com/graphql/query/?query_hash=58712303d941c6855d4e888c5f0cd22f&variables={urllib.parse.quote(variables)}').json()
            has_next_page = response['data']['user']['edge_follow']['page_info']['has_next_page']
            end_cursor = response['data']['user']['edge_follow']['page_info']['end_cursor']
            variables = '{"id":"' + str(id) + '","first":12,"after":"'+end_cursor+'"}'
            for i in response['data']['user']['edge_follow']['edges']:
                result['followees'].append(i['node']['username'])

        return result

if __name__ == '__main__':
    print(inst_parser().get_page('dirsamp'))
