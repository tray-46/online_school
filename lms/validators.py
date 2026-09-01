import re

from rest_framework import serializers


class YouTubeLinkValidator:

    def __init__(self):
        self.regex = re.compile(
            r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu\.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]{11})((?:\?|\&)\S+)?$")

    def __call__(self, value):
        if not self.regex.match(value):
            raise serializers.ValidationError("Only youtube links are allowed.")
