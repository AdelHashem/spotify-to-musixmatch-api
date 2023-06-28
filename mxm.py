import os, re
import Asyncmxm
import asyncio


class MXM:
    BASE_URL = "http://api.musixmatch.com/ws/1.1/"
    DEFAULT_KEY = os.environ.get("MXM_API")
    DEFAULT_KEY2 = os.environ.get("MXM_API2")
    def __init__(self, key=None, session=None):
        self.key = key or self.DEFAULT_KEY
        self.key2 = self.DEFAULT_KEY2
        self.musixmatch = Asyncmxm.Musixmatch(self.key)
        self.musixmatch2 = Asyncmxm.Musixmatch(self.key)


    async def track_get(self, isrc = None, commontrack_id = None) -> dict:
        try:
            response = await self.musixmatch2.track_get(
                track_isrc=isrc, commontrack_id=commontrack_id
            )
            return response
        except Asyncmxm.exceptions.MXMException as e:
            if re.search("404", str(e)):
                return {"error:404"}
            else:
                return e
            

    async def matcher_track(self,sp_id = None,itunes_id = None):
        try:
            response = await self.musixmatch.matcher_track_get(
                q_track="null", track_spotify_id=sp_id
            )
            return response["message"]["body"]
        except Asyncmxm.exceptions.MXMException as e:
            if re.search("404", str(e)):
                return {"error": "The track hasn't been imported yet. Try one more time after 1-5 minutes (tried to import it using matcher call)."}
            return {"error": e}
        except Exception as e:
            return {"error": str(e)}
        
    async def Tracks_Data(self, iscrcs):
        tracks = []
        Limit = 5
        import_count = 0
        if "isrc" not in iscrcs[0]:
            return iscrcs
        
        coro = [self.track_get(isrc["isrc"]) for isrc in iscrcs]
        tasks = [asyncio.create_task(c) for c in coro]
        tracks = await asyncio.gather(*tasks)

        coro = [self.matcher_track(isrc["track"]["id"]) for isrc in iscrcs]
        tasks = [asyncio.create_task(c) for c in coro]
        matchers = await asyncio.gather(*tasks)

        return {"tracks": tracks, "matchers": matchers}


    async def matcher_tracks_get(self,ids:list) -> list:
        coro = [self.matcher_track(id) for id in ids]
        tasks = [asyncio.create_task(c) for c in coro]
        tracks = await asyncio.gather(*tasks)
        return tracks
