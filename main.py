# This example requires the 'message_content' intent.
from config import TOKEN
import discord
from lib.dictionaries.cedict import CEDict
from hanziconv import HanziConv
from discord.ext import commands
import json
import Paginator

from lib.dictionaries.taishanese import TaishaneseDict
from utils import paginate

intents = discord.Intents.default()
intents.message_content = True


cedict = CEDict()
taishan_dict = TaishaneseDict()

DEFAULT_PREFIX = ']'
NUM_RESULTS_PER_PAGE = 5

prefix_dict = json.load(open('prefixes.json','r'))
async def get_prefix(client, message):
    key = str(message.guild.id)
    if key not in prefix_dict:
        return DEFAULT_PREFIX
    else:
        return prefix_dict[key]

bot = commands.Bot(command_prefix=(get_prefix), intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def ce(ctx, query):
    results = cedict.search(query)
    pages = paginate(query, results, NUM_RESULTS_PER_PAGE)
    if len(results) == 0:
        embed = discord.Embed(title=f'No result found for {query}')
        await ctx.send(embed=embed)
    else:
        await Paginator.Simple().start(ctx, pages = pages)

@bot.command(aliases=["conv", "c"])
async def convert(ctx, *, text):
    trad = HanziConv.toTraditional(text)
    simp = HanziConv.toSimplified(text)
    if text != simp:
        embed = discord.Embed(title=f'Converting to Simplified', description=simp)
    else:
        embed = discord.Embed(title=f'Converting to Traditional', description=trad)
    await ctx.send(embed=embed)

@bot.command()
async def simptrad(ctx, *, text):
    trad = HanziConv.toTraditional(text)
    embed = discord.Embed(title=f'Converting to Traditional', description=trad)
    await ctx.send(embed=embed)    

@bot.command()
async def tradsimp(ctx, *, text):
    simp = HanziConv.toSimplified(text)
    embed = discord.Embed(title=f'Converting to Simplified', description=simp)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    key = str(ctx.guild.id)
    prefix_dict[key] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefix_dict, f)
    embed = discord.Embed(title=f'Changed prefix to {prefix}')
    await ctx.send(embed=embed)

@bot.command(aliases=["ts"])
async def taishan(ctx, lang, query):
    lang = lang.lower()
    if lang == "taishanese" or lang == "ts":
        results = taishan_dict.search_taishanese(query)
    elif lang == "en" or lang == "english":
        results = taishan_dict.search_english(query)
    elif lang == "mando" or lang == "mandarin":
        results = taishan_dict.search_mandarin(query)
    elif lang == "canto" or lang == "cantonese":
        results = taishan_dict.search_cantonese(query)
    else:
        results = []
    if len(results) == 0:
        embed = discord.Embed(title=f'No result found for {query}')
    else:
        embed = paginate(query, results, NUM_RESULTS_PER_PAGE)
    await ctx.send(embed=embed)

bot.run(TOKEN)