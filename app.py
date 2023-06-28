from fastapi import FastAPI
from pydantic import BaseModel
from mxm import MXM

mxm = MXM()

class isrcs(BaseModel):
    data: dict

class SpIds(BaseModel):
    data: dict


class TrackItem(BaseModel):
    track: dict


class Tracks(BaseModel):
    tracks: list[TrackItem]




app = FastAPI()

@app.get('/api/match_id', response_model=Tracks)
async def matcher_tracks(data:SpIds) -> Tracks:
    print(data)
    tracks = await mxm.matcher_tracks_get(data.data["ids"])
    return {"tracks":tracks}
