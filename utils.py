import discord


def paginate(query:str, entries:list[str], results_per_page:int) -> list[discord.Embed]:
    partitions = [entries[i:i+results_per_page] for i in range(0, len(entries), results_per_page)]
    pages = [discord.Embed(title=f'Search result for {query}', description="\n".join(partitions[i])) for i in range(len(partitions))]
    return pages