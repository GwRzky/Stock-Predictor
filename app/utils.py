from markupsafe import Markup
import re

def nl2br(value):
    """Convert newlines to <br> tags"""
    if not value:
        return ""
    return Markup(re.sub(r'\n', '<br>', value))