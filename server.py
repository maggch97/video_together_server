import enum
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
        if __pydantic_self__.lastUpdateTime is None:
            __pydantic_self__.lastUpdateTime = time.time()

    lastUpdateTime: Optional[float]
    originalCurrent: Optional[int]
    playbackRate: Optional[float] = 1
    paused: Optional[bool]


class Viedo(BaseModel):
    link: Optional[str]


class Role(enum.Enum):
    MASTER = 1
    GREEN = 2


class RoomMeta(BaseModel):
    id: Optional[str]
    password: Optional[str]


class Room(BaseModel):
    meta: RoomMeta
    play: Optional[Play] = Play()
    video: Optional[Viedo] = Viedo()
    serverTime: Optional[int]

    def PermissionCheck(self, role: Role, password: str):
        if role == Role.MASTER:
            if password != self.meta.password:
                return False
        print(password, self.meta.password)
        return True


class Response(BaseModel):
    errCode: int
    errMsg: str
    data: Optional[Any]

    @staticmethod
    def Error(errCode: int, errMsg: str):
        resp = Response(errCode=errCode, errMsg=errMsg)
        return resp

    @ staticmethod
    def Ok(data: Any):
        resp = Response(errCode=0, errMsg="ok")
        resp.data = data
        return resp


database = dict()


@ app.put('/room/{room_id}')
def roomUpdate(room_id: str, room: Room):
    if room_id in database:
        if database[room_id].PermissionCheck(Role.MASTER, room.meta.password) is not True:
            return Response.Error(1, "房间已存在，密码错误")
    # print(room_id, room, database[room_id])
    database[room_id] = room
    # print(room_id, room, database[room_id])
    return Response.Ok(room)


@ app.get('/room/{room_id}')
def roomGet(room_id: str):
    if room_id not in database:
        return Response.Error(2, "房间不存在")
    database[room_id].serverTime = time.time()
    return Response.Ok(database[room_id])


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8080, workers=1)
