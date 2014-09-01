import boto.sqs
import json
import nltk.data
from goose import Goose


class ArticleMessage(object):
    """For passing articles to gif creation queue"""

    def __init__(self, article, uuid):
        self.article = article
        self.uuid = uuid

    def summary(self):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        lines = tokenizer.tokenize(self.article.cleaned_text)
        return " ".join(lines[:3])

    def to_json(self):
        obj = {"title": self.article.title, "image": self.article.top_image.src, "uuid": self.uuid, "text": self.summary() }
        return json.dumps(obj)


if __name__ == '__main__':
    sqs = boto.sqs.connect_to_region("eu-west-1")
    inq = sqs.get_queue("thrumlinkparser")
    message = inq.read()
    if message is not None:
        data = json.loads(message.get_body())
        g = Goose()
        article = g.extract(url=data["url"])
        am = ArticleMessage(article, data["uuid"])
        outq = sqs.get_queue("thrumgifcreator")
        outmessage = outq.new_message(body=am.to_json())
        outq.write(outmessage)
        #print  article.cleaned_text, article.top_image.src, article.title
        inq = sqs.get_queue("thrumlinkparser")
        inq.delete_message(message)
    