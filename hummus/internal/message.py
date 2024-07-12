from ..embed import Embed, ImageEmbed

async def prepareEmbed(embed):
	prep_embed = {"title":embed.title,"description":embed.description,"color":embed.color,"url":embed.url,"timestamp":embed.timestamp,"fields":[]}
	if embed.image:
		prep_embed["image"] = {"url":embed.image.url,"width":embed.image.width,"height":embed.image.height}
	if embed.thumbnail:
		prep_embed["thumbnail"] = {"url":embed.thumbnail.url,"width":embed.thumbnail.width,"height":embed.thumbnail.height}
	if embed.footer:
		prep_embed["footer"] = {"text":embed.footer.text,"icon_url":embed.footer.icon_url}
	if embed.author:
		prep_embed["author"] = {"name":embed.author.name,"url":embed.author.url,"icon_url":embed.author.icon_url}
	for field in embed.fields:
		prep_embed['fields'].append({"name":field.name,"value":field.value,"inline":field.inline})
	return prep_embed

def makeEmbed(embeds):
	prep = []
	for embed in embeds:
		if embed['type'] == "image" or embed['type'] == "gifv":
			e = ImageEmbed(embed)
		else:
			e = Embed(embed.get('title'),embed.get('description'),embed.get('color'),embed.get('url'),embed.get('timestamp'))
		if embed.get('fields') and type(e) == Embed:
			for field in embed['fields']:
				e._addField(field.get('name'),field.get('value'),field.get('inline'))
		if embed.get('video'):
			e._addVideo(embed['video']['url'],embed['video']['width'],embed['video']['height'])
		if embed.get('provider'):
			e._addProvider(embed['provider'])
		if embed.get('image'):
			e._addImage(embed['image']['url'])
		if embed.get('thumbnail'):
			e._addThumbnail(embed['thumbnail']['url'])
		if embed.get('footer'):
			e._addFooter(embed['footer']['text'],embed['footer'].get('icon_url'))
		if embed.get('author'):
			e._addAuthor(embed['author']['name'],embed['author'].get('url'),embed['author'].get('icon_url'))
		prep.append(e)
	return prep


class Reply:
	def __init__(self,message):
		self.content = message.content
		self.author = message.author