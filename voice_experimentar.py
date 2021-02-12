import discord
from discord.ext import commands
import youtube_dl
import os
import datetime
from urllib import parse, request
import re

#para que funcione hay que instalar youtube_dl y FFmpeg

client = commands.Bot(command_prefix=">", description="Hi")

'''  
Falta areglar, si no esta tocando nada que se salga del canal de voz etc

bucle infinito con while

https://www.mclibre.org/consultar/python/lecciones/python-while.html
https://www.mclibre.org/consultar/python/lecciones/python-while.html

'''

@client.event
async def on_ready():
    print('logueado como {0.user}'.format(client))
    activity = discord.Game(name=">ayuda ó >helpp",url="https://www.youtube.com/watch?v=V2hlQkVJZhE")
    await client.change_presence(status=discord.Status.online, activity=activity) #idle, online
    '''
    # Setting `Listening ` status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))

    # Setting `Watching ` status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))
    '''

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'**Welcome {member.mention}!**  Listo para jugar? See `>ayuda` para detalles y comandos!')

@client.event
async def on_messaje(message):
    new_message = str(message.content)
    
    await message.channel.purge(limit=1)

    print("Alguien escribio algo")

@client.command()
async def info(ctx):
    autor = str(ctx.message.author) + " se la come!"
    embed = discord.Embed(title=f"{ctx.guild.name}", description= autor, timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
    embed.add_field(name="Server creado a las", value=f"{ctx.guild.created_at}", inline=True)
    embed.add_field(name="Server poseído", value=f"{ctx.guild.owner}", inline=True)
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}", inline=True)
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}", inline=True)
    embed.add_field(name="Miembros", value=f"{ctx.guild.member_count}", inline=True)
    
    #embed.add_field(name="Miembros", value=f"{ctx.guild.members}", inline=True)
    # embed.set_thumbnail(url=f"{ctx.guild.icon}")
    # embed.set_thumbnail(url=icon)
    embed.set_thumbnail(url="https://i.imgur.com/XFubD8u.png")
    await ctx.send(embed=embed)




#busca en youtube sin necesidad de url

@client.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall( r"watch\?v=(\S{11})", html_content.read().decode())
    print(search_results)
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])




#para hacer la lista puedo simplemente hacer un array que guarde las url de los videos, cuando termina una, sigue la otra y así



@client.command()
async def play(ctx, *, search): #play
    #Verificar si esta en el mismo canal que el (canaluser = ctx.message.author.voice.channel)
    
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall( r"watch\?v=(\S{11})", html_content.read().decode())
    print(search_results)
    #await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])

    

    try:
        canal = ctx.message.author.voice.channel
    except Exception as e:
        await ctx.send("**Bop bop... ñeee Primero conectate a un canal de voz**")
    
    v = discord.utils.get(client.voice_clients, guild=ctx.guild)

    

    

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        if v.is_connected():
            await ctx.send(f"Actualmente estoy ocupado en: **{str(v.channel)}**")
            return #probar que hace sin el return

    #voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = "GTA V Online")
    

    #await voiceChannel.connect()
    try:
        await canal.connect()    
    except Exception as e:
        print("el bot ya esta conectado")
    
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', #192 default
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl: #parece que se instancia como ydl_opts
        url = 'https://www.youtube.com/watch?v=' + search_results[0]
        ydl.download([url]) #Aqui podria poner la busqueda sin url para que sea mas facil
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print("Renombrando archivo")
            os.rename(file, "song.mp3")
    
    voice.play(discord.FFmpegPCMAudio("song.mp3"),after=lambda e: print("la cancion termino")) #play a la canción
    print("**La canción se ha reproducido**")
    pyer = str(ctx.message.author)
    if pyer == "͋̈́ͫ҉N͋̈́ͫ҉o͋̈́ͫ҉i͋̈́ͫ҉s͋̈́ͫ҉e#9923":
        await ctx.send(f"**Reproduciendo para mi bb ͋̈́ͫ҉N͋̈́ͫ҉o͋̈́ͫ҉i͋̈́ͫ҉s͋̈́ͫ҉e** {name}")
        autor = str(ctx.message.author) + " mi padre :,D"
        embed = discord.Embed(title=f"{ctx.guild.name}", description= autor, timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
        embed.add_field(name="url", value=f"{url}", inline=True)
        embed.set_thumbnail(url="https://i.imgur.com/XFubD8u.png")
        await ctx.send(embed=embed)
        #await ctx.send("Espero te guste ❤👉👌❤")
    else:
        await ctx.send(f"**Escuchando** {name}")
        autor = str(ctx.message.author) + " Reproduciendo"
        embed = discord.Embed(title=f"{ctx.guild.name}", description= autor, timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
        embed.add_field(name="url", value=f"{url}", inline=True)
        embed.set_thumbnail(url="https://i.imgur.com/XFubD8u.png")
        await ctx.send(embed=embed)
    #lo de abajo solo es para controlar el audio pero no es tan necesario
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1.00 #1.00 es mucho

    #APARTE!!!!!!!!!!!!


@client.command()
async def hola(ctx):
    await ctx.message.channel.purge(limit=1)
    await ctx.send("Hola a tod@s :D")

@client.command()
async def ayuda(ctx):
    await ctx.send("Reproducir >play 'nombre de la canción'  sin comillas\nPausar >pause\nReaunidar >resume\nDetener >stop \nDesconectar del canal de voz >disconnect")

@client.command()
async def helpp(ctx):
    await ctx.send("Reproducir >play 'nombre de la canción'  sin comillas\nPausar >pause\nReaunidar >resume\nDetener >stop \nDesconectar del canal de voz >disconnect")



@client.command()
async def disconnect(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        if voice.is_connected():
            await voice.disconnect()
    except Exception as e:
        await ctx.send("Bop Bop... No estoy connectado en un canal de voz. 😁")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("Musica pausada")
    else:
        await ctx.send("Ningun audio actualmente.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("Musica Resumida")
    else:
        await ctx.send("El audio no esta pausado.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        await ctx.send("Musica Detenida")
        await ctx.send("Si no me necesitas escribe >disconnect")
    else:
        print("no se esta reproduciendo, no se puede detener")
        await ctx.send("Nada reproduciendose, no se puede detener uwu")




    

client.run('ODA4ODEyMjQ1OTczOTkxNDM0.YCL_Gg.DvjPIrqVWskqnSWdKIFsgfxC9lE')