import requests
from instagram_sync.core import settings


def get_user_pages(access_token):
    url = f"{settings.GRAPH_API_URL}/me/accounts?access_token={access_token}"

    response = requests.get(url)

    return response.json()


def get_page_instagram_accounts(page_id, access_token):
    url = f"{settings.GRAPH_API_URL}/{page_id}?fields=instagram_business_account&access_token={access_token}"

    response = requests.get(url)

    return response.json()
