import warnings
import psutil
import base64
import aiohttp
import asyncio
import json

warnings.filterwarnings('ignore')

async def get_lcu(lcu_process='LeagueClientUx.exe'):
    riotclient_auth_token = None
    riotclient_app_port = None

    for p in psutil.process_iter():
        if p.name() == lcu_process:
            args = p.cmdline()
            for a in args:
                if '--riotclient-auth-token=' in a:
                    riotclient_auth_token = a.split('--riotclient-auth-token=', 1)[1]
                if '--riotclient-app-port=' in a:
                    riotclient_app_port = a.split('--riotclient-app-port=', 1)[1]
    
    if not riotclient_auth_token or not riotclient_app_port:
        raise ValueError("LCU process not found or doesn't have the required arguments.")

    riotclient_session_token = base64.b64encode(('riot:' + riotclient_auth_token).encode('ascii')).decode('ascii')
    return riotclient_session_token, riotclient_app_port

async def get_headers(riotclient_session_token):
    riotclient_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'LeagueOfLegendsClient',
        'Authorization': 'Basic ' + riotclient_session_token
    }
    return riotclient_headers

async def get_summoners(riotclient_app_port, riotclient_headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://127.0.0.1:{riotclient_app_port}/chat/v5/participants/champ-select',
                               headers=riotclient_headers, verify_ssl=False) as response:
            summoners = await response.text()
            summoners = json.loads(summoners)['participants']
            summoners = ",".join([summoner['game_name'] for summoner in summoners])
            return summoners

if __name__ == '__main__':
    riotclient_session_token, riotclient_app_port = asyncio.run(get_lcu())
    riotclient_headers = asyncio.run(get_headers(riotclient_session_token))
    summoners = asyncio.run(get_summoners(riotclient_app_port, riotclient_headers))
    