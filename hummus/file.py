from requests_toolbelt import MultipartEncoder
import tempfile
import filetype
import random
import string
import json
import io

class File:
	def __init__(self,file):
		read = None
		filename = None
		thing = None

		if type(file) == io.BufferedReader:
			file = file.read() #the lines below should rake care of the rest

		if type(file) == bytes:
			with tempfile.NamedTemporaryFile(delete=True) as temp_file:
				temp_file.write(file)
				kind = filetype.guess(temp_file.name)
			filename = f"image.{kind.extension}"
			thing = (filename, file, kind.mime)
			read = file

		if type(file) == str:
			openedfile = open(file,"rb")
			kind = filetype.guess(file)
			read = openedfile.read()
			filename = file.split("/")[-1]
			thing = (file, read, kind.mime)

		if type(file) == io.BytesIO:
			kind = filetype.guess(file.getvalue())
			filename = f"image.{kind.extension}"
			read = file.getvalue()
			thing = (filename,read, kind.mime)

		self.headers = {
		'Content-Type': 'multipart/form-data; boundary=418737004913864675834237162763',
		} #this will be filled with token and useragent before message send
		self.file_json = {"filename":filename,"Content-Type":"image/png"}
		self.fields = {"file":thing,"payload_json":None} #"payload_json" will also be filled later along with token and useragent
		fakedata = {'content': "",'tts':False,'file':self.file_json}
		fakefields = {"file":thing,"payload_json":json.dumps(fakedata)}
		self.data = MultipartEncoder(fields=fakefields,boundary='----WebKitFormBoundary'+''.join(random.sample(string.ascii_letters+string.digits,16)))
		self.headers['Content-Type'] = self.data.content_type