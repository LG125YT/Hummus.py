from typing import *
import tempfile
import filetype
import io

class File:
	def __init__(self,file:Union[str,bytes,io.BufferedReader,io.BytesIO],file_name:str="file",empty:bool=False):
		self.empty = empty
		if empty:
			return
		read = None
		filename = None
		thing = None #me smol brain hav no idea what to name

		if type(file) == io.BufferedReader:
			file = file.read()
			with tempfile.NamedTemporaryFile(delete=True) as temp_file:
				temp_file.write(file)
				kind = filetype.guess(temp_file.name)
			filename = file_name
			read = file
			if not kind:
				thing = (file, read, 'unsupported')
			else:
				thing = (file, read, kind.mime)
				filename += f".{kind.extension}"

		elif type(file) == bytes:
			with tempfile.NamedTemporaryFile(delete=True) as temp_file:
				temp_file.write(file)
				kind = filetype.guess(temp_file.name)
			filename = file_name
			read = file
			if not kind:
				thing = (file, read, 'unsupported')
			else:
				thing = (file, read, kind.mime)
				filename += f".{kind.extension}"

		elif type(file) == str:
			openedfile = open(file,"rb")
			read = openedfile.read()
			kind = filetype.guess(file)
			filename = file.split("/")[-1]
			thing = (file, read, 'unsupported') if not kind else (file, read, kind.mime)

		elif type(file) == io.BytesIO:
			kind = filetype.guess(file.getvalue())
			filename = file_name
			read = file.getvalue()
			if not kind:
				thing = (file, read, 'unsupported')
			else:
				thing = (file, read, kind.mime)
				filename += f".{kind.extension}"

		else:
			from .utils import Exceptions
			raise Exceptions.FileError(f"Invalid file type: {type(file)}. Please pass a file object, bytes, BytesIO or string.")

		self.fields = {"file":thing,"payload_json":None}
		self.file_json = {"filename":filename,"Content-Type":thing[2]}

	async def get_file_data(self) -> bytes:
		if self.empty:
			return #type:ignore
		return self.fields['file'][1]

class Attachment:
	def __init__(self,data,instance):
		self.instance = instance
		self.id:str = data['id']
		self.filename:str = data['filename']
		self.size:int = data['size']
		self.url:str = data['url']
		self.proxy_url:str = data['proxy_url']
		self.height:int = data.get('height')
		self.width:int = data.get('width')

class Icon: #guild icon, user avatar, banner, etc
	def __init__(self,data,type,instance,is_user=False):
		from .utils import Enums #haha i love circular import errors!
		self.instance = instance
		self.object_id:str = data['id']
		self.id:str = data.get(type)
		self.url:Union[str,None] = f"{instance.cdn+type}s/{self.object_id}/{self.id}.png"
		if not self.id:
			self.url = None
			if is_user:
				self.url = Enums.DefaultAvatars.all[int(data['discriminator'])%5]