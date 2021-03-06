from douyin_spider.models.JsonMixIn import ToJsonMixIn
from douyin_spider.utils.decryption.signture import generate_signature
from douyin_spider.utils.common import get_user_dytk_by_id
from douyin_spider.utils.get import get
from douyin_spider.config import share_user_base_url, HEADERS


class BasicUser(object):
    """
    User super class
    """

    def __init__(self, **kwargs):
        self.id = None
        self.nickname = None

    def videos(self, max=None):
        """
        videos belongs to challenge
        :param max:videos number need
        :return:videos generator
        """
        print(f"<{type(self).__name__}<{self.nickname},{self.id}>>")
        if not isinstance(max, int):
            raise RuntimeError("`max` param must be int")
        if max <= 0:
            raise RuntimeError("`max` param must >=1")
        from douyin_spider.utils.parse import parse_to_video

        user_video_params = {
            'user_id': str(self.id),
            'count': '21',
            'max_cursor': '0',
            'aid': '1128',
            '_signature': generate_signature(str(self.id)),
            'dytk': get_user_dytk_by_id(str(self.id)),
        }
        count, cursor = 0, None
        while True:
            if cursor:
                user_video_params['max_cursor'] = str(cursor)
            result = get(share_user_base_url, params=user_video_params, headers=HEADERS)
            aweme_list = result.get('aweme_list', [])
            for item in aweme_list:
                count += 1
                video = parse_to_video(item)
                yield video
                if max and count >= max:
                    return

            if result.get('has_more'):
                cursor = result.get('max_cursor')
            else:
                break
        if count == 0:
            print(f"There is no video in the user {self.id}")
        print(f"video count:{count}")


class User(BasicUser, ToJsonMixIn):
    """
    User model

    Main public parameters:
    - id: user id
    - nickname: user's nickname
    - ...
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.id = kwargs.get('id')
        self.avatar_url = kwargs.get('avatar_url')
        self.is_verified = kwargs.get('is_verified')
        self.verify_info = kwargs.get('verify_info')
        self.is_hide_search = kwargs.get('is_hide_search')
        self.nickname = kwargs.get('nickname')
        self.region = kwargs.get('region')
        self.signature = kwargs.get('signature')
        self.gender = kwargs.get('gender')
        self.alias = kwargs.get('alias')

    def __repr__(self):
        return "<User<%s,%s>>" % (self.alias, self.nickname)


class Star(BasicUser, ToJsonMixIn):
    """
    Star model

    Main public parameters:
    - id: user id
    - nickname: star's nickname
    - hot_value: star's hot_value of searching
    - ...
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.id = kwargs.get('id')
        self.nickname = kwargs.get('nickname')
        self.signature = kwargs.get('signature')
        self.avatar_url = kwargs.get('avatar_url')
        self.factor_hot_value = kwargs.get('factor_hot_value')
        self.hot_value = kwargs.get('hot_value')

    def __repr__(self):
        return "<Star<%s,%s>>" % (self.nickname, self.id)


if __name__ == '__main__':
    user = User(alias="xx", nickname="www")
    print(user)

    star = Star(id='1231', nickname='jerry')
    star.videos()
