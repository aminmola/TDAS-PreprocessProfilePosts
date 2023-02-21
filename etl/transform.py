import re
from datetime import datetime
from unidecode import unidecode
import utils.helper as hlp
from utils.mongo import Mongo
import pytz


class AccountModel(Mongo):
    _connection_name = 'mongo_connection1'
    _collection_name = 'accounts'
    _db_name = 'data_pipline'


def cleaning(caption: str):
    """Cleaning raw caption
    :Parameters
    ------------------
    Raw caption of the post

    :returns
    ------------------
    caption
    1 - with no persian number : DONE
    2 - whole space instead of half space : DONE
    3 - with Homogenization of char 'ک' : ...
    4 - with Homogenization of char "ی" : DONE
    5 - eradicate the hashtag in the middle of caption : ...
    6 - ...
    """
    if not caption:
        return ""
    # Emoji Remover
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    caption = emoji_pattern.sub(r' ', caption)

    ### 1 - with no persian number###
    caption = re.split('', caption)
    for i in range(len(caption)):
        if unidecode(caption[i]).isnumeric():
            caption[i] = unidecode(caption[i])
    caption = ''.join(caption)
    ##############################

    ### 2 - some extra stafs###
    caption = caption.replace('\u200c', " ")  # halfspace to space
    caption = caption.replace('ي', "ی")
    caption = re.sub(r' +', ' ', caption)  # remove extra spaces
    caption = re.sub(r'[ـ\r]', '', caption)  # remove keshide, carriage returns
    caption = re.sub(r'\n\n+', '\n\n', caption)  # remove extra newlines
    caption = re.sub(r'[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652]', '',
                     caption)  # remove FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA, SHADDA, SUKUN
    caption = caption.replace('ك', "ک")
    caption = caption.replace('أ', 'ا')

    return caption


def remove_hashtags(caption: str):
    return re.sub('#(_*[a-zآ-ی0-9]*_*)+', '', cleaning(caption))


def run(data: dict):
    account_model = AccountModel()
    posts = []
    k = 0
    for post in data["latestPosts"]:
        if k == 0:
            pre_account = account_model.find_one({"accountProviderId": int(post["ownerId"])})
            if not pre_account:
                account = {
                    'accountProviderId': int(post["ownerId"]),
                    'userName': post['ownerUsername'],
                    'lastTakenAtDate': datetime.strptime(post["timestamp"], '%Y-%m-%dT%H:%M:%S.0000000'),
                    'lastPostCreated': datetime.now(pytz.timezone("IRAN")),
                    'fullName': data['fullName'],
                    'profileImage': data['profilePicUrl'],
                    'PostCodes': []
                }
            else:
                account = pre_account
                account['lastTakenAtDate'] = datetime.strptime(post["timestamp"], '%Y-%m-%dT%H:%M:%S.0000000')
                account['lastPostCreated'] = datetime.now(pytz.timezone("IRAN"))
                account['profileImage'] = data["profilePicUrl"]
            k += 1
        account['PostCodes'].append(post["shortCode"])
        post_rec = {
            'source': "profile",
            'accountProviderId': int(post["ownerId"]),
            'code': post["shortCode"],
            'caption': post["caption"],
            'cleaned_caption': cleaning(post["caption"]),
            'like_count': post["likesCount"],
            'userName': post['ownerUsername'],
            'providerId': int(post["id"]),
            'nohash_caption': remove_hashtags(post["caption"]),
            'takenAtDate': datetime.strptime(post["timestamp"], '%Y-%m-%dT%H:%M:%S.0000000'),
            'local_created_at': datetime.strptime(str(str(datetime.now(pytz.timezone("IRAN"))).split("+")[0].split(".")[0] + ".0000000").replace(" ","T"),'%Y-%m-%dT%H:%M:%S.0000000'),
            'created_at': datetime.now(pytz.timezone("UTC")),
            'fullName': data['fullName'],
            'profileImage': data['profilePicUrl']
        }
        # if post["timestamp"][-1] == "Z":
        #     post_rec['takenAtDate'] = datetime.strptime(post["timestamp"], '%Y-%m-%dT%H:%M:%S.000Z')
        # elif post["timestamp"][-1] == "0":
        #     post_rec['takenAtDate'] = datetime.strptime(post["timestamp"], '%Y-%m-%dT%H:%M:%S.0000000')
        # else:
        #     post_rec['takenAtDate'] = datetime.strptime(post["timestamp"].split("+")[0], '%Y-%m-%dT%H:%M:%S')

        if 'locationName' in list(post.keys()):
            post_rec['loc'] = post["locationName"]

        # 'profileImage': desc['owner']['profile_pic_url'],
        # 'fullName': desc['owner']['full_name'],
        # if 'edge_media_preview_comment' in list(desc["shortcode_media"].keys()):
        #     post_rec['comment_count']: int(desc["shortcode_media"]["edge_media_to_parent_comment"]["count"])

        post_images = []
        if post["type"] == "Image":
            post_images.append({
                'url': post["displayUrl"].replace("amp;", ""),
                'width': post["dimensionsWidth"],
                'height': post["dimensionsHeight"]
            })
            post_rec['images'] = post_images
        for media in post["childPosts"]:
            if media["type"] == "Image":
                post_images.append({
                    'url': media["displayUrl"].replace("amp;", ""),
                    'width': media["dimensionsWidth"],
                    'height': media["dimensionsHeight"]
                })
        if post_images:
            post_rec['images'] = post_images
        # if desc['media_type'] == 1:
        #     url_list = desc['image_versions2']['candidates']
        #     post_images.append(sorted(url_list, key=lambda d: d['width'])[int(len(url_list) / 2)])
        #     post_rec['images'] = post_images
        if post_images:
            posts.append(post_rec)
    account['PostCodes'] = list(set(account['PostCodes']))
    return posts, account


def run_online(data: dict):
    posts = []
    for post in data["latestPosts"]:
        post_rec = {
            'caption': post["caption"],
            'cleaned_caption': cleaning(post["caption"])
        }
        posts.append(post_rec)
    return posts


def run1(data: dict):
    desc = data['graphql']["shortcode_media"]
    post_rec = {
        'source': "profile",
        'accountProviderId': desc['owner']["id"],
        'userName': desc['owner']["username"],
        'profileImage': desc['owner']['profile_pic_url'],
        'fullName': desc['owner']['full_name'],
        'providerId': desc["id"],
        'code': desc["shortcode"],
        'caption': desc["edge_media_to_caption"]["edges"][0]["node"]["text"],
        'cleaned_caption': cleaning(desc["edge_media_to_caption"]["edges"][0]["node"]["text"]),
        'takenAtDate': datetime.fromtimestamp(desc["taken_at_timestamp"]),
        'created_at': hlp.datetime_formatter(datetime.now()),
        'like_count': desc["edge_media_preview_like"]["count"],
        # 'updated_at': hlp.datetime_formatter(datetime.now()),
        'nohash_caption': remove_hashtags(desc["edge_media_to_caption"]["edges"][0]["node"]["text"])
    }
    # if 'edge_media_preview_comment' in list(desc["shortcode_media"].keys()):
    #     post_rec['comment_count']: int(desc["shortcode_media"]["edge_media_to_parent_comment"]["count"])
    if 'location' in list(desc.keys()) and desc["location"]:
        if "address_json" in list(desc["location"].keys()):
            post_rec['address_json'] = desc['location']["address_json"]
        if "slug" in list(desc["location"].keys()):
            post_rec['slug'] = desc['location']["slug"]
        if "locname" in list(desc["location"].keys()):
            post_rec['locname'] = desc['location']["name"]
    post_images = []
    if desc["__typename"] == "GraphImage":
        # it's just a singular Image
        media = desc["display_resources"][int(len(desc["display_resources"]) / 2)]
        media['url'] = media.pop("src")
        media['width'] = media.pop("config_width")
        media['height'] = media.pop("config_height")
        post_images.append(media)
        if post_images:
            post_rec['images'] = post_images
        # if desc['media_type'] == 1:
        #     url_list = desc['image_versions2']['candidates']
        #     post_images.append(sorted(url_list, key=lambda d: d['width'])[int(len(url_list) / 2)])
        #     post_rec['images'] = post_images
        post_rec['profile_image_busy'] = False
        post_rec['post_image_busy'] = False
        post_rec['filtering_image_busy'] = False
        return post_rec

    if desc["__typename"] == "GraphSidecar":
        # it's just a singular Image
        images = desc["edge_sidecar_to_children"]["edges"]
        for image in images:
            if image["node"]["__typename"] == "GraphImage":
                media = image["node"]["display_resources"][int(len(image["node"]["display_resources"]) / 2)]
                media['url'] = media.pop("src")
                media['width'] = media.pop("config_width")
                media['height'] = media.pop("config_height")
                post_images.append(media)
        if post_images:
            post_rec['images'] = post_images
        # if desc['media_type'] == 1:
        #     url_list = desc['image_versions2']['candidates']
        #     post_images.append(sorted(url_list, key=lambda d: d['width'])[int(len(url_list) / 2)])
        #     post_rec['images'] = post_images
        post_rec['profile_image_busy'] = False
        post_rec['post_image_busy'] = False
        post_rec['filtering_image_busy'] = False
        return post_rec
