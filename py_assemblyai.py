from time import *
import sys, os
import requests
import json as JSON

API_KEY = str(os.environ['ASSEMBLYAPIKEY'])

file_output = False
out_file = ''

def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


def upload():
	filename = input("Enter an input file:  ")
	print("If you input a name below, I will append '.txt' to it and put the transcript there.")
	output_file = input("Enter an output file (Else, output will be directed to STDOUT.):  ")
	if output_file:
		global file_output
		file_output = True
		global out_file
		out_file = output_file + '.txt'
		print("line 27 " + str(file_output) + ' '+ str(out_file))
	headers = {'authorization': API_KEY}
	response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=read_file(filename))

	return response.json()

def submit():
	u = upload()
	if u['upload_url']:
		url = u['upload_url']
	else:
		print(u)
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
	print("line 73 " + str(file_output))
	if file_output:

		output = out_file
		with open(output, 'wt') as f:
			for line in raw['text']:
				f.write(line)
		return output

	print(raw['text'])

if __name__=="__main__":
	get_transcript()
