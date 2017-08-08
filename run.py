import discord
import time
import config
from config import token, link, prefix, ownerid
from discord.ext.commands import Bot

client = Bot(prefix)

@client.event
async def on_ready():
    print("----------------------")
    print("Logged In As")
    print("Username: %s"%client.user.name)
    print("ID: %s"%client.user.id)
    print("----------------------")

@client.command()
async def ping():
    '''See if The Bot is Working'''
    pingtime = time.time()
    pingms = await client.say("Pinging...")
    ping = time.time() - pingtime
    await client.edit_message(pingms, ":ping_pong:  time is `%.01f seconds`" % ping)
    
@client.command()
async def botinvite():
    '''A Link To Invite This Bot To Your Server!'''
    await client.say("Check Your Dm's :wink:")
    await client.whisper(link)

#gets a server invite and pms it to the user who requested it  

@client.command(pass_context=True)
async def serverinvte(context):
	"""Pm's A Invite Code (To The Server) To The User"""
	invite = await client.create_invite(context.message.server,max_uses=1,xkcd=True)
	await client.send_message(context.message.author,"Your invite URL is {}".format(invite.url))
	await client.say ("Check Your Dm's :wink: ")

#Gets a List of Bans From The Server

@client.command(pass_context = True)
async def gbans(ctx):
    '''Gets A List Of Users Who Are No Longer With us'''
    x = await client.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "List of The Banned Idiots", description = x, color = 0xFFFFF)
    return await client.say(embed = embed)

#Lists Info About The server

@client.command(pass_context = True)
async def serverinfo(ctx):
    '''Displays Info About The Server!'''

    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: #Just in case there are too many roles...
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles);
    channelz = len(server.channels);
    time = str(server.created_at); time = time.split(' '); time= time[0];

    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', colour = 0xFFFF);
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = '__Owner__', value = str(server.owner) + '\n' + server.owner.id);
    join.add_field(name = '__ID__', value = str(server.id))
    join.add_field(name = '__Member Count__', value = str(server.member_count));
    join.add_field(name = '__Text/Voice Channels__', value = str(channelz));
    join.add_field(name = '__Roles (%s)__'%str(role_length), value = roles);
    join.set_footer(text ='Created: %s'%time);

    return await client.say(embed = join);

#a command that sets the bots game

@client.command(pass_context=True)
async def setgame(ctx, *, game):
    """Sets my game (Owner)"""
    if ctx.message.author.id == (ownerid):
        message = ctx.message
        await client.delete_message(message)
        await client.whisper("Game was set to **{}**!".format(game))
        await client.change_presence(game=discord.Game(name=game))

#Clears The Chat

@client.command(pass_context=True)       
async def clear(ctx, number):
    '''Clears The Chat 2-100'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await client.say("You do not have the role: Admin")
    pass
    mgs = []
    number = int(number)
    async for x in client.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await client.delete_messages(mgs)

@client.command()
async def warn(user="", reason="", mod="", n="", channel=""):
    """Warns a Member"""
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await client.say("You do not have the role: Admin")
    pass

    if user == "":
        await client.say(":x: No user Mentioned")
    if reason == "":
        await client.say(":x: No reason entered!")
    if mod == "":
        await client.say(":x: No Mod is Selected!")
    if n == "":
        await client.say(":x: No Warn Number was selected")
    if channel == "":
        await client.say(":x: No Channel entered!")
    channel = client.get_channel(channel)
    em = discord.Embed(color=0x42fc07)
    em.add_field(name='Warning', value=("You Have Been Warned -->"))
    em.add_field(name='User', value=(user))
    em.add_field(name='Reason', value=(reason))
    em.add_field(name='Moderator', value=(mod))
    em.set_footer(text="Warnings had : {}".format(n))
    await client.send_message(channel, embed=em)

@client.command(pass_context=True, hidden = True)
async def report(ctx, user: discord.Member, *, reason):
    """Reports user and sends report to Bot Admin"""
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await client.say("You do not have the role: Admin")
    pass

    author = ctx.message.author
    server = ctx.message.server


    joined_at = user.joined_at
    user_joined = joined_at.strftime("%d %b %Y %H:%M")
    joined_on = "{}".format(user_joined)

    args = ''.join(reason)
    adminlist = []
    check = lambda r: r.name in 'YOUR_ROLE_HERE'

    members = server.members
    for i in members:

        role = bool(discord.utils.find(check, i.roles))

        if role is True:
            adminlist.append(i)
        else:
            pass

    colour = discord.Colour.magenta()

    description = "User Reported"
    data = discord.Embed(description=description, colour=colour)
    data.add_field(name="Report reason", value=reason)
    data.add_field(name="Report by", value=author)
    data.add_field(name="Reported user joinned this server on", value=joined_on)
    data.set_footer(text="User ID:{}"
                            "".format(user.id))

    name = str(user)
    name = " ~ ".join((name, user.nick)) if user.nick else name

    if user.avatar_url:
        data.set_author(name=name, url=user.avatar_url)
        data.set_thumbnail(url=user.avatar_url)
    else:
        data.set_author(name=name)

    for i in adminlist:
        await client.send_message(i, embed=data)

@client.command(pass_context = True)
async def ban(ctx, member : discord.Member = None, days = " ", reason = " "):
    """Bans specified member from the server."""
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await client.say("You do not have the role: Admin")
    pass

    try:
        if member == None:
            await client.say(ctx.message.author.mention + ", please specify a member to ban.")
            return

        if member.id == ctx.message.author.id:
            await client.say(ctx.message.author.mention + ", you cannot ban yourself.")
            return
        else:
            await client.ban(member, days)
            if reason == ".":
                await client.say(member.mention + " has been banned from the server.")
            else:
                await client.say(member.mention + " has been banned from the server. Reason: " + reason + ".")
            return
    except Forbidden:
        await client.say("You do not have the necessary permissions to ban someone.")
        return
    except HTTPException:
        await client.say("Something went wrong, please try again.")

#Kick a Member From The Server

@client.command(pass_context = True)
async def kick(ctx, *, member : discord.Member = None):
    '''Kicks A User From The Server'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await client.say("You do not have the role: Admin")
    pass

    if not member:
        return await client.say(ctx.message.author.mention + "Specify a user to kick!")
    try:
        await client.kick(member)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            return await client.say(":x: Privilege too low!")
 
    embed = discord.Embed(description = "**%s** has been kicked."%member.name, color = 0xF00000)
    embed.set_footer(text="BasicDiscord Bot v1.0")
    await client.say(embed = embed)

#Mutes a Member From The server

@client.command(pass_context = True)
async def mute(ctx, *, member : discord.Member):
    '''Mutes A Memeber'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await client.say("You do not have the role: Admin")
    pass

    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    await client.edit_channel_permissions(ctx.message.channel, member, overwrite)

    await client.say("**%s** is now Muted! Wait For an Unmute.."%member.mention)

#Unmutes a member

@client.command(pass_context = True)
async def unmute(ctx, *, member : discord.Member):
    '''Unmutes The Muted Memeber'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await client.say("You do not have the role: Admin")
    pass

    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = True
    await client.edit_channel_permissions(ctx.message.channel, member, overwrite)

    await client.say("**%s** Times up...You are Unmuted!"%member.mention)


client.run(token)
