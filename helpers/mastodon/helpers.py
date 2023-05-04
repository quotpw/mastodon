import re


def extract_link(response):
    data = {}
    for value in re.findall('<.*?\?(.*?)>; rel="(.*?)"', response.headers.get('link', '')):
        data[value[1]] = {}
        for kv in value[0].split('&'):
            kv = kv.split('=')
            data[value[1]][kv[0]] = kv[1]
    return data
