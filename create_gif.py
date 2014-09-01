import boto.sqs
import json
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os, os.path
import requests


def get_filepath(uuid):
    return "images/%s/" % uuid

class TitleImage(object):

    def __init__(self,text, uuid):
        self.text = text
        self.uuid = uuid
        if not os.path.exists(get_filepath(uuid)):
            os.makedirs(get_filepath(uuid))

    def generate(self):
        font = ImageFont.truetype("fonts/Lato-Bold.ttf", 72)
        (w,h) = font.getsize(self.text)
        image = Image.new("RGB", (w + 32, w + 32), "#fff")
        draw = ImageDraw.Draw(image)
        draw.text((16,(w+32)/2 - h), self.text, font=font, fill="#222")
        image = image.resize((640, 640) , Image.ANTIALIAS)
        image.save(self.get_filename(), 'GIF')
        return self

    def get_filename(self):
        return os.path.join(get_filepath(self.uuid),"title.gif")

class ImageImage(object):

    def __init__(self, image_url, uuid):
        self.image_url = image_url
        print self.image_url
        self.uuid = uuid
        self.filename = image_url.split("/")[-1]

    def download(self):
        self.local_filename = os.path.join(get_filepath(self.uuid), self.filename)
        # NOTE the stream=True parameter
        r = requests.get(self.image_url, stream=True)
        with open(self.local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return self

    def save(self):
        image = Image.open(self.local_filename)
        image = image.crop()
        image = image.resize((640, 640) , Image.ANTIALIAS)
        image.save(self.get_filename(), 'GIF')
        return self

    def get_filename(self):
        return os.path.join(get_filepath(self.uuid),"image.gif")


class MainTextImage(object):
    pass


if __name__ == '__main__':
    sqs = boto.sqs.connect_to_region("eu-west-1")
    inq = sqs.get_queue("thrumgifcreator")
    message = inq.read()
    if message is not None:
        data = json.loads(message.get_body())
        inq.delete_message(message)
        img = (TitleImage(data["title"], data["uuid"])).generate()
        print img.get_filename()
        if data["image"]:
            imgimg = (ImageImage(data["image"],data["uuid"])).download().save()
        print data["image"]