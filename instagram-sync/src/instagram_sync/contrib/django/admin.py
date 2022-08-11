from urllib.parse import parse_qs, urlparse

from django.contrib import admin
from django.http import QueryDict
from django.shortcuts import redirect
from django.urls import reverse
from instagram_sync.core import settings
from instagram_sync.core.graph_api.auth import get_user_access_token

from ...core.graph_api.pages import get_page_instagram_accounts, get_user_pages
from .models import InstagramAccount

IG_ID_FIELD_NAME = "account_id"


@admin.register(InstagramAccount)
class InstagramAccountAdmin(admin.ModelAdmin):
    fields = (IG_ID_FIELD_NAME, "access_token")
    add_form_template = "instagram_sync/add_form.html"

    def add_view(self, request, form_url="", extra_context=None):
        query_string = parse_qs(urlparse(request.get_full_path()).query)
        app_id = 418459443679300
        add_view_url = reverse("admin:instagram_sync_instagramaccount_add")
        redirect_uri = f"http://localhost:8000{add_view_url}"

        if "code" in query_string and request.method == "GET":
            user_access_token = get_user_access_token(
                app_id, query_string["code"][0], redirect_uri
            )
            user_access_token = user_access_token["access_token"]
            user_pages = get_user_pages(user_access_token)
            page_id = user_pages["data"][0]["id"]
            instagram_accounts = get_page_instagram_accounts(page_id, user_access_token)
            instagram_account_id = instagram_accounts["instagram_business_account"][
                "id"
            ]

            request.GET = QueryDict(
                f"access_token={user_access_token}&{IG_ID_FIELD_NAME}={instagram_account_id}"
            )

            return super().add_view(
                request, form_url=add_view_url, extra_context=extra_context
            )
        elif request.method == "POST":
            return super().add_view(
                request, form_url=form_url, extra_context=extra_context
            )
        elif "error" in query_string:
            #  need to send a message to the admin that things didn't work
            return redirect(reverse("admin:index"))

        return redirect(
            f"{settings.FACEBOOK_LOGIN_URL}/dialog/oauth?client_id={app_id}"
            f"&redirect_uri={redirect_uri}&scope=instagram_basic,pages_show_list"
        )
