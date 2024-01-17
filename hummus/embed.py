import requests
from PIL.Image import open as openImage
from io import BytesIO

def getDimensions(image_url):
	response = requests.get(image_url)
	if response.status_code == 200:
					img = openImage(BytesIO(response.content))
					width, height = img.size
					return width, height
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
	def __init__(self,url):
		self.url = url
		self.width,self.height = getDimensions(url)

class Image:
	def __init__(self,url):
		self.url = url
		self.width,self.height = getDimensions(url)

class Embed:
	def __init__(self,title,description,color:int=0,url=None,timestamp=None):
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

	async def addAuthor(self,name,url=None,icon_url=None):
		self.author = EmbedAuthor(name,url,icon_url)

	async def addFooter(self,text,icon_url=None):
		self.footer = Footer(text,icon_url)

	async def addField(self,name,value,inline=False):
		self.fields.append(Field(name,value,inline))

	async def addThumbnail(self,url):
		self.thumbnail = Thumbnail(url)

	async def addImage(self,url):
		self.image = Image(url)

#example embed
[{
				"title":
				"Holy crapple!",
				"description":
				"Test works!",
				"color":
				16711680,  # Color in decimal (e.g., Red)
				"fields": [{
								"name": "average extra uneccessary info",
								"value": "ignore"
				}, {
								"name": "but wait",
								"value": "theres more?"
				}]
}]