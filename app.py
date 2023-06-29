from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from mxm import MXM
import asyncio

mxm = MXM()

class SpIds(BaseModel):
    ids: List[str]

class Track(BaseModel):
    track: Dict

class Tracks(BaseModel):
    tracks: List[Dict]


app = FastAPI()

@app.get('/api/match_id', response_model=Tracks)
async def matcher_tracks(data: SpIds):
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
    uvicorn.run("app:app", host="0.0.0.0", port=port)