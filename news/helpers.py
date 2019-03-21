def generate_mazemap_embed(location_url):
    if location_url is None or not location_url.startswith('https://use.mazemap.com/#'):
        return None  # invalid link
    url_path = location_url[location_url.index('#'):]
    return 'https://use.mazemap.com/embed.html' + url_path
