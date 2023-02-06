import feedparser
import newspaper
import pandas as pd

GOOGLE_RSS_URL="https://news.google.com/rss/"
GOOGLE_RSS_TOPIC_URL="https://news.google.com/rss/topics/<TOPIC_ID>"
GOOGLE_RSS_KEYWORD="https://news.google.com/rss/search?q=<KEYWORD>"
GOOGLE_RSS_COUNTRY_LANGUAGE="https://news.google.com/rss?hl=<LANGUAGE_CODE>&gl=<COUNTRY_CODE>&ceid=<COUNTRY_CODE>:<LANGUAGE_CODE>"
GOOGLE_RSS_KEYWORD_LOCALIZATION="https://news.google.com/rss/search?q=<KEYWORD>&hl=<LANGUAGE_CODE>&gl=<COUNTRY_CODE>&ceid=<COUNTRY_CODE>:<LANGUAGE_CODE>"
GOOGLE_RSS_DATERANGE=GOOGLE_RSS_KEYWORD+"+after:<AFTER_DATE>+before:<BEFORE_DATE>" # 2022-06-10
GOOGLE_RSS_DATERANGE_LOCALIZATION=GOOGLE_RSS_DATERANGE+"&hl=<LANGUAGE_CODE>&gl=<COUNTRY_CODE>&ceid=<COUNTRY_CODE>:<LANGUAGE_CODE>"
keyword="smact"
NewsFeed = feedparser.parse(GOOGLE_RSS_DATERANGE_LOCALIZATION.replace(
    "<LANGUAGE_CODE>","It").replace(
        "<COUNTRY_CODE>","It").replace(
            "<KEYWORD>",keyword).replace(
                "<BEFORE_DATE>","2022-12-22").replace(
                    "<AFTER_DATE>","2022-01-01"))

# NewsFeed = feedparser.parse(GOOGLE_RSS_KEYWORD_LOCALIZATION.replace("<KEYWORD>",keyword))

list_articles=[]

for newsItem in NewsFeed.entries:
    article=newspaper.Article(url=newsItem["link"])
    article.download()
    article.parse()
    # print(article.title+"\n"+article.text+"\n"+str(article.publish_date)+"\n"+"\n -----Nuovo Articolo------ \n")

    list_articles.append({"titolo":article.title,"autori":article.authors,"testata giornalistica":newsItem.source["title"],"data di pubblicazione":article.publish_date,"link":newsItem["link"],"testo":article.text})     

df=pd.DataFrame(list_articles)
print(df)