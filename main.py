# This example requires the 'message_content' intent.
from config import TOKEN
import discord
from lib import corpusRequest
from lib.dictionaries.cedict import CEDict
from hanziconv import HanziConv

intents = discord.Intents.default()
intents.dm_messages = True

client = discord.Client(intents=intents)

cedict = CEDict()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('corpus'):
        args = message.content.split()[1:]
        lang = args[0]
        corpus = args[1]
        print(" ".join(args[2:]))
        if corpus == 'lcmc':
            corpus = corpusRequest.lcmc
        elif corpus == 'web':
            corpus = 'INTERNET-ZH'
        words = " ".join(args[2:])
        await message.channel.send(f'Searching for instances of **{words}** in corpus **{corpus}** :\n'+ corpusRequest.leedsLookup(corpus, words))
    elif message.content.startswith(']ce'):
        query = message.content.split()[1]
        description = cedict.search(query)
        if not description:
            embed = discord.Embed(title=f'No result found for {query}')
        else:
            embed = discord.Embed(title=f'Search result for {query}', description=description)
        await message.channel.send(embed=embed)
    elif message.content.startswith(']simptrad'):
        query = message.content[10:]
        trad = HanziConv.toTraditional(query)
        embed = discord.Embed(title=f'Converting to Traditional', description=trad)
        await message.channel.send(embed=embed)
    elif message.content.startswith(']tradsimp'):
        query = message.content[10:]
        simp = HanziConv.toSimplified(query)
        embed = discord.Embed(title=f'Converting to Simplified', description=simp)
        await message.channel.send(embed=embed)
    elif message.content.startswith(']convert'):
        # TODO: if I decide to stop hardcoding I should probably stop slicing by index number. save prefix by server in a json file and slice by prefix + number:
        query = message.content[9:]
        trad = HanziConv.toTraditional(query)
        simp = HanziConv.toSimplified(query)
        if query != simp:
            embed = discord.Embed(title=f'Converting to Simplified', description=simp)
        else:
            embed = discord.Embed(title=f'Converting to Traditional', description=trad)
        await message.channel.send(embed=embed)
    elif message.content.startswith(']help'):
        description = """
            **]ce :**
              - Search Mandarin Chinese words in English in simplified/traditional characters or pinyin.

            **]help :**
              - this message

            **]convert / ]simptrad / ]tradsimp :**
              - convert simplified <-> traditional
        """
        embed = discord.Embed(title=f'List of Commands:', description=description)
        await message.channel.send(embed=embed)
    

client.run(TOKEN)