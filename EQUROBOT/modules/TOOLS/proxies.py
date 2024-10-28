import asyncio
import aiohttp
import itertools
from pyrogram import filters
from config import LOGGER_ID, OWNER_ID
from EQUROBOT import app

class ProxyManager:
    def __init__(self):

        self.proxy_list = [
                "purevpn0s4931691:jm3s6om1bfbd@prox-ae.pointtoserver.com:10799",
                "tickets:proxyon145@162.212.170.77:12345",
                "purevpn0s607365:5whkx7x6o7c1@prox-au.pointtoserver.com:10799",
                "tickets:proxyon145@161.0.1.13:12345",
                "purevpn0s4931691:jm3s6om1bfbd@prox-fi.pointtoserver.com:10799",
                "tickets:proxyon145@23.94.251.13:12345",
                "purevpn0s4931691:jm3s6om1bfbd@prox-vn.pointtoserver.com:10799",
                "purevpn0s607365:5whkx7x6o7c1@prox-bh.pointtoserver.com:10799",
                "purevpn0s4931691:jm3s6om1bfbd@prox-sg.pointtoserver.com:10799",
                "purevpn0s607365:5whkx7x6o7c1@prox-ae.pointtoserver.com:10799",
                "purevpn0s607365:5whkx7x6o7c1@prox-sg.pointtoserver.com:10799",
                "purevpn0s607365:5whkx7x6o7c1@prox-eg.pointtoserver.com:10799",
                "purevpn0s4931691:jm3s6om1bfbd@prox-ng.pointtoserver.com:10799",
                "tickets:proxyon145@107.172.170.115:12345"
            ]

        self.alive_proxies = []
        self.proxy_pool = None
        self.initialization_done = asyncio.Event()
        asyncio.create_task(self.initialize_proxy_pool())

    async def send_logger_message(self, message_text):
        try:
            await app.send_message(chat_id=LOGGER_ID, text=message_text)
        except Exception as e:
            print(f"Error sending log message: {e}")

    async def check_proxy(self, proxy):
        url = "http://httpbin.org/ip"
        try:

            if "@" in proxy:
                auth_part, addr_part = proxy.split("@")
                username, password = auth_part.split(":", 1)
                ip, port = addr_part.split(":")
                proxy_auth = aiohttp.BasicAuth(username, password)
                proxy_url = f"http://{ip}:{port}"
            else:

                proxy_auth = None
                proxy_url = f"http://{proxy}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy=proxy_url, proxy_auth=proxy_auth, timeout=5) as response:
                    if response.status == 200:
                        return proxy, "Live ✅"
                    else:
                        return proxy, "Dead ❌"
        except (ValueError, aiohttp.ClientError, asyncio.TimeoutError):
            return proxy, "Dead ❌"

    async def get_alive_proxies(self):
        tasks = [self.check_proxy(proxy) for proxy in self.proxy_list]
        results = await asyncio.gather(*tasks)
        alive_proxies = [proxy for proxy, status in results if status == "Live ✅"]
        return alive_proxies

    async def initialize_proxy_pool(self):
        self.alive_proxies = await self.get_alive_proxies()
        if not self.alive_proxies:
            await self.send_logger_message("No proxies available after initialization!")
            raise Exception("No proxies available")
        self.proxy_pool = itertools.cycle(self.alive_proxies)
        if len(self.alive_proxies) < 5:
            warning_message = f"Warning: Only {len(self.alive_proxies)} proxies left alive!"
            await self.send_logger_message(warning_message)
        self.initialization_done.set()

    async def get_proxy(self):
        await self.initialization_done.wait()
        if not self.alive_proxies:
            raise Exception("No proxies available")
        proxy = next(self.proxy_pool)
        return self.format_proxy(proxy)

    def format_proxy(self, proxy):
        if "@" in proxy:
            auth_part, addr_part = proxy.split("@")
            return f"http://{auth_part}@{addr_part}"
        else:
            return f"http://{proxy}"

    async def refresh_proxies(self):
        self.alive_proxies = await self.get_alive_proxies()
        if len(self.alive_proxies) < 5:
            warning_message = f"Warning: Only {len(self.alive_proxies)} proxies left alive!"
            await self.send_logger_message(warning_message)
        self.proxy_pool = itertools.cycle(self.alive_proxies)

    async def set_proxy_list(self, new_proxy_list):
        self.proxy_list = new_proxy_list
        self.initialization_done.clear()
        await self.initialize_proxy_pool()

    def remove_proxy_list(self):
        self.proxy_list = []
        self.alive_proxies = []
        self.proxy_pool = None

proxy_manager = ProxyManager()

async def proxies():
    return await proxy_manager.get_proxy()

def proxies_sync():
    try:
        loop = asyncio.get_running_loop()

        raise RuntimeError("Cannot use proxies_sync() when the event loop is running. Use 'await proxies()' instead.")
    except RuntimeError:

        return asyncio.run(proxy_manager.get_proxy())

@app.on_message(filters.command("setproxy", prefixes=["/", ".", "!"]))
async def set_proxy(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply("You are not authorized to set the proxy list.")
        return

    try:
        new_proxy_data = message.text.split(' ', 1)[1]

        new_proxy_list = [line.strip() for line in new_proxy_data.strip().replace(',', '\n').split('\n') if line.strip()]
        await proxy_manager.set_proxy_list(new_proxy_list)
        await message.reply("Proxy list has been set successfully.")
        await proxy_manager.send_logger_message(f"Proxy list set by {message.from_user.id}")
    except IndexError:
        await message.reply("Please provide a valid proxy list after the command. Example:\n/setproxy username:password@ip:port\nusername:password@ip:port\n...")
    except Exception as e:
        await message.reply(f"Failed to set proxy list: {str(e)}")

@app.on_message(filters.command("removeproxy", prefixes=["/", ".", "!"]))
async def remove_proxy(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply("You are not authorized to remove the proxy list.")
        return

    if proxy_manager.proxy_list:
        proxy_manager.remove_proxy_list()
        await message.reply("Proxy list has been removed.")
        await proxy_manager.send_logger_message(f"Proxy list removed by {message.from_user.id}")
    else:
        await message.reply("No proxy list was set.")

@app.on_message(filters.command("viewproxy", prefixes=["/", ".", "!"]))
async def view_proxy(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply("You are not authorized to view the proxy list.")
        return

    if not proxy_manager.proxy_list:
        await message.reply("No proxy list has been set.")
        return

    proxy_list_str = "\n".join(proxy_manager.proxy_list)
    await message.reply(f"Current Proxy List:\n{proxy_list_str}")
