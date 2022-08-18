# This example requires the 'message_content' intent.
from config import TOKEN
import discord
from lib import corpusRequest
from lib.dictionaries import cedict

intents = discord.Intents.default()
intents.dm_messages = True

client = discord.Client(intents=intents)

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
    elif message.content.startswith(']dict'):
        arg = message.content.split()[1]
        if arg not in cedict.whole_dict:
            embed = discord.Embed(title=f'no result found for {arg}')
        else:
            result = cedict.whole_dict[arg]
            description = ""
            for word in result:
                description += f'**{word["simplified"]}/{word["traditional"]}({word["pinyin"]})**\n'
                for i, defn in enumerate(word["english"]):
                    description +=f'   {i+1}. {defn}\n'
                description += "\n"
            embed = discord.Embed(title=f'Search result for {arg}', description=description)
        await message.channel.send(embed=embed)
        
client.run(TOKEN)