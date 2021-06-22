import discord
from discord.ext import commands
from discord import Embed
import asyncio
import json
import DiscordUtils
import youtube_dl

def get_prefix(client, message):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix, intents = discord.Intents.all())
music = DiscordUtils.Music()

rules = [":pushpin: 1. Be respectful, civil, and welcoming. \n\
Sometimes discussion can get heated, but you are responsible for your own behavior.\n\
This includes not targeting individuals and not posting personal information",

":pushpin: 2. No insults, racism, sexism, homophobia, transphobia, and other kinds of discriminatory speech.\n\
We do not welcome these types of speech"]

filtered_words = ["smoke", "smoking", "drink", "drinking"]

@client.event
async def on_ready():
  print("Bot is ready")

@client.event
async def on_guild_join(guild):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  prefixes[str(guild.id)] = '~'

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=4)

""" @client.event
async def on_guild_remove(guild):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  prefixes.pop(str(guild.id))

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=4) """

@client.command(aliases=['prefix'])
async def setprefix(ctx, prefixset):
  if (not ctx.author.guild_permissions.manage_channels):
    await ctx.send('This command requires ``Manage Channels``')
    return

  if (prefixset == None):
    prefixset = '~'


  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  prefixes[str(ctx.guild.id)] = prefixset

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=4)
   
    await ctx.send(f'The bot prefix has been changed to {prefixset}')
   
@client.event
async def on_message(msg):
  for word in filtered_words:
    if word in msg.content:
      await msg.delete()
    

  await client.process_commands(msg)

@client.command()
async def hello(ctx):
  await ctx.send("Hello Sir! Hope You are doing well :)")

""" @client.event
async def on_command_error(ctx,error):
  await ctx.send("You can't do that ;-;")
  await ctx.message.delete() """

@client.command()
async def rule(ctx,*,number):
  await ctx.send(rules[int(number)-1])

@client.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2):
  await ctx.channel.purge(limit = amount)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "Inactive"):
  try:
    await member.send("You have been kicked form the Happy House 3.0, Beacuse:" +reason)
  except:
    await ctx.send("The member has their dms closed")

  await ctx.send(member.name +  " has been kicked from the Happy House 3.0, Beacuse:" + reason)
  await member.kick(reason=reason)

@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "Inactive"):
  await ctx.send(member.name +  " has been banned from the Happy House 3.0, Beacuse:" + reason)
  await member.ban(reason=reason)

@client.command(aliases=['ub'])
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
  banned_users = await ctx.guild.bans()
  member_name, member_disc = member.split('#')

  for banned_entry in banned_users:
    user = banned_entry.user

    if(user.name, user.discriminator)==(member_name, member_disc):

      await ctx.guild.unban(user)
      await ctx.send(member_name +" has been unbanned!")
      return
      
  await ctx.send(member+" was not found")

@client.command(aliases=['user','info'])
@commands.has_permissions(kick_members=True)
async def whois(ctx, member : discord.Member):
  embed = discord.Embed(title = member.name , description = member.mention , color = discord.Colour.red())
  embed.add_field(name = "ID", value = member.id , inline = True)
  embed.set_thumbnail(url = member.avatar_url)
  embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
  await ctx.send(embed=embed)

@client.command(aliases = ['pl'])
async def poll(ctx,*,msg):
  channel = ctx.channel
  try:
    op1 , op2 = msg.split("or")
    txt = f"React with ✅ for {op1} or ❎ for {op2}"
  except:
    await channel.send("Correct Syntax: [Choice1] or [Choice2]")
    return

  embed = discord.Embed(title="Poll", description = txt, color = discord.Colour.red())
  message_ = await channel.send(embed=embed)
  await message_.add_reaction("✅")
  await message_.add_reaction("❎")
  await ctx.message.delete()

songs = asyncio.Queue()
play_next_song = asyncio.Event()

@client.command()
async def join(ctx):
  await ctx.author.voice.channel.connect()
  await ctx.send('Joined your voice channel')

@client.command()
async def leave(ctx):
  await ctx.voice_client.disconnect()
  await ctx.send('Left your voice channel')


""" @client.command(name= 'play', help= 'This command plays a song')
async def play(ctx, url):
  if ctx.message.author.voice:
    await ctx.send ('You are not connected to voice channel')
    return
  else:
    channel = ctx.message.author.voice.channel

  await channel.connect() """


""" @client.command(name= 'stop', help= 'This command plays a song')
async def stop(ctx):
  voice_client = ctx.message.guild.voice_client
  await voice_client.disconnect()
 """
#server = ctx.message.guild
#voice_channel = ctx.message.guild.voice_client
""" 
@client.command
async def play(ctx, url):
  if ctx.message.author.voice:
    await ctx.send ('You are not connected to voice channel')
    return
  else:
    channel = ctx.message.author.voice.channel

  await channel.connect()
  async with ctx.typing():
    player = await YTDLSource.from_url(url, client.loop)
    ctx.message.guild.voice_clien.play(player, after=lambda e: print('Player error: %s' %e) if e else None)
    await ctx.send(f'Now Playing: {player.title}') """





@client.command()
async def play(ctx, *, url):
    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        await ctx.send(f"Playing {song.name}")
    else:
        song = await player.queue(url, search=True)
        await ctx.send(f"Queued {song.name}")

""" async def audio_player_task():
    while True:
        play_next_song.clear()
        current = await songs.get()
        current.start()
        await play_next_song.wait()


def toggle_next():
    client.loop.call_soon_threadsafe(play_next_song.set)


@client.command(pass_context=True)
async def play(ctx, url):
    if not client.is_voice_connected(ctx.message.server):
        voice = await client.join_voice_channel(ctx.message.author.voice_channel)
    else:
        voice = client.voice_client_in(ctx.message.server)

    player = await voice.create_ytdl_player(url, after=toggle_next)
    await songs.put(player)

client.loop.create_task(audio_player_task()) """

@client.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send(f"Paused {song.name}")

@client.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send(f"Resumed {song.name}")

""" @client.command()
async def stop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await player.stop()
    await ctx.send("Stopped") """

@client.command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        await ctx.send(f"Enabled loop for {song.name}")
    else:
        await ctx.send(f"Disabled loop for {song.name}")

@client.command()
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await ctx.send(f"{', '.join([song.name for song in player.current_queue()])}")

@client.command()
async def np(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    await ctx.send(song.name)

@client.command()
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    if len(data) == 2:
        await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
    else:
        await ctx.send(f"Skipped {data[0].name}")

@client.command()
async def volume(ctx, vol):
    player = music.get_player(guild_id=ctx.guild.id)
    song, volume = await player.change_volume(float(vol) / 100) # volume should be a float between 0 to 1
    await ctx.send(f"Changed volume for {song.name} to {volume*100}%")

@client.command()
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))
    await ctx.send(f"Removed {song.name} from queue")


""" client.remove_command("help")

@client.group(invoke_without_command = True)
async def help(ctx):
  em = discord.Embed(title = "Help", description = "Use ~help <command> for extended information on a command.", color = ctx.author.color)

  em.add_field(name = "Moderation", value = "kick,ban,clear,poll,unban,info")
  em.add_field(name = "Fun", value = "Can add anything")

  await ctx.send(embed = em)

@help.command()
async def kick (ctx):

  em = discord.Embed(title = "Kick", description = "Kicks a member from the guild", color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "~kick/k <member> [reason]")

  await ctx.send(embed = em) 
   
@help.command()
async def ban (ctx):

  em = discord.Embed(title = "Ban", description = "Ban a member from the guild", color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "~ban/b <member> [reason]")

  await ctx.send(embed = em) 

@help.command()
async def unban (ctx):

  em = discord.Embed(title = "UnBan", description = "UnBan a member from the guild", color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "~unban/ub <member>#<id>")

  await ctx.send(embed = em)  

@help.command()
async def clear (ctx):

  em = discord.Embed(title = "Clear", description = "Clear a member from the guild", color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "~clear/c [amount=2]")

  await ctx.send(embed = em) 

@help.command()
async def whois (ctx):

  em = discord.Embed(title = "WhoIs", description = "Give a info of a member from the guild", color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "~whois/info/user <member>")

  await ctx.send(embed = em)

@help.command()
async def poll (ctx):

  em = discord.Embed(title = "Poll", description = "Take a Poll", color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "~poll/pl <p1> or <p2>")

  await ctx.send(embed = em)

@help.command()
async def help (ctx):

  em = discord.Embed(title = "Help", description = "Help a member from the guild", color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "~help [command]")

  await ctx.send(embed = em)  """



client.run("TOKEN-KEY")