from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from mxm import MXM
import asyncio
import aiohttp


class StartAiohttp:
    session = None
    def __init__(self,limit, limit_per_host) -> None:
        self.limit = limit
        self.limit_per_host = limit_per_host
        

    def start_session(self):
        if self.session is None:
            connector = aiohttp.TCPConnector(limit=self.limit, limit_per_host=self.limit_per_host)
            self.session = aiohttp.ClientSession(connector=connector)

    def get_session(self):
        return self.session


    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None

client = StartAiohttp(5,5)


async def on_startup() -> None:
    client.start_session()

async def on_shutdown() -> None:
    await client.close_session()

app = FastAPI(on_startup=[on_startup],on_shutdown=[on_shutdown])


class SpIds(BaseModel):
    ids: List[str]

class Track(BaseModel):
    track: Dict

class Tracks(BaseModel):
    tracks: List[Dict]




@app.get('/api/match_id', response_model=Tracks)
async def matcher_tracks(data: SpIds):
    client.start_session()
    mxm = MXM(session=client.get_session())
    coro = [mxm.matcher_track(id) for id in data.ids]
    tasks = [asyncio.create_task(c) for c in coro]
    tracks = await asyncio.gather(*tasks)
    #return tracks
    #tracks = await mxm.matcher_tracks_get(data.ids)
    return Tracks(tracks=tracks)

import uvicorn
from os import getenv

if __name__ == "__main__":
    port = int(getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload= True)