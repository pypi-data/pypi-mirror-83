import base64
import datetime
import xml.etree.ElementTree as ET

import requests


class AuthError(Exception):
    """
        認証失敗を知らせる例外クラス
    """
    pass


_authKey = b'bcd151073c03b352e1ef2fd66c32209da9ca0afa'

_URL_AUTH1 = 'https://radiko.jp/v2/api/auth1'
_URL_AUTH2 = 'https://radiko.jp/v2/api/auth2'
_URL_PROGRAM = 'https://radiko.jp/v3/program/date/{date}/{area}.xml'
_URL_GET_LIST = 'http://f-radiko.smartstream.ne.jp/{st}/_definst_/' \
                + 'simul-stream.stream/playlist.m3u8'


def get_partial_key(r):
    offset = int(r.headers["X-Radiko-KeyOffset"])
    length = int(r.headers["X-Radiko-KeyLength"])
    return base64.b64decode(_authKey[offset: offset + length])


def get_date(dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    if dt.hour < 5:
        dt -= datetime.timedelta(days=1)
    return dt.strftime("%Y%m%d")


class Client:

    def __init__(self):
        self.area = None
        self.headers = {
            'x-radiko-app': 'pc_html5',
            'x-radiko-app-version': '0.0.1',
            'x-radiko-user': 'dummy_user',
            'x-radiko-device': 'pc',
            'x-radiko-authtoken': '',
            'x-radiko-partialkey': '',
        }
        self.stations = []
        self.select = None

        r = requests.get(_URL_AUTH1, headers=self.headers)
        if r.status_code != 200:
            raise AuthError("認証1に失敗")
        self.headers["x-radiko-authtoken"] = r.headers["X-RADIKO-AUTHTOKEN"]
        self.headers["x-radiko-partialkey"] = get_partial_key(r)

        r = requests.get(_URL_AUTH2, headers=self.headers)
        if r.status_code != 200:
            raise AuthError("認証2に失敗")
        self.area = r.content.decode().split(',')[0]

    def get_stations(self):
        r = requests.get(_URL_PROGRAM.format(date=get_date(), area=self.area), header=self.headers)
        if r.status_code != 200:
            raise Exception("取得に失敗しました")
        x_program = ET.fromstring(r.content.decode())
        x_stations = x_program.find("stations").findall("station")
        for x_station in x_stations:
            self.stations.append(Station(x_station))


class Station:

    def __init__(self, x_station):
        self.progs = []
        self.id = x_station.attrib["id"]
        self.name = x_station.find("name").text
        self.load_programs(x_station.find("progs"))

    def load_programs(self, x_progs):
        for x_prog in x_progs:
            self.progs.append(Prog(x_prog))

    def get_on_air(self, dt=None):
        if dt is None:
            dt = datetime.datetime.now()
        for prg in self.progs:
            if prg.is_on_air(dt):
                return prg
        return None


class Prog:

    def __init__(self, x_prg):
        self.id = x_prg.attrib["id"]
        self.master_id = x_prg.attrib["master_id"]
        self.ft = datetime.datetime.strptime(x_prg.attrib["ft"][0:12], "%Y%m%d%H%M")
        self.to = datetime.datetime.strptime(x_prg.attrib["to"][0:12], "%Y%m%d%H%M")
        self.title = x_prg.find("title").text
        self.url = x_prg.find("url").text
        self.pfm = x_prg.find("pfm").text
        self.img = x_prg.find("img").text

    def is_on_air(self, dt=None):
        if dt is None:
            dt = datetime.datetime.now()
        return self.ft <= dt < self.to
