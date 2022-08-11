import requests
from instagram_sync.core import settings


def get_user_access_token(app_id, code_parameter, redirect_uri):
    app_secret = "c2dde7a3599fb3eba47574d135c9963a"
    url = (
        f"{settings.GRAPH_API_URL}/oauth/access_token?client_id={app_id}"
        f"&redirect_uri={redirect_uri}"
        f"&client_secret={app_secret}"
        f"&code={code_parameter}"
    )
    response = requests.get(url)

    return response.json()


def inspect_user_access_token(token):
    ...


def delete_user_access_token(token):
    ...
