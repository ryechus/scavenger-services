import re

import requests
from instagram_sync.core import settings as ig_sync_settings

FIRST_POST_TIMESTAMP = 1563433200


def get_media_count(account_id, access_token):
    response = requests.get(
        f"{ig_sync_settings.GRAPH_API_URL}/{account_id}"
        f"?fields=media_count"
        f"&access_token={access_token}"
    )

    return response.json()["media_count"]


def get_media(account_id, access_token, since=FIRST_POST_TIMESTAMP):
    media_limit = get_media_count(account_id, access_token)
    response = requests.get(
        f"{ig_sync_settings.GRAPH_API_URL}/{account_id}/media"
        f"?access_token={access_token}"
        "&fields=media_url,children{media_url},caption,timestamp,permalink"
        f"&limit={media_limit}"
        f"&since={since}"
    )

    return response.json()


def parse_caption(caption):
    title_regex = re.compile(r"^([^@#]+)?(\s{0,1}[@#].*)")
    tags_re = re.compile(r"(#)([\w.-]+)")
    artist_re = re.compile(r"(@)([\w.-]+)")
    artists = []
    tags = []

    post_title = "Default Title"

    # for m in media[35:100]:
    # caption = m["caption"]
    artist_iter = artist_re.finditer(caption)
    tag_iter = tags_re.finditer(caption)
    match_str = title_regex.match(caption)

    if match_str:
        post_title = match_str.groups()[0] or post_title

    for artist in artist_iter:
        artists.append(artist.groups()[1])

    for tag in tag_iter:
        tags.append(tag.groups()[1])

    return {"title": post_title.replace("\n", ""), "tags": tags, "artists": artists}
