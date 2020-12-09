from time import *
import sys
import requests
import json as JSON

API_KEY = "Your API Key Here."

def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


def upload():
	filename = input("Enter a filename with full path:  ")
	headers = {'authorization': API_KEY}
	response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=read_file(filename))

	return response.json()

def submit():
	u = upload()
	url = u['upload_url']
	endpoint = "https://api.assemblyai.com/v2/transcript"

	json = {
    	"audio_url": str(url)
	}

	headers = {
	    "authorization": API_KEY,
	    "content-type": "application/json"
	}

	response = requests.post(endpoint, json=json, headers=headers)

	return response.json() # get_transcript(response)

def get_transcript():
	s = submit()
	t_id = str(s['id'])
	endpoint = "https://api.assemblyai.com/v2/transcript/" + t_id

	headers = {
	    "authorization": API_KEY,
	}

	response = requests.get(endpoint, headers=headers)
	r = response.json()
	while r['status'] != 'completed':
		sleep(5)
		tmp = requests.get(endpoint, headers=headers)
		t = tmp.json()
		r = t
		print(r['status'])
	transcript = requests.get(endpoint, headers=headers)
	raw = transcript.json()

	print(raw['text'])

if __name__=="__main__":
	get_transcript()