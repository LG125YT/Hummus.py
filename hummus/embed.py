from PIL.Image import open as openImage
from io import BytesIO
import fake_useragent
from typing import *
import requests

def getDimensions(image_url):
	response = requests.get(image_url,headers={"User-Agent":fake_useragent.UserAgent(browsers=['chrome', 'firefox', 'opera', 'safari', 'edge', 'internet explorer']).random})
	if response.status_code == 200:
		img = openImage(BytesIO(response.content))
		width, height = img.size
		return width, height, True
	else:
		raise Exception(f"Failed to retrieve image from URL. Status code: {response.status_code}")

class Field:
	def __init__(self,name,value,inline=False):
		self.name = name
		self.value = value
		self.inline = inline

class Footer:
	def __init__(self,text,icon_url=None):
		self.text = text
		self.icon_url = icon_url

class EmbedAuthor:
	def __init__(self,name,url=None,icon_url=None):
		self.name = name
		self.url = url
		self.icon_url = icon_url

class Thumbnail:
	def __init__(self,url,width=None,height=None):
		self.url = url
		self.width = width
		self.height = height
		self.available = False

	async def getDimensions(self):
		self.width,self.height,self.available = getDimensions(self.url)

class Image:
	def __init__(self,url):
		self.url = url
		self.width = None
		self.height = None
		self.available = False

	async def getDimensions(self):
		self.width,self.height,self.available = getDimensions(self.url)

class Provider:
	def __init__(self,data):
		self.name = data['name']
		self.url = data.get('url')

class Video:
	def __init__(self,url,width=None,height=None):
		self.url = url
		self.width = width
		self.height = height
		self.available = False

	async def getDimensions(self):
		self.width,self.height,self.available = getDimensions(self.url)

class Embed:
	def __init__(self,title:str,description:str,color:int=0,url:Union[str,None]=None,timestamp:Union[str,None]=None):
		self.title = title
		self.description = description
		self.color = color
		self.fields = []
		self.url = url
		self.timestamp = timestamp
		self.author = None
		self.footer = None
		self.thumbnail = None
		self.image = None

	async def addAuthor(self,name:str,url:Union[str,None]=None,icon_url:Union[str,None]=None):
		self.author = EmbedAuthor(name,url,icon_url)

	async def addFooter(self,text:str,icon_url:Union[str,None]=None):
		self.footer = Footer(text,icon_url)

	async def addField(self,name:str,value:str,inline:bool=False):
		self.fields.append(Field(name,value,inline))

	async def addThumbnail(self,url:str):
		self.thumbnail = Thumbnail(url)

	async def addImage(self,url:str):
		self.image = Image(url)

	#for usage in the internal folder
	def _addAuthor(self,name,url=None,icon_url=None):
		self.author = EmbedAuthor(name,url,icon_url)
	
	def _addFooter(self,text,icon_url=None):
		self.footer = Footer(text,icon_url)
	
	def _addField(self,name,value,inline=False):
		self.fields.append(Field(name,value,inline))
	
	def _addThumbnail(self,url):
		self.thumbnail = Thumbnail(url)
	
	def _addImage(self,url):
		self.image = Image(url)

	def _addVideo(self,url,width=None,height=None):
		self.video = Video(url,width,height)

	def _addProvider(self,data):
		self.provider = Provider(data)

class ImageEmbed:
	def __init__(self,data):
		self.type = data['type']
		self.url = data['url']
		self.thumbnail = Thumbnail(data['thumbnail']['url'],data['thumbnail']['width'],data['thumbnail']['height'])

	def _addThumbnail(self,url):
		self.thumbnail = Thumbnail(url)
	
	def _addImage(self,url):
		self.image = Image(url)
	
	def _addVideo(self,url,width=None,height=None):
		self.video = Video(url,width,height)
	
	def _addProvider(self,data):
		self.provider = Provider(data)