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
        query = message.content.split()[1]
        trad = HanziConv.toTraditional(query)
        embed = discord.Embed(title=f'Converting {query} to Traditional', description=trad)
        await message.channel.send(embed=embed)
    elif message.content.startswith(']tradsimp'):
        query = message.content.split()[1]
        simp = HanziConv.toSimplified(query)
        embed = discord.Embed(title=f'Converting {query} to Traditional', description=simp)
        await message.channel.send(embed=embed)
    elif message.content.startswith(']help'):
        description = """
            **]ce :**
              - Search Mandarin Chinese words in English in simplified/traditional characters or pinyin.

            **]help :**
              - this message

            **]simptrad / ]tradsimp :**
              - convert simplified <-> traditional
        """
        embed = discord.Embed(title=f'List of Commands:', description=description)
        await message.channel.send(embed=embed)
    

client.run(TOKEN)