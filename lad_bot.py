"""
*******************************************************************************************************************
Project Description:
    La araña discoteca bot is a Discord music-player bot. Name inspired by Community, but dubbed 'LAD-bot' for short.
    LAD-bot is written on python, utilizing the discord api.

Author:
    crow
*******************************************************************************************************************
"""

import utilities
import asyncio
import discord
import requests
import youtube_dl
from discord.ext import commands


intents = discord.Intents().all()
client = discord.Client(intents=intents)

# bot instance, defining a command prefix
lad_bot = commands.Bot(command_prefix='::')

FFMPEG_PREFERENCE = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 1',
    'options': '-vn'
}

sessions = []

def check_session(ctx):
    """
    :desc: Checks if session with same characteristics (guild/channel) as ctx param
    :param ctx: discord.ext.commands.Context
    :return: session()
    """
    if len(sessions) >= 1:
        for session in sessions:
            if session.guild == ctx.guild and session.channel == ctx.author.voice.channel:
                return session
        session = utilities.Session(
            ctx.guild, ctx.author.voice.channel, id=len(sessions))
        sessions.append(session)
        return session
    else:
        session = utilities.Session(ctx.guild, ctx.author.voice.channel, id=0)
        sessions.append(session)
        return session


def prepare_continue_queue(ctx):
    """
    :description: Used to call next song in queue
                  Since Lambda functions cannot call async functions, this workaround lets us continue
                  the queue after the current song ends
    :param ctx: discord.ext.Commands.Context
    :return: None
    """
    fut = asyncio.run_coroutine_threadsafe(continue_queue(ctx), lad_bot.loop)
    try:
        fut.result()
    except Exception as e:
        print(e)


async def continue_queue(ctx):
    """
        :Description: Checks if there is a valid pointer in queue, proceeds to play next song.
                      Recursive loop using prepare_continue_queue to ensure the parsing of each in queue
        :param ctx: discord.ext.commands.Context
        :return: None
        """
    session = check_session(ctx)
    if not session.q.theres_next():
        await ctx.send("Queue has come to an end.")
        return

    session.q.next()

    voice = discord.utils.get(lad_bot.voice_clients, guild=session.guild)
    source = await discord.FFmpegOpusAudio.from_probe(session.q.current_music.url, **FFMPEG_PREFERENCE)

    if voice.is_playing():
        voice.stop()
    voice.play(source, after=lambda e: prepare_continue_queue(ctx))
    await ctx.send(session.q.current_music_thumb)
    await ctx.send(f"::Now playing:: {session.q.current_music.title}")


@lad_bot.command(name='play', help='queues up a track from youtube search')
async def play(ctx, *, arg):
    """
    :description: Checks where cmd author is, searches for song, joins channel and plays audio from youtube.
    :param ctx: discord.ext.commands.Context
    :param arg: str | either a URL or a search query
    :return: None
    """
    try:
        voice_channel = ctx.author.voice.channel

    # If author isn't in a voice channel, return.
    except AttributeError as e:
        print(e)
        await ctx.send("you aint in a fuckin' channel bro")
        return

    # find author's session
    session = check_session(ctx)

    # searches for audio
    with youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ytdler:
        try:
            requests.get(arg)
        except Exception as e:
            print(e)
            info = ytdler.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        else:
            info = ytdler.extract_info(arg, download=False)
    url = info['formats'][0]['url']
    thumb = info['thumbnails'][0]['url']
    title = info['title']

    session.q.enqueue(title, url, thumb)

    # find voice client for lad_bot
    voice = discord.utils.get(lad_bot.voice_clients, guild=ctx.guild)
    if not voice:
        await voice_channel.connect()
        voice = discord.utils.get(lad_bot.voice_clients, guild=ctx.guild)
    # If already playing something add to queue instead
    if voice.is_playing():
        await ctx.send(thumb)
        await ctx.send(f"Added to queue: {title}")
    else:
        await ctx.send(thumb)
        await ctx.send(f"Playing now: {title}")

        # Guarantees requested music is current music
    session.q.set_last_as_current()

    source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_PREFERENCE)
    voice.play(source, after=lambda ee: prepare_continue_queue(ctx))


@lad_bot.command(name='next', aliases=['skip'], help="skips current track")
async def skip(ctx):
    """
    :desc: Skips the current song, plays next in queue if any.
    :param ctx: discord.ext.commands.Context
    :return: None
    """
    # Finds author session
    session = check_session(ctx)
    # if none in queue, return
    if not session.q.theres_next():
        await ctx.send("Nothing in queue friend")
        return

    # finds available voice client for lad_bot
    voice = discord.utils.get(lad_bot.voice_clients, guild=session.guild)

    if voice.is_playing():
        voice.stop()
        return
    else:
        session.q.next()
        source = await discord.FFmpegOpusAudio.from_probe(session.q.current_music.url, **FFMPEG_PREFERENCE)
        voice.play(source, after=lambda e: prepare_continue_queue(ctx))
        return


@lad_bot.command(name='printq', aliases=['qlist'], help="tells you what's on queue and the sessionID")
async def print_queue(ctx):
    """
    :desc: A debug command to find session id, what is current playing and what is on the queue.
    :param ctx: discord.ext.commands.Context
    :return: None
    """

    session = check_session(ctx)
    await ctx.send(f"Session ID: {session.id}")
    await ctx.send(f"Current song title: {session.q.current_music.title}")
    queue = [q[0] for q in session.q.queue]
    await ctx.send(f"Queue: {queue}")


@lad_bot.command(name='leave', aliases=['kick', 'banish'], help="Kicks the bot from current voice channel if in one")
async def leave(ctx):
    """
    :desc: If bot is connected to a voice channel, it leaves it.
    :param ctx: discord.ext.commands.Context
    :return: None
    """
    voice = discord.utils.get(lad_bot.voice_clients, guild=ctx.guild)
    if voice.is_connected:
        check_session(ctx).q.clear_queue()
        await voice.disconnect()
    else:
        await ctx.send("lad_bot not connected, can't leave if not in a channel.")


@lad_bot.command(name='pause', help='pauses current track')
async def pause(ctx):
    """
    :desc: If playing audio, pause it.
    :param ctx: discord.ext.commands.Context
    :return: None
    """
    voice = discord.utils.get(lad_bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Nothing currently playing, can't pause")


@lad_bot.command(name='resume', aliases=['unpause', 'continue'], help="Resumes a paused track")
async def resume(ctx):
    """
    :desc: If audio is paused, resumes playing it.
    :param ctx: discord.ext.commands.Context
    :return: None
    """
    voice = discord.utils.get(lad_bot.voice_clients, guild=ctx.guild)
    if voice.is_paused:
        voice.resume()
    else:
        await ctx.send("Music is already paused")


@lad_bot.command(name='stop', aliases=['clear', 'end'], help="Stops current song and clears song queue")
async def stop(ctx):
    """
    :desc: Stops playing audio and clears the session's queue.
    :param ctx: discord.ext.commands.Context
    :return: None
    """
    session = check_session(ctx)
    voice = discord.utils.get(lad_bot.voice_clients, guild=ctx.guild)
    if voice.is_playing:
        voice.stop()
        session.q.clear_queue()
    else:
        await ctx.send("No longer playing music, queue has been cleared.")


# Runs lad_bot's loop.
lad_bot.run('OTkwMzk2MTEwMDk2OTczODQ0.Gg8LUK.jB96RvTr_h897R6-Z-eNtLnxjhgnpym8JKhoyo')

