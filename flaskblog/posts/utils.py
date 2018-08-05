from slugify import slugify

def slugurl(text, delim=u'-'):
    """Generates Slug for URL."""
    return slugify(text)

