import discord
from discord.ext import commands

# Deine Discord-Bot-Token hier einfügen
TOKEN = 'Your Bot Token'

# Liste der Beleidigungen
BAD_WORDS = ["crazy", "Crazy?", "crazy?"]

# Liste der whitelisted Personen (nach Discord-Benutzer-ID)
WHITELISTED_USERS = [693227494815563826]

intents = discord.Intents.default()
intents.message_content = True  # Aktiviert das Empfangen von Nachrichteninhalten

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.id in WHITELISTED_USERS:
        await bot.process_commands(message)
        return
    
    content = message.content.lower()
    
    for word in BAD_WORDS:
        if word in content:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, bitte halte die Kommunikation freundlich.")
            return  # Sofort abbrechen, wenn eine Beleidigung erkannt wurde

    await bot.process_commands(message)

@bot.command()
async def clear(ctx, amount=500):  # Standardmäßig 500 Nachrichten löschen
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'{amount} Nachricht(en) wurden gelöscht.', delete_after=500)

bot.run(TOKEN)
