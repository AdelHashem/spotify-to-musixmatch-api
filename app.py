from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from mxm import MXM

mxm = MXM()

class SpIds(BaseModel):
    ids: List[str]

class Track(BaseModel):
    track: Dict

class Tracks(BaseModel):
    tracks: List[Track]


app = FastAPI()

@app.get('/api/match_id', response_model=Tracks)
async def matcher_tracks(data: SpIds):
    tracks = await mxm.matcher_tracks_get(data.ids)
    return Tracks(tracks=tracks)