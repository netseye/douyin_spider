from douyin_spider.utils.common import parse_datetime, get_array_first
from douyin_spider.models.video import Video
from douyin_spider.models.music import Music
from douyin_spider.models.user import User, Star
from douyin_spider.models.address import Address


def get_video_url(video_list):
    """
    parse video url from video_list
    :param video_list:
    :return:
    """
    if video_list and isinstance(video_list, list):
        return video_list[0]
    return None


def get_music_url(music_list):
    """
    parse music url from music_list
    :param music_list:
    :return:
    """
    if music_list and isinstance(music_list, list):
        return music_list[-1]
    return None


def get_cover_url(video_json):
    """
    parse cover url from video_json
    :param video_json:
    :return:
    """
    return video_json.get('origin_cover') or video_json.get('cover')


def parse_gender(gender_codeName_str):
    """
    parse user gender
    :param gender_codeName_str:
    :return:
    """
    dict_gender_mapping = {'0': 'male', '1': 'female', '2': "unknown"}
    if isinstance(gender_codeName_str, str):
        return dict_gender_mapping[gender_codeName_str]


def download_video_test(url):
    """
    download test with headers
    :param url:
    :return:
    """
    import requests
    headers = {'User-Agent': 'Aweme 5.5.0 rv:55011 (iPhone; iOS 11.3.1; zh_CN) Cronet'}
    res = requests.get(url, headers=headers)
    with open('test.mp4', 'wb+') as f:
        f.write(res.content)


def parse_to_video(data):
    """
    parse json to Video
    :param data:
    :return: Video
    """
    id = data.get('aweme_id')

    statistics = data.get('statistics', {})
    like_count = statistics.get('digg_count')
    comment_count = statistics.get('comment_count')
    share_count = statistics.get('share_count')

    share_url = data.get('share_url')
    desc = data.get('desc')
    group_id = data.get('group_id')
    author_user_id = data.get('author_user_id')
    create_time = parse_datetime(data.get('create_time'))
    is_ads = data.get('is_ads')
    region = data.get('region')

    video = data.get('video', {})
    ratio = video.get('ratio')
    cover_url = get_array_first(get_cover_url(video).get('url_list', []))
    play_url = get_video_url(video.get('play_addr', {}).get('url_list', []))
    duration = data.get('duration')

    music = parse_to_music(data.get('music', {}))
    author = parse_to_user(data.get('author', {}))
    address = parse_to_address(data.get('poi_info', {}))

    if id:
        return Video(
            id=id,
            like_count=like_count,
            comment_count=comment_count,
            share_count=share_count,
            share_url=share_url,
            desc=desc,
            group_id=group_id,
            author_user_id=author_user_id,
            create_time=create_time,
            is_ads=is_ads,
            region=region,
            ratio=ratio,
            cover_url=cover_url,
            play_url=play_url,
            duration=duration,
            music=music,
            author=author,
            address=address
        )
    else:
        return None


def parse_to_user(author_json):
    """
    parse json to User
    :param author_json:
    :return: User
    """
    id = author_json.get('mid')
    avatar_url = get_array_first(author_json.get('avatar_larger', {}).get('url_list'))
    is_verified = author_json.get('is_verified')
    verify_info = author_json.get('custom_verify')
    is_hide_search = author_json.get('hide_search')
    nickname = author_json.get('nickname')
    region = author_json.get('CN')
    signature = author_json.get('signature')
    gender = parse_gender(author_json.get('gender'))
    birthday = parse_datetime(author_json.get('birthday'))
    alias = author_json.get('unique_id') or author_json.get('short_id')

    if id:
        return User(
            id=id,
            avatar_url=avatar_url,
            is_verified=is_verified,
            verify_info=verify_info,
            is_hide_search=is_hide_search,
            nickname=nickname,
            region=region,
            signature=signature,
            gender=gender,
            birthday=birthday,
            alias=alias
        )
    else:
        return None


def parse_to_star(star_json):
    """
    parse json to Star
    :param star_json:
    :return:Star
    """
    user_info = star_json.get('user_info', {})
    id = user_info.get('uid')
    nickname = user_info.get('nickname')
    signature = user_info.get('signature')
    avatar_url = get_array_first(user_info.get('avatar_larger', {}).get('url_list', []))
    factor_hot_value = star_json.get('factor_hot_value')
    hot_value = star_json.get('hot_value')
    if id:
        return Star(
            id=id,
            nickname=nickname,
            signature=signature,
            avatar_url=avatar_url,
            factor_hot_value=factor_hot_value,
            hot_value=hot_value
        )
    else:
        return None


def parse_to_music(music_json):
    """
    parse json to Music
    :param music_json:
    :return: Music
    """
    id = music_json.get('mid')
    title = music_json.get('title')
    play_url = get_music_url(music_json.get('play_url', {}).get('url_list', []))
    owner_name = music_json.get('owner_nickname')
    album = music_json.get('album')
    owner_id = music_json.get('owner_id')
    duration = music_json.get('duration')
    cover_url = get_array_first(music_json.get('cover_large', {}).get('url_list'))

    if id:
        return Music(
            id=id,
            title=title,
            play_url=play_url,
            owner_name=owner_name,
            album=album,
            owner_id=owner_id,
            duration=duration,
            cover_url=cover_url
        )
    else:
        return None


def parse_to_address(poi_info_json):
    """
    parse json to Address
    :param poi_info_json:
    :return: Address
    """
    if poi_info_json:
        id = poi_info_json.get('poi_id')
        longitude = poi_info_json.get('poi_longitude')
        latitude = poi_info_json.get('poi_latitude')
        name = poi_info_json.get('poi_name')

        address_info = poi_info_json.get('address_info', {})
        province = address_info.get('province') or None
        city = address_info.get('city') or None
        simple_addr = address_info.get('simple_addr') or None
        district = address_info.get('district') or None
        city_code = address_info.get('city_code') or None
        sub_address = address_info.get('address') or None

        if id:
            return Address(
                id=id,
                longitude=longitude,
                latitude=latitude,
                name=name,
                province=province,
                city=city,
                simple_addr=simple_addr,
                district=district,
                city_code=city_code,
                sub_address=sub_address
            )
        else:
            return None


if __name__ == '__main__':
    url = 'https://api.amemv.com/aweme/v1/play/?video_id=v0200f940000bis3ort1mik7192tss6g&line=1&ratio=540p&media_type=4&vr_type=0&improve_bitrate=0'
    download_video_test(url)
