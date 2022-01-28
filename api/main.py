from typing import Optional
from fastapi import FastAPI, Request, status, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from config import *
import mysql.connector
from datetime import time


logas = FastAPI()

templates = Jinja2Templates(directory="channels")


@logas.get("/api/")
async def root(response: Response):
    response.status_code = status.HTTP_200_OK
    return {"message": "Hello World"}


@logas.get("/api/channels/{channel}")
async def watch_channel(request: Request, channel: str, response: Response):
    response.status_code = status.HTTP_200_OK
    return templates.TemplateResponse(channel, {"request": request})


@logas.get("/api/get_all_channels/")
async def get_all_channels(response: Response):

    def struct_channel(channels):
        return {
            'nom': channels[0],
            'lien': channels[1],
        }

    db = mysql.connector.connect(**database())
    cursor = db.cursor()

    cursor.execute("""
        SELECT nom, lien FROM Channel
    """)

    channel_data = list(map(struct_channel, cursor.fetchall()))
    db.close()

    if channel_data is not None :
        response.status_code = status.HTTP_200_OK
        return channel_data


@logas.get("/api/get_all_programs/")
async def get_all_programs(response: Response):

    def struct_program(programs):
        return {
            'jour': programs[0],
            'heure': str(programs[1]),
            'titre': programs[2],
            'chaine': programs[3],
            'statut': programs[4],
        }

    db = mysql.connector.connect(**database())
    cursor = db.cursor()

    cursor.execute("""
        SELECT jour, heure, titre, chaine, statut FROM Program
    """)

    program_data = list(map(struct_program, cursor.fetchall()))
    db.close()

    if program_data is not None :
        response.status_code = status.HTTP_200_OK
        return program_data


if __name__ == '__main__':
    uvicorn.run("main:logas", port=1806, host='0.0.0.0', workers=10, reload=True)