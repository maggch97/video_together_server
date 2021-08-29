import time
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from typing import Optional, Any
import json

app = FastAPI()


class Play(BaseModel):
    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        __pydantic_self__.lastUpdateTime = time.time()

    lastUpdateTime: Optional[int]
    originalCurrent: Optional[int]
    playbackRate: Optional[float] = 1


class Viedo(BaseModel):
    link: Optional[str]


class Room(BaseModel):
    id: Optional[str]
    password: Optional[str]
    play: Optional[Play] = Play()
    video: Optional[Viedo] = Viedo()
    serverTime: Optional[int]


database = {}


@app.put('/room/{room_id}')
def roomUpdate(room_id: str, room: Room):
    database[room_id] = room
    return room


@app.get('/room/{room_id}')
def roomGet(room_id: str):
    database[room_id].serverTime = time.time()
    return database[room_id]


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8080, workers=1)
