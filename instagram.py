#Для поиска информации в СУБД используются account_name=username, tag='follower' (для подписчиков) и
#tag='subscription' (для подписок)

import scrapy
from scrapy.http import HtmlResponse
from SocialNetworkParser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'vasia_krutov'
    insta_pass = '#PWD_INSTAGRAM_BROWSER:10:1603088237:Ad1QAKtDvhV05Lb1MM1UCKk2D0zmydSyHMGcCMj0WoTk29AUIp35rQKhL/G8YbbEOLGF/e7Z20yTNWdd4qW5Je1qBD5QgwzFlfMoFFOPeEen6JpRleNEP1GT+dE+keOM3d4oNH1v+6KDyjp71DgapqqcGQ=='
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = ['aviationdaily', 'aviationanatomy']
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    hash_followers = 'c76146de99bb02f6415203be841dd25a' #hash для получения данных подписчиках
    hash_sub = 'd04b0a864b4b54837c0d870b0e77e076' #hash для получения данных подписках

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pass},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for el in self.parse_user:
                yield response.follow(
                    f'/{el}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': el}
            )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {
            'id': user_id,
            'first': 24
        }
        url_followers = f'{self.graphql_url}query_hash={self.hash_followers}&{urlencode(variables)}'
        yield response.follow(
            url_followers,
            callback=self.user_followers_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )
        url_subscription = f'{self.graphql_url}query_hash={self.hash_sub}&{urlencode(variables)}'
        yield response.follow(
            url_subscription,
            callback=self.user_subscription_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

    def user_followers_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_data = j_data['data']['user']['edge_follow']['page_info']  #<-- здесь периодически вылетает, пишет KeyError: 'edge_follow'. В методе user_subscription_parse такая же строка полностью работает
        if page_data['has_next_page']:
            variables['after'] = page_data['end_cursor']
            url_followers = f'{self.graphql_url}query_hash={self.hash_followers}&{urlencode(variables)}'
            yield response.follow(
                url_followers,
                callback=self.user_followers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        followers = j_data.get('data').get('user').get('edge_follow').get('edges')
        for follower in followers:
            item = InstaparserItem(
                account_name=username,
                tag='follower',
                user_id=follower['node']['id'],
                follower_user_name=follower['node']['username'],
                follower_id=follower['node']['full_name'],
                photo=follower['node']['profile_pic_url']

            )
        yield item

    def user_subscription_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_data = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_data['has_next_page']:
            variables['after'] = page_data['end_cursor']
            url_subscription = f'{self.graphql_url}query_hash={self.hash_sub}&{urlencode(variables)}'
            yield response.follow(
                url_subscription,
                callback=self.user_followers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        subscription = j_data.get('data').get('user').get('edge_follow').get('edges')
        for sub in subscription:
            item = InstaparserItem(
                account_name=username,
                tag='subscription',
                user_id=sub['node']['id'],
                sub_user_name=sub['node']['username'],
                sub_id=sub['node']['full_name'],
                photo=sub['node']['profile_pic_url']
            )
        yield item



    #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    #Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

