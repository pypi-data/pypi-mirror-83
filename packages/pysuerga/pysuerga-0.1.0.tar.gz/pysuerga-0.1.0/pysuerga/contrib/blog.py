import datetime
import time
import operator
import feedparser


def main(context):
    """
    Given the blog feed defined in the configuration yaml, this context
    preprocessor fetches the posts in the feeds, and returns the relevant
    information for them (sorted from newest to oldest).
    """
    posts = []
    for feed_url in context["blog"]["feed"]:
        feed_data = feedparser.parse(feed_url)
        for entry in feed_data.entries:
            published = datetime.datetime.fromtimestamp(
                time.mktime(entry.published_parsed)
            )
            posts.append(
                {
                    "title": entry.title,
                    "author": entry.author,
                    "published": published,
                    "feed": feed_data["feed"]["title"],
                    "link": entry.link,
                    "description": entry.description,
                    "summary": entry.summary,
                }
            )
    posts.sort(key=operator.itemgetter("published"), reverse=True)
    context["blog"]["posts"] = posts[: context["blog"]["num_posts"]]
    return context
