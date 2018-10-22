

def generate_mazemap_embed(mazemap_url):
    if mazemap_url is None or not mazemap_url.startswith('https://use.mazemap.com/#'):
        return ''  # invalid link
    url_path = mazemap_url[mazemap_url.index('#'):]
    return 'https://use.mazemap.com/embed.html' + url_path
