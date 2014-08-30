import boto.sqs
import boilerpipe
import json

if __name__ == '__main__':
	sqs = boto.sqs.connect_to_region("eu-west-1")
	q = sqs.get_queue("thrumlinkparser")
	message = q.read()
	if message is not None:
		data = json.loads(message.get_body())
		print data
		q.delete_message(message)
	