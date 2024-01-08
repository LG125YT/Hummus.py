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

	async def addAuthor(self,name,url=None,icon_url=None):
		self.author = EmbedAuthor(name,url,icon_url)

	async def addFooter(self,text,icon_url=None):
		self.footer = Footer(text,icon_url)

	async def addField(self,name,value,inline=False):
		self.fields.append(Field(name,value,inline))

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