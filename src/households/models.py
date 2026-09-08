import secrets
import string

from django.conf import settings
from django.db import IntegrityError, models, transaction


INVITE_CODE_ALPHABET = string.ascii_uppercase + string.digits
INVITE_CODE_LENGTH = 8


def generate_invite_code() -> str:
    return "".join(
        secrets.choice(INVITE_CODE_ALPHABET) for _ in range(INVITE_CODE_LENGTH)
    )


class Household(models.Model):
    name = models.CharField(max_length=120)
    invite_code = models.CharField(max_length=16, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if self.invite_code:
            super().save(*args, **kwargs)
            return
        for _ in range(16):
            self.invite_code = generate_invite_code()
            try:
                with transaction.atomic():
                    super().save(*args, **kwargs)
                return
            except IntegrityError:
                self.invite_code = ""
        raise IntegrityError("Could not generate a unique invite code")

    def __str__(self) -> str:
        return self.name


class Membership(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="membership",
    )
    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    def __str__(self) -> str:
        return f"{self.user} in {self.household}"


def household_for(user):
    try:
        return user.membership.household
    except Membership.DoesNotExist:
        return None
