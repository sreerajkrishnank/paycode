from flask import Flask,request
import datetime
import uuid
from elasticsearch import Elasticsearch
es = Elasticsearch()


app = Flask(__name__)

@app.route("/qrCode")
def qrCode():
	data = request.args.get('data')
	args = data.split("_");
	amount = float(args[0]);
	whoPaid = args[1];
	pin = args[2];
	toWhom = args[3];
	if validateCustomerIdRequest(amount, whoPaid, pin, toWhom):
		sendMessage(whoPaid, toWhom, amount, True)
	else:
		sendMessage(whoPaid, toWhom, amount, False)
	return args[0]

def validateCustomerIdRequest(amount, whoPaid, pin, toWhom):
	return validateCustomerIdAndPin(whoPaid, pin) and validateCustomerIdAndPin(toWhom) and validateAndReduceBalance(whoPaid, amount) and addBalance(toWhom, amount)

def validateCustomerIdAndPin(customerId, pin=-1):
	try:
	    res = es.get(index="hackathon", doc_type='userData', id=customerId)	
	    if pin == -1:
	    	return True
	    else:	
	    	return (res['_source']['pin'] == pin)
	except:
		return False

def validateAndReduceBalance(customerId, amount):
	res = es.get(index="hackathon", doc_type='userData', id=customerId)
	if (res['_source']['amount'] >= amount):
		res['_source']['amount'] = res['_source']['amount'] - amount;
		result = es.index(index="hackathon", doc_type='userData', id=customerId, body=res['_source'])
		return True
	else:
		return False

def addBalance(customerId, amount):
	res = es.get(index="hackathon", doc_type='userData', id=customerId)
	res['_source']['amount'] = res['_source']['amount'] + amount;
	result = es.index(index="hackathon", doc_type='userData', id=customerId, body=res['_source'])
	return True	

def sendMessage(whoPaid, toWhom, amount, isSuccessful):
	transactionId = uuid.uuid4()
	doc = {'whoPaid': whoPaid, 'toWhom': toWhom, 'amount': amount, 'timestamp' : datetime.datetime.utcnow(), 'successful' : isSuccessful}
	smsText = ("Transaction successful for Rs: "+ str(amount) if isSuccessful else "Transaction failed");
	sms1 = {'number' : whoPaid, 'text' : smsText}
	es.index(index="hackathon", doc_type='transaction', id=transactionId, body=doc)
	es.index(index="hackathon", doc_type='sms', id=datetime.datetime.utcnow(), body=sms1)
	sms2 = {'number' : toWhom,'text' : smsText}
	es.index(index="hackathon", doc_type='sms', id=datetime.datetime.utcnow(), body=sms2)
	return True

if __name__ == "__main__":
    app.run(debug=True)
