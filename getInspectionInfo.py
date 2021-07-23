import discord
import datetime
import time
import pytz
import requests
from bs4 import BeautifulSoup as bs
from discord.ext import commands


def path():
    URL = 'http://api.maplestory.nexon.com/soap/maplestory.asmx'
    req = requests.get(URL)

    # 과부화 방지
    time.sleep(0.500)

    # 정보를 받아오지 못함
    if req.status_code != 200:
        embed = discord.Embed(title="메이플스토리 팅패치 정보",
                              description='정보를 받아오지 못했어요..',
                              timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0xff8000)
        return embed

    # soap api
    GetInspectionInfo = """<?xml version="1.0" encoding="utf-8"?>
                <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
                  <soap12:Body>
                    <GetInspectionInfo xmlns="https://api.maplestory.nexon.com/soap/" />
                  </soap12:Body>
                </soap12:Envelope>
                """

    headers = {'Content-Type': 'application/soap+xml'}
    req = requests.post(URL, data=GetInspectionInfo, headers=headers).text

    # bs
    soup_obj = bs(req, "html.parser")
    pathStart = soup_obj.select('startDateTime')[0].text

    pathEnd = soup_obj.select('endDateTime')[0].text
    pathContents = soup_obj.select('strObstacleContents')[0].text

    # output
    embed = discord.Embed(title="메이플스토리 팅패치 정보",
                          description=f'`최근 예정된 팅패치 정보입니다.`\n '
                                      f'시작 시간 : **{pathStart}**\n'
                                      f'종료 시간 : **{pathEnd}**\n'
                                      f'점검 내용 : **{pathContents}**',
                          timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0xff8000)

    return embed


class Base(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.command(name="메이플패치")
    async def 메이플패치(self, ctx):
        await ctx.send(embed=path())
        
    @commands.command(name="팅패")
    async def 팅패(self, ctx):
        await ctx.send(embed=path())
        
    @commands.command(name="팅패치")
    async def 팅패치(self, ctx):
        await ctx.send(embed=path())
        
    @commands.command(name="메이플팅패치")
    async def 메이플팅패치(self, ctx):
        await ctx.send(embed=path())


def setup(app):
    app.add_cog(Base(app))
