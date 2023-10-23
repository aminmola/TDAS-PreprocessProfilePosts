import utils.config as cfg
from unidecode import unidecode
import re
import requests
import jellyfish as jf
from thefuzz import fuzz
from thefuzz import process


def caption_similarity(new_post,exist_post):
    result = jf.levenshtein_distance(new_post["caption"],exist_post["caption"])
    if result >1:
        return False
    else:
        return True


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


class Taggers:
    def __init__(self,post:dict):
        self.post = post
        self.post["cleaned_caption"] = cleaning(post["caption"])

    def sale(self):
        url = f"http://{cfg.BASE_SERVER_HOST}:10010/sale_manual_set"
        params = {"caption": f"{self.post['cleaned_caption']}", 'id': 9}
        vec = requests.request("POST", url, params=params)
        information = vec.json()['data'][0]
        self.post["IsSale"] = information[0]


    def price(self):
        url = f"http://{cfg.BASE_SERVER_HOST}:10009/price_manual_set"
        params = {"caption": f"{self.post['cleaned_caption']}"}
        vec = requests.request("POST", url, params=params)
        information = vec.json()['data'][0]
        self.post["Price"] = information["Price"]
        self.post["PriceUnit"] = information["PriceUnit"]
        self.post["OriginalPrice"] = information["OriginalPrice"]
            
    def shipping(self):
        url = f"http://{cfg.BASE_SERVER_HOST}:10011/shipping_manual_set"
        params = {"caption": f"{self.post['cleaned_caption']}"}
        vec = requests.request("POST", url, params=params)
        information = vec.json()['data'][0]
        self.post["BuyInPerson"] = information["BuyInPerson"]
        self.post["ShippingPrice"] = information["ShippingPrice"]
        self.post["ShippingLoc"] = information["ShippingLoc"]
        self.post["ShippingOption"] = information["ShippingOption"]
        self.post["ReturnOption"] = information["ReturnOption"] 

    def category(self):
        url = f"http://{cfg.BASE_SERVER_HOST}:10004/category_manual_set"
        params = {"caption": f"{self.post['cleaned_caption']}"}
        vec = requests.request("POST", url, params=params)
        information = vec.json()['data'][0]
        self.post["CategoryId"] = information["CategoryId"]
        self.post["GenderDetection"] = information["GenderDetection"] 

    def material(self):
        url = f"http://{cfg.BASE_SERVER_HOST}:10007/material_manual_set"
        params = {"caption": f"{self.post['cleaned_caption']}"}
        vec = requests.request("POST", url, params=params)
        information = vec.json()['data'][0]
        self.post["MaterialId"] = information["MaterialId"]

    def brand(self):
        url = f"http://{cfg.BASE_SERVER_HOST}:10003/brand_manual_set"
        params = {"caption": f"{self.post['cleaned_caption']}"}
        vec = requests.request("POST", url, params=params)
        information = vec.json()['data'][0]
        self.post["BrandId"] = information["BrandId"]

    def size(self):
        url = f"http://{cfg.BASE_SERVER_HOST}:10012/size_manual_set"
        params = {"caption": f"{self.post['cleaned_caption']}"}
        vec = requests.request("POST", url, params=params)
        information = vec.json()['data'][0]
        self.post["SizeId"] = information["SizeId"]

    def attribute(self):
        url = f"http://{cfg.BASE_SERVER_HOST}:10002/attribute_manual_set"
        params = {"caption": f"{self.post['cleaned_caption']}"}
        vec = requests.request("POST", url, params=params)
        information = vec.json()['data'][0]
        self.post["Attributes"] = information["Attributes"]

    def color(self):
        url = f"http://{cfg.BASE_SERVER_HOST}:10005/color_manual_set"
        params = {"caption": f"{self.post['cleaned_caption']}"}
        vec = requests.request("POST", url, params=params)
        information = vec.json()['data'][0]
        self.post["ColorId"] = information["ColorId"]