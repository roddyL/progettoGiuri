import json
import requests
import re
import nltk
import wordcloud

API_KEY = "4b362c42052d41a7a8541e6f350b1004"

def news_get(keyword):
    url = f"https://newsapi.org/v2/everything?language=it&q={keyword}&apiKey={API_KEY}"
    response = requests.get(url)
    response =json.loads(response.text)["articles"]
    testo_completo= ""
    
    for article in response:
        testo_completo+=article["content"]
        testo_completo+=article["title"]

    testo_completo = re.sub("\[([^\]]+)\]"," ",testo_completo)
    text = nltk.word_tokenize(testo_completo, language="italian")
    result = nltk.pos_tag(text)

    new_text = ' '.join([word for word, tag in result if tag[0] in "NJV"])

    stopwords = set(wordcloud.STOPWORDS)
    stopwords.update([keyword,'ad', 'al', 'https','allo', 'ai','furono', 'fossi', 'fosse', 'fossimo', 'fossero', 'essendo', 'faccio', 'fai', 'facciamo',
    'fanno', 'faccia', 'facciate', 'facciano', 'farò', 'farai', 'farà', 'faremo', 'farete', 'faranno', 'farei', 'faresti', 'farebbe',
    'faremmo', 'fareste', 'farebbero', 'facevo', 'facevi', 'faceva', 'facevamo', 'facevate', 'facevano', 'feci', 'facesti', 'fece',
    'facemmo', 'faceste', 'fecero', 'facessi', 'facesse', 'facessimo', 'facessero', 'facendo', 'sto', 'stai', 'sta', 'stiamo',
    'stanno', 'stia', 'stiate', 'stiano', 'starò', 'starai', 'starà', 'staremo', 'starete', 'staranno', 'starei', 'staresti',
    'starebbe', 'staremmo', 'stareste', 'starebbero', 'stavo', 'stavi', 'stava', 'stavamo', 'stavate', 'stavano', 'stetti',
    'stesti', 'stette', 'stemmo', 'steste', 'stettero', 'stessi', 'stesse', 'stessimo', 'stessero', 'stando' 'agli', 'all',
    'agl', 'alla', 'alle', 'con', 'col', 'coi', 'da', 'dal', 'dallo', 'dai', 'dagli', 'dall', 'dagl', 'dalla', 'dalle',
    'di', 'del', 'dello', 'dei', 'degli', 'dell', 'degl', 'della', 'delle', 'in', 'nel', 'nello', 'nei', 'negli', 'nell',
    'negl', 'nella', 'nelle', 'su', 'sul', 'sullo', 'sui', 'sugli', 'sull', 'sugl', 'sulla', 'sulle', 'per', 'tra', 'contro',
    'io', 'tu', 'lui', 'lei', 'noi', 'voi', 'loro', 'mio', 'mia', 'miei', 'mie', 'tuo', 'tua', 'tuoi', 'tue', 'suo', 'sua',
    'suoi', 'sue', 'nostro', 'nostra', 'nostri', 'nostre', 'vostro', 'vostra', 'vostri', 'vostre', 'mi', 'ti', 'ci', 'vi',
    'lo', 'la', 'li', 'le', 'gli', 'ne', 'il', 'un', 'uno', 'una', 'ma', 'ed', 'se', 'perché', 'anche', 'come', 'dov',
    'dove', 'che', 'chi', 'cui', 'non', 'più', 'quale', 'quanto', 'quanti', 'quanta', 'quante', 'quello', 'quelli',
    'quella', 'quelle', 'questo', 'questi', 'questa', 'queste', 'si', 'tutto', 'tutti', 'a', 'c', 'e', 'i', 'l',
    'o', 'ho', 'hai', 'ha', 'abbiamo', 'avete', 'hanno', 'abbia', 'abbiate', 'abbiano', 'avrò', 'avrai', 'avrà', 'avremo',
    'avrete', 'avranno', 'avrei', 'avresti', 'avrebbe', 'avremmo', 'avreste', 'avrebbero', 'avevo', 'avevi', 'aveva',
    'avevamo', 'avevate', 'avevano', 'ebbi', 'avesti', 'ebbe', 'avemmo', 'aveste', 'ebbero', 'avessi', 'avesse',
    'avessimo', 'avessero', 'avendo', 'avuto', 'avuta', 'avuti', 'avute', 'sono', 'sei', 'è', 'siamo', 'siete',
    'sia', 'siate', 'siano', 'sarò', 'sarai', 'sarà', 'saremo', 'sarete', 'saranno', 'sarei', 'saresti',
    'sarebbe', 'saremmo', 'sareste', 'sarebbero', 'ero', 'eri', 'era', 'eravamo', 'eravate', 'erano', 'fui',
    'fosti', 'fu', 'fummo', 'foste', 'iframe','class','src',
    "più","l","non","dalla","nell","o","alla","nella","nel","si","al","dal","ha","è","e","un","una","uno","che","il", "lo", "la", "i", "gli", "le", "di", "da",
      "del", "dello", "della", "dei", "degli", "delle", "in", "a", "con", "su", "per", "tra", "fra"])

    modello = wordcloud.WordCloud(stopwords=stopwords,width=1920, height=1080, background_color="rgba(255, 255, 255, 0)").generate(new_text)
    modello.to_file("./static/nuvola.png")

    return response

# def news_get(keyword):
#     with open('sample.json', 'r') as openfile:
#         # Reading from json file
#             response = json.load(openfile)
#     return response
