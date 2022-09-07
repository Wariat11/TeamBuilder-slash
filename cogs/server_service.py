from http import server
from discord.ext import commands
import sqlite3
import os
import discord
from discord import Embed
from discord import File
from cogs.handle_db import HandlingDatabase as db



class ServerService(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.roles = ['DPS','TANK','MAGICIAN','SUPPORT','HEALER','LEECH','OTHER']


    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        conn = sqlite3.connect(f"databases//{guild.name} - {str(guild.id)}.db")
        await db.admin_add_table_roles(self,guild)
        await db.admin_add_table_class(self,guild)
        await db.admin_add_table_channel(self,guild)
        for index in self.roles:
            await db.admin_add_role(self,index,guild)
        await self.sendDm(self,f"Bot added to server `{guild.name} - {str(guild.id)}`")
        conn.close()
        async for entry in guild.audit_logs(action=discord.AuditLogAction.integration_create,limit=1):
            invite_user = await self.bot.fetch_user(entry.user.id)
        file = File('img/logo.png')
        embed = Embed(
        title = "Hi! I'm a Team Builder :office_worker: thanks for adding me on Your server ! ({})".format(guild.name),
        description = "Let's configure me in few steps",
        color = 0x009ef7)
        embed.add_field(name = '1. Adding channel to channel list', value = """/add_channel `channel_id` (click right button on channel and copy and paste ID)
                        Now channel is available to use my service. Check `/channels` on server""",inline=False)
        embed.add_field(name = "2. Add icon class (optional)", value = "/add_class `class_name` `:icon:`",inline=False)
        embed.set_thumbnail(url = "attachment://logo.png")
        await invite_user.send(file=file,embed=embed)
            
    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        if os.path.exists(f"databases//{guild.name} - {str(guild.id)}.db"):
            os.remove(f"databases//{guild.name} - {str(guild.id)}.db")
            print("Database deleted successfully")
        await self.sendDm(self,f"Bot removed from server `{guild.name} - {str(guild.id)}`")
            

    @commands.is_owner()    
    @commands.command()
    async def sendDm(self,ctx,info):
        admin = await self.bot.fetch_user(562603559670120458)
        return await admin.send(info)
    
def setup(bot):
    bot.add_cog(ServerService(bot))
