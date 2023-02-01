from run import app, db, News

with app.app_context():
    db.create_all()
    
    # import feedparser
    # import newspaper

    # GOOGLE_RSS_URL="https://news.google.com/rss/"
    # NewsFeed = feedparser.parse(GOOGLE_RSS_URL)

    # # NewsFeed = feedparser.parse(GOOGLE_RSS_KEYWORD_LOCALIZATION.replace("<KEYWORD>",keyword))

    # for newsItem in NewsFeed.entries:
    #     article=newspaper.Article(url=newsItem["link"])
    #     article.download()
    #     article.parse()
    #     # print(article.title+"\n"+article.text+"\n"+str(article.publish_date)+"\n"+"\n -----Nuovo Articolo------ \n")

    #     the_news=News(args={"titolo":article.title,"autori":article.authors,"testata_giornalistica":newsItem.source["title"],"data_di_pubblicazione":article.publish_date,"link":newsItem["link"],"testo":article.text})     
    #     db.session.add(the_news)

    # db.session.commit()
