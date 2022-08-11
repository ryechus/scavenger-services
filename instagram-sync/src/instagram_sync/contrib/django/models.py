from django.db import models
from encrypted_model_fields.fields import EncryptedCharField


class InstagramAccount(models.Model):
    account_id = models.PositiveBigIntegerField(primary_key=True)
    access_token = EncryptedCharField(max_length=512)
    authorized_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "instagram_account"
        verbose_name_plural = "Instagram Accounts"
