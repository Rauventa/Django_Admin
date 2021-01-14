from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from authtoken.utils import get_random_token


class Token(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_tokens',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    type = models.CharField(max_length=30, blank=True, db_index=True)
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = 'токен'
        verbose_name_plural = 'REST-Токены'

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = get_random_token()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.key
