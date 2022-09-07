from discord.ext import commands
from discord import Embed
from discord.ext.commands import MissingPermissions
from cogs.handle_db import HandlingDatabase as db


class HelpCommand(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
        
    @commands.guild_only()
    @commands.slash_command(name = 'help',description='Help command.')
    async def help(self,ctx):
        embed = Embed(
            title = "Helpdesk\nAvailable commands:",
            description = """Server administrator and group organizer can add, modify, remove users from group and also delete group.
Every user which isn't a organizer or administrator can only add one record to group and also can modify it.
It's possible to create only one group on channel.""",
            color = 0x009ef7
        )
        embed.add_field(name = 'Commands with permission', value = '**/admin_help**',inline=False)
        embed.add_field(name = 'Commands for user', value = """**/help**
**/party** (Check available party if exists)
**/channels** (Check available channels which where can create group)
**/classes** (Check available classes)
**/organize** `group_name` `date(00.00.0000)` `time(00:00)` 
(at group name it possible add :icon:)
**/add** `name` `role` `class` (Adding user to group with class and role. It possible to add only with class )
**/update_class** `name` `class` (Updating user class)
**/update_role** `name` `role` (Updating user role)
**/add_description** `description` (Adding description to group information)
**/remove_description**
**/remove** `name` (Removing from group)
**/delete** (only !delete, be careful deleting instantly)""",inline=False)
        embed.set_footer(text = f"Used by {ctx.author.name}\nThis message will be deleted in 60s",icon_url='https://cdn-icons-png.flaticon.com/512/751/751381.png')
        await ctx.respond(embed=embed,delete_after = 60)
        
#--------------------------------------------------------------------------------------------------------------------------------------------------------      

    @commands.guild_only()
    @commands.has_permissions(administrator=True)  
    @commands.slash_command(name = "help_admin",description='Help command for administrator.')
    async def help_admin(self,ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You have not permission to use this command",delete_after=2)
            return
        embed = Embed(
            title = "Administrator Helpdesk\nAvailable commands:",
            description = """Special commands for administrator to add and modify class and channels for possibilities create team""",
            color = 0x009ef7
        )
        embed.add_field(name = 'Commands for administrator', value = """/admin_help
/add_channel `channel_id`
/remove_channel `channel_id`
/add_class `class_name` `:icon:`
/remove_class `class_name`""",inline=False)
        embed.set_footer(text = f"Used by {ctx.author.name}\nThis message will be deleted in 60s",icon_url='https://cdn-icons-png.flaticon.com/512/751/751381.png')
        await ctx.author.send(embed=embed,delete_after = 60)
        await ctx.respond("Admin help command")
        
        
        
#--------------------------------------------------------------------------------------------------------------------------------------------------------      
        

    @commands.guild_only()
    @commands.slash_command(name = 'classes',description='Check available classes.')  
    async def classes(self,ctx):
        embed = Embed(
            title = "Available classes:",
            color = 0x009ef7
        )
        embed.add_field(name = '** **', value = '-----------------------------------------------------------------------------------',inline=False)
        for i in await db.check_classes(ctx):
            embed.add_field(name = f"{i[1]} - {i[0]}",value='** **',inline=True)
        embed.set_footer(text = f"Used by {ctx.author.name}",icon_url='https://cdn-icons-png.flaticon.com/512/751/751381.png')
        await ctx.respond(embed=embed)
        
def setup(bot):
    bot.add_cog(HelpCommand(bot))
