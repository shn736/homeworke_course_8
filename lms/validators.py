import re

from rest_framework.serializers import ValidationError


class UrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)

        if tmp_val is None or tmp_val == "":
            return

        reg = re.compile(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$")
        if not bool(reg.match(tmp_val)):
            raise ValidationError("Ссылка должна быть на youtube.com или youtu.be")
