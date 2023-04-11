import discord
import re
from .song import Song
from .music_bot import add_to_queue
from pytimeparse.timeparse import timeparse
from .utils import SP, NotFoundSongException, Source, YDL_OPTS

from youtubesearchpython import VideosSearch
import yt_dlp

async def define_source(msg : discord.Message, bot : discord.Bot):
    url = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', msg.content)

    if url != []:
        spotify = re.search(r'spotify.com/track', url[0])
        youtube = re.search(r'youtu', url[0])
        #sp_playlist = re.search(r'spotify.com/playlist', url[0])

        if spotify is not None:
            track = SP.track(url[0])
            if track == None:
                raise NotFoundSongException(Source.Spotify)
            
            song = search_on_YT(f"""{track["name"]} {track['artists'][0]['name']}""", track["duration_ms"] // 1000, Source.Spotify)
            await add_to_queue(msg.guild, song, msg.author, bot)
        
        elif youtube is not None:
            with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
                video = ydl.extract_info(url[0], download=False)
            
                if video == None:
                    raise NotFoundSongException(Source.YouTube)
            
            song = Song(video['title'], url[0], video["duration"], video["live_status"]=="is_live")
            await add_to_queue(msg.guild, song, msg.author, bot)
        
        #elif sp_playlist is not None:
        #    if await self.searchplaylist(url[0], msg) != []:
        #        return await self.searchplaylist(url[0], msg)
            


    else:
        spotifytrack = re.search(r'spotify:track:[^\s<>"]+', msg.content)
        #spotifyuri = re.search(r'spotify:(playlist):[^\s<>"]+', msg.content)
        if spotifytrack is not None:
            track = SP.track(spotifytrack[0])
            if track == None:
                raise NotFoundSongException(Source.Spotify)
            
            song = search_on_YT(f"""{track["name"]} {track['artists'][0]['name']}""", track["duration_ms"] // 1000, Source.Spotify)
            await add_to_queue(msg.guild, song, msg.author, bot)
        
        #elif spotifyuri is not None:
        #    if await self.searchplaylist(spotifyuri[0], msg) != []:
        #        return await self.searchplaylist(spotifyuri[0], msg)

        else:
            
            song = get_linkYT(msg.content, Source.YouTube)
            
            await add_to_queue(msg.guild, song, msg.author, bot)  

def search_on_YT(name : str, duration : int, source : Source) -> Song:
    search_results = VideosSearch(name, limit=5)
    results = search_results.result()['result']
    if results == []:
        raise NotFoundSongException(Source.YouTube)
    times = []
    for result in results:
        time_str = result["duration"]
        times.append(timeparse(time_str))
    index=times.index(min(times, key = lambda x: abs(duration - x)))
    url = results[index]['link']
    time=times[index]
    song = Song(name=name, url=url, duration=time, source=source)
    return song

def get_linkYT(name : str, source : Source) -> (str | None):
    search_results = VideosSearch(name, limit=1)
    result = search_results.result()['result']
    if result == []:
        raise NotFoundSongException(Source.YouTube)
    raw_url = result[0]
    time = 0
    if raw_url['duration'] is not None:
        time = timeparse(raw_url['duration'])

    song = Song(raw_url["title"], raw_url["link"], time, source, raw_url['duration'] is None)
    return song

#async def searchplaylist(self, uri, msg : discord.Message):
#    playlist = sp.playlist_tracks(uri)
#    not_founded = []
#    queue = MusicBot(msg.guild.id).queue
#    if playlist == None:
#        raise SpotifyWithoutRequest("No playlist found")
#    for song in playlist['items'][0 : (20 - len(queue))]:
#        name = f"""{song['track']['name']} {song['track']['artists'][0]['name']}"""
#        duration = int(song['track']['duration_ms']//1000)
#        link = self.get_linkYT(msg, False, {"title" : name, "time" : duration})
#        if link != None:
#            await self.add_to_queue(msg, link, "Spotify")
#        else:
#            not_founded.append(name)
#    if not_founded != []:
#        return not_founded