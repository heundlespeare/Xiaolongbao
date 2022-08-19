# This example requires the 'message_content' intent.
from config import TOKEN
import discord
from lib.dictionaries.cedict import CEDict
from hanziconv import HanziConv
from discord.ext import commands
import json
import Paginator

intents = discord.Intents.default()
intents.message_content = True


cedict = CEDict()


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
    partitions = [results[i:i+NUM_RESULTS_PER_PAGE] for i in range(0, len(results), NUM_RESULTS_PER_PAGE)]
    pages = [discord.Embed(title=f'Search result for {query}, Page {i+1}/{len(partitions)}', description="\n".join(partitions[i])) for i in range(len(partitions))]
    if len(results) == 0:
        embed = discord.Embed(title=f'No result found for {query}')
        await ctx.send(embed=embed)
    else:
        await Paginator.Simple().start(ctx, pages = pages)

@bot.command()
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
async def setprefix(ctx, prefix):
    key = str(ctx.guild.id)
    prefix_dict[key] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefix_dict, f)
    embed = discord.Embed(title=f'Changed prefix to {prefix}')
    await ctx.send(embed=embed)

bot.run(TOKEN)