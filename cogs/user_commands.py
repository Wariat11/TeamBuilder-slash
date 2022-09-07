from discord.ext import commands
import re
from datetime import datetime
from cogs.embeds import DisplayEmbed
from cogs.handle_db import  HandlingDatabase as db
from discord import Option
from discord import Embed
import discord
import sqlite3

class UserCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    async def get_classes(self,ctx: discord.AutocompleteContext):
        conn = sqlite3.connect(f"databases//{ctx.interaction.guild.name} - {str(ctx.interaction.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT class FROM Classes")
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return sorted([i[0] for i in rows if i[0].startswith(ctx.value.title())])


#----------------------------------------------------------------------------------------------------------------------------------------------------


    @commands.guild_only()
    @commands.slash_command(name='party',description='Check if the party exists')
    async def party(self,ctx):
        try: #if id_channel exist in DB
            await ctx.respond("Actual group")
            await DisplayEmbed(self.bot).embed(self,ctx)
        except:
            await ctx.respond("`Party not exists`",delete_after=10)
      
      

#----------------------------------------------------------------------------------------------------------------------------------------------------



    @commands.guild_only()
    @commands.slash_command(name = 'organize',description='Organize the party')
    async def organize_party(self,ctx, 
                             name:Option(str,"Name of party"),
                             date:Option(str,"Date `00.00.0000`"),
                             time:Option(str,"Time 00:00")):
        try:
            pattern_date = re.match("(\d{2}.\d{2}.\d{4})",date)[0]
            pattern_time = re.match("(\d{2}.\d{2})",time)[0]
            
            party_date = datetime.strptime(pattern_date, '%d.%m.%Y').date()
            party_time = datetime.strptime(pattern_time, '%H:%M').time()
            party_date = party_date.strftime("%d.%m.%Y")
            party_time = party_time.strftime("%H:%M")
        except:
            await ctx.respond('Something went wrong. Check if the `date and time are correct.`',delete_after=10)
            return
        try:
            if str(ctx.channel.id) in [i[1] for i in await db.check_channels(self,ctx)]:
                await db.add_table(self,ctx)
                await db.add_date_time(self,ctx,name,str(party_date),party_time)
                await ctx.respond(f"@everyone **`{name}`** has been created.")
                await DisplayEmbed(self.bot).embed(self,ctx)
                return
            else:    
                await ctx.respond("`Channel not exist in channel list... Check !channels`",delete_after=10)
        except:
            await ctx.respond("Group already exists... Check `/party`",delete_after=10)
            
  
 
 
#----------------------------------------------------------------------------------------------------------------------------------------------------


    @commands.guild_only()
    @commands.slash_command(name = 'add',description = "Add member to group.")
    async def add_user(self,ctx,
                    name:Option(str,"User name",required=True),
                    role:Option(str,"User role",required=False,choices = ["LEECH","HEALER","MAGICIAN","SUPPORT","TANK","DPS"]),
                    _class:Option(str,"User class",required=False, autocomplete=get_classes)):
        list_of_names = [name[1] for name in await db.check_party(self,ctx)]
        id_list = [id[0] for id in await db.check_party(self,ctx)]
        organize_person = [i[3] for i in await db.get_date_time(self,ctx)][0]
        if role != None:
            role = role.upper()
        if _class != None:
            _class = _class.title()
        if name in list_of_names:
            await ctx.respond(f'`{name}` already exist in group',delete_after=10)
            return
        if ctx.author.mention == organize_person or ctx.author.guild_permissions.administrator == True:
            if name not in list_of_names:
                await db.add_user(self,ctx,name,role,_class)
                await DisplayEmbed(self.bot).embed(self,ctx)
                await ctx.respond(f"Added {name}")
                return
        else:
            if str(ctx.author.id) not in id_list and name not in list_of_names:
                await db.add_user(self,ctx,name,role,_class)
                await DisplayEmbed(self.bot).embed(self,ctx)
                await ctx.respond(f"Added `{name}`",delete_after=10)
                return
            else:
                await ctx.respond("You already add member",delete_after=10)
                return

 
 
#----------------------------------------------------------------------------------------------------------------------------------------------------

 
        
    @commands.guild_only()
    @commands.slash_command(name = 'remove',description = "Remove member from group.")
    async def remove_user(self,ctx,name:Option(str,"User name",required=True)):
        try:
            organize_person = [i[3] for i in await db.get_date_time(self,ctx)][0]
            for index in await db.check_party(self,ctx):
                if name in index:
                    if str(ctx.author.id) in index or organize_person == ctx.author.mention or ctx.author.guild_permissions.administrator:
                        await db.remove_user(self,ctx,name)
                        await DisplayEmbed(self.bot).embed(self,ctx)
                        await ctx.respond(f"`{name}` removed from group")
                        return
                    else:
                        await ctx.respond('You are not allowed to remove user. You can only remove yourself from group.',delete_after=10)
                        return
            await ctx.respond(f'`{name}` not exists in group',delete_after=10)
        except:
            await ctx.respond("`Party not exists`",delete_after=10)
                
                

#----------------------------------------------------------------------------------------------------------------------------------------------------


    @commands.guild_only()
    @commands.slash_command(name = "update_class",description = "Update a class")
    async def update_class(self, ctx,
                           name:Option(str,"name",required=True,),
                           _class:Option(str,"Class",required=True)):
        try:
            organize_person = [i[3] for i in await db.get_date_time(self,ctx)][0]
            for index in await db.check_party(self,ctx):
                if name in index:
                    if str(ctx.author.id) in index or organize_person == ctx.author.mention or ctx.author.guild_permissions.administrator:
                        await db.update_class_user(self,ctx,name,_class.title())
                        await DisplayEmbed(self.bot).embed(self,ctx)
                        await ctx.respond(f"`{name}` class updated to {_class}")
                        return
                    else:
                        await ctx.respond('You are not allowed to update member. You can only update your class.',delete_after=2)
                        return
            await ctx.respond(f"`{name}` not exists in group",delete_after=10)
        except:
            await ctx.respond("`Party not exists`",delete_after=10)
                

#----------------------------------------------------------------------------------------------------------------------------------------------------


    @commands.guild_only()
    @commands.slash_command(name = "update_role",description = "Update a role")
    async def update_role(self, ctx,
                           name:Option(str,"name",required=True,),
                           role:Option(str,"Class",required=True,choices = ["LEECH","HEALER","MAGICIAN","SUPPORT","TANK","DPS"])):
        try:
            organize_person = [i[3] for i in await db.get_date_time(self,ctx)][0]
            for index in await db.check_party(self,ctx):
                if name in index:
                    if str(ctx.author.id) in index or organize_person == ctx.author.mention or ctx.author.guild_permissions.administrator:
                        await db.update_role_user(self,ctx,name,role.upper())
                        await DisplayEmbed(self.bot).embed(self,ctx)
                        await ctx.respond(f"`{name}` role updated to {role}")
                        return
                    else:
                        await ctx.respond('You are not allowed to update member. You can only update your role.',delete_after=60)
                        return
            await ctx.respond(f"`{name}` not exists in group",delete_after=10)
        except:
            await ctx.respond("`Party not exists`",delete_after=10)


#----------------------------------------------------------------------------------------------------------------------------------------------------
              


    @commands.guild_only()
    @commands.slash_command(description='description')
    async def add_description(self,ctx,text:Option(str,"Description",required=True)):
        try:
            organize_person = [i[3] for i in await db.get_date_time(self,ctx)][0]
            if organize_person == ctx.author.mention or ctx.author.guild_permissions.administrator:
                await db.add_description_user(self,ctx,text,organize_person)
                await DisplayEmbed(self.bot).embed(self,ctx)
                await ctx.respond(f"Description added successfully.")
            else:
                await ctx.respond("You are not allowed to add description.",delete_after=10)
        except:
            await ctx.respond("`Party not exists`",delete_after=10)
        
        

#----------------------------------------------------------------------------------------------------------------------------------------------------
    


    @commands.guild_only()
    @commands.slash_command(description='Remove description')
    async def remove_description(self,ctx):
        try:
            organize_person = [i[3] for i in await db.get_date_time(self,ctx)][0]
            if ctx.author.mention == organize_person or ctx.author.guild_permissions.administrator:
                await db.remove_description_user(self,ctx,organize_person)
                await DisplayEmbed(self.bot).embed(self,ctx)
                await ctx.respond(f"Description removed successfully.")
            else:
                await ctx.respond("You are not allowed to add description.",delete_after=10)
        except:
            await ctx.respond("`Party not exists`",delete_after=10)
            
            
            
#----------------------------------------------------------------------------------------------------------------------------------------------------            
            
            
            
    @commands.guild_only()
    @commands.slash_command(name = "delete", description='Delete party')
    async def delete_party(self, ctx):
        try:
            organize_person = [i[3] for i in await db.get_date_time(self,ctx)][0]
            if ctx.author.mention == organize_person or ctx.author.guild_permissions.administrator:
                await db.delete_party_user(self,ctx)
                await ctx.respond(f"Party deleted successfully")
            else:
                await ctx.respond("You are not allowed to delete group.",delete_after=10)
        except:
            await ctx.respond("`Party not exists`",delete_after=10)

        
        
#----------------------------------------------------------------------------------------------------------------------------------------------------            
    

        
    @commands.guild_only()   
    @commands.slash_command(name = "channels" ,description = "Check available channels")
    async def channels(self,ctx):
        try: #if id_channel exist in DB
            channels = [index[0] for index in await db.check_channels(self,ctx)]
            channels_full = [i for i in await db.check_channels(self,ctx)]
            channels_name = "\n".join(channels)
            a = {}
            for i in channels_full:
                a[i[0]] = i[1]
            channels_admin = ""
            for i in channels_full:
                channels_admin += f"{i[0]} : {i[1]}\n"
            embed = Embed(
                title = 'Avaliable channels to create party',
                color = 0x009ef7
            )
            embed.add_field(name=":page_facing_up: Channels name:",value=f"`{channels_name}`",inline=False)
            embed.set_footer(text = f'Used by {ctx.author.name}\nThis message will be deleted in 60s',icon_url= "https://cdn-icons.flaticon.com/png/512/954/premium/954591.png?token=exp=1656187185~hmac=abdad1d243fadf49e9daaccc2c72d2a5")
            await ctx.respond(embed=embed,delete_after=60)
        except:
            await ctx.respond("There is no channel available",delete_after=10)          
        
        
        
def setup(bot):
    bot.add_cog(UserCommands(bot))
