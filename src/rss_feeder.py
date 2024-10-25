url = "https://www.federalreserve.gov/feeds/speeches.xml"
import feedparser
#import newspaper
#from flask import render_template

# def get_metadata(article: newspaper.article.Article) -> dict:
#     if not article.is_parsed:
#         raise TypeError("Article must be parsed.")
#
#     title = article.title
#     image = article.top_img
#     url = article.url
#     try:
#         description = article.meta_data['description']
#     except KeyError:
#         description = ""
#
#     return {"title": title, "description": description, "image": image, "url": url}
#
#

feed = feedparser.parse(url)
from linkpreview import link_preview

for entry in feed.entries:
    print(entry.title)
    print(entry.link)
    preview = link_preview(entry.link, parser="lxml")
    print("title:", preview.title)
    print("description:", preview.description)
    print("image:", preview.image)
    print("force_title:", preview.force_title)
    print("absolute_image:", preview.absolute_image)
    print("site_name:", preview.site_name)
    print("favicon:", preview.favicon)
    print("absolute_favicon:", preview.absolute_favicon)
    print(entry.description)
