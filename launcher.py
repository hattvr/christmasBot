import configparser
import discord, os, time, pymongo, json, sys, traceback, aioredis
from colorama import Fore, init
from github import Github
from aiohttp import ClientSession
from discord.ext import commands
from configparser import ConfigParser


# Read config file and grab discord tokens
config = ConfigParser()
config.read('config.ini')
token = config.get('data', 'token')

class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = ".", 
            intents = discord.Intents.all(), 
            owner_ids = {188109365671100416, 738362958253522976}
        )
        self.db = pymongo.MongoClient().christmas
        self.session: ClientSession

    async def on_ready(self):
        print(f"[{Fore.GREEN}!{Fore.RESET}] Bot has started successfully!")

        self.session = ClientSession(loop=self.loop)
        self.redis = aioredis.from_url("redis://localhost")

        await self.load_extension("jishaku")
        await self.load_modules()

        # commands = await self.tree.sync()
        # updated = {}
        # for command in commands:
        #     updated.update({command.name:command.id})
            
        # with open('application_commands.json', 'w') as f:
        #     json.dump(updated, f, indent=4)
        
        await self.change_presence(
            status=discord.Status.online, 
            activity=discord.Activity(
                type=discord.ActivityType.listening, 
                name='ho ho ho!'
            )
        )
    
    @property
    def application_commands(self):
        with open('application_commands.json') as cmds:
            return json.load(cmds)

    async def is_owner(self, user):
        return user.id in self.owner_ids
        
    async def load_modules(self):
        for path, subdirs, files in os.walk("modules"):
            for name in files:
                if name.endswith(".py"):
                    name = os.path.join(name)[:-3]
                    path = (os.path.join(path).replace("/", ".")).replace("\\", ".")
                    filepath = path + "." + name
                    try:
                        await self.load_extension(filepath)
                        print(f"{Fore.LIGHTGREEN_EX}Loaded:{Fore.RESET} " + filepath)
                    except:
                        print(f"{Fore.RED}Error:{Fore.RESET} {filepath}\n" + traceback.format_exc())
                else:
                    continue
        
init()
Client().run(token)
