#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import feedparser
import slugify
import re

rss_url = "https://mixxxblog.blogspot.com/feeds/posts/default"

feed = feedparser.parse(rss_url)
items = feed["items"]
for item in items:
    time = item["published_parsed"]
    title = item["title"]
    author = item["author_detail"]["name"]
    date = '{:04d}-{:02d}-{:02d}'.format(time.tm_year, time.tm_mon, time.tm_mday)
    filename = '{}-{}.html'.format(date, slugify.slugify(title))
    value = item["content"][0]["value"]
    value = re.sub(r'(\</[^>]*>)', '\g<1>\n', value)
    value = re.sub(r'(\<[^>]*/>)', '\g<1>\n', value)
    if re.match(r'<h\d>.*</h\d>.*', value.splitlines()[0]):
        value = ''.join(value.splitlines()[1:])
    if re.match(r'<br(\s+[^>]*)>', value.splitlines()[0].strip()):
        value = ''.join(value.splitlines()[1:])
    with open(filename, "w") as f:
        f.write((
            "title: {title}\n"
            "author: {author}\n"
            "date: {date}\n"
            "\n"
            "{{% extends \"post.html\" %}}\n"
            "\n"
            "{{% block post %}}\n"
            "\n"
            "{content}\n"
            "\n"
            "{{% endblock %}}\n").format(
                title=title,
                date=date,
                author=author,
                content=value,
            ))
