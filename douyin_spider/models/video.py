from douyin_spider.models.JsonMixIn import ToJsonMixIn


class Video(ToJsonMixIn):
    """
    Video model

    Main public parameters:
    - id: video id,unique
    - play_url: video url
    - music: music of the video use
    - address: address of the video
    - ...
    - author: author of the video
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.like_count = kwargs.get('like_count')
        self.comment_count = kwargs.get('comment_count')
        self.share_count = kwargs.get('share_count')
        self.share_url = kwargs.get('share_url')
        self.desc = kwargs.get('desc')
        self.group_id = kwargs.get('group_id')
        self.author_user_id = kwargs.get('author_user_id')
        self.create_time = kwargs.get('create_time')
        self.is_ads = kwargs.get('is_ads')
        self.region = kwargs.get('region')
        self.ratio = kwargs.get('ratio')
        self.cover_url = kwargs.get('cover_url')
        self.play_url = kwargs.get('play_url')
        self.duration = kwargs.get('duration')
        self.music = kwargs.get('music')
        self.author = kwargs.get('author')
        self.address = kwargs.get('address')

    def __repr__(self):
        return "<Video<%s,%s>>" % (self.id, self.desc[:50].strip() if self.desc else None)


if __name__ == '__main__':
    video=Video(id="123134")
    print(video)
