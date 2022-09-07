from discord.ext import commands
from discord import Option
from cogs.handle_db import  HandlingDatabase as db


class AdminCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
        
    @commands.guild_only()
    @commands.slash_command(name = 'add_channel',description='Add a channel to the channel list (COMMAND WITH PERMISSION).')
    async def add_channel(self,ctx,channel_id:Option(str,'Channel ID (Click right button on channel then copy and paste channel ID)')):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You have not permission to use this command",delete_after=10)
            return
        try:
            channel_name = self.bot.get_channel(int(channel_id))
            channel_list = [i[1] for i in await db.check_channels(self,ctx)]
            if channel_name != None:
                if channel_id in channel_list:
                    await ctx.respond(f"`{channel_name}` exist in channel list.",delete_after=10)
                    return
                await db.add_channel(self,ctx,channel_name,channel_id)
                await ctx.respond(f"`{channel_name}` added to channel list.",delete_after=10)
            else:
                await ctx.respond(f"Channel `{channel_id}` not exists.",delete_after=10)
        except:
            await ctx.respond(f"Channel `{channel_id}` not exists.",delete_after=10)


    @commands.guild_only()
    @commands.slash_command(name = 'remove_channel',description='Remove a channel from channel list (COMMAND WITH PERMISSION).')
    async def remove_channel(self,ctx,channel_id):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You have not permission to use this command",delete_after=2)
            return
        channel_list = [i[1] for i in await db.check_channels(self,ctx)]
        try:
            channel_name = await self.bot.fetch_channel(channel_id)
            if channel_id in channel_list:
                await db.delete_channel(self,ctx,channel_id)
                await ctx.respond(f"`{channel_name}` removed from channel list.",delete_after=2)
            else:
                await ctx.respond(f"`{channel_name}` not exist in channel list.",delete_after=2)  
        except:
            await ctx.respond(f"`{channel_id}` not exist in channel list.",delete_after=2)
            return
            

# --------------------------------------------------------------------------------------------------------------------------------------------------


    @commands.guild_only()
    @commands.slash_command(name = 'add_class',description='Add class to class list (COMMAND WITH PERMISSION).')
    async def add_class(self,ctx,
                        class_name:Option(str,"Class name"),
                        icon:Option(str,"Enter icon :icon:")):        
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You have not permission to use this command",delete_after=10)
            return
        class_name = class_name.title()
        class_list = [i[0] for i in await db.check_classes(self,ctx)]
        if class_name not in class_list:
            await db.add_class(self,ctx,class_name.title(),icon)
            await ctx.respond(f"`{class_name.title()}` added to class list.",delete_after=10)
        else:
            await ctx.respond(f"`{class_name.title()}` exist in class list.",delete_after=10)
            

# --------------------------------------------------------------------------------------------------------------------------------------------------


    @commands.guild_only()
    @commands.slash_command(name = 'remove_class',description='Remove class from class list (COMMAND WITH PERMISSION).')
    async def remove_class(self,ctx,
                        class_name:Option(str,"Class name")): 
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You have not permission to use this command",delete_after=10)
            return
        class_name = class_name.title()
        class_list = [i[0] for i in await db.check_classes(self,ctx)]
        if class_name in class_list:
            await db.remove_class(self,ctx,class_name.title())
            await ctx.respond(f"`{class_name.title()}` removed from class list.",delete_after=10)
        else:
            await ctx.respond(f"`{class_name.title()}` not exist in class list.",delete_after=10)
            


def setup(bot):
    bot.add_cog(AdminCommands(bot))
