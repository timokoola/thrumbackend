#
import boto.sqs
import os, sys
import json
import uuid

class UrlPackage(object):
	"""Class for sending URLs to queue"""
	def __init__(self,url):
		self.url = url
		self.uuid = uuid.uuid4()

	def to_json(self):
		obj = {"url": self.url, "uuid": str(self.uuid) }
		return json.dumps(obj)

if __name__ == '__main__':
	url = UrlPackage(sys.argv[1])
	sqs = boto.sqs.connect_to_region("eu-west-1")
	q = sqs.get_queue("thrumlinkparser")
	message = q.new_message(body=url.to_json())
	q.write(message)


