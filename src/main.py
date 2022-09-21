from argparse import ArgumentError
from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
import random

load_dotenv()  # Loads the .env file

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    intents=intents  # Set up basic permissions
)


bot.author_id = os.getenv("DISCORD_AUTHOR_ID")  # Change to your discord id


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


@bot.command(name='name')  # Repeat the name of the user
async def name(ctx):
    await ctx.send(f'{ctx.author.display_name}')


@bot.command(name='d6')  # Roll a dice
async def d6(ctx):
    await ctx.send(f'After the roll of the {"🎲"} you got : {random.randint(1, 6)}')


@bot.listen()  # Reply to a message
async def on_message(message):
    if message.content == 'Salut tout le monde':
        await message.channel.send('Salut tout seul {}'.format(message.author.mention))


@bot.command()  # Give a role admin to a user
async def admin(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Please specify a member")
    if member.roles == discord.Permissions.administrator:
        await ctx.send("This user is already an administrator")
    else:
        role = discord.utils.get(ctx.guild.roles, name="Admin")
        if role is None:
            perms = discord.Permissions(
                administrator=True, manage_channels=True, ban_members=True, kick_members=True)
            create_admin = await ctx.guild.create_role(name="Admin", permissions=perms)
            await ctx.send("Congratz! Admin role have been created and {} added to it!".format(member.mention))
            await member.add_roles(create_admin)
        else:
            perms = discord.Permissions()
            perms.update(administrator=True, manage_channels=True,
                         ban_members=True, kick_members=True)
            await role.edit(permissions=perms)
            await ctx.send("Congratz! {} have been added to the Admin role!".format(member.mention))
            await member.add_roles(role)


@bot.command()  # Kick a user
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason=None):
    if member is None:
        await ctx.send("Please specify a member")
    else:
        await member.ban(reason=reason)


@bot.command()  # Count members in server and show their status
async def count(ctx):
    members = ctx.guild.members
    online = 0
    offline = 0
    idle = 0
    dnd = 0
    for member in members:
        print(member.status)
        if member.status == discord.Status.online:
            online += 1
        elif member.status == discord.Status.offline:
            offline += 1
        elif member.status == discord.Status.idle:
            idle += 1
        elif member.status == discord.Status.dnd:
            dnd += 1
    await ctx.send("Online: {}\nOffline: {}\nIdle: {}\nDo not disturb: {}".format(online, offline, idle, dnd))


@bot.command()  # Post a random comic from xkcd
async def xkcd(ctx):
    comic = random.randint(1, 2400)
    await ctx.send("https://xkcd.com/{}/".format(comic))


@bot.command(name='poll')  # Create a poll yes/no answer
async def poll(ctx, *, question):
    embed = discord.Embed(title=question, color=0x00ff00)
    embed.add_field(name="Yes", value=":thumbsup:", inline=True)
    embed.add_field(name="No", value=":thumbsdown:", inline=True)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')


token = os.getenv("DISCORD_TOKEN")  # Token is in the .env
bot.run(token)  # Starts the bot
