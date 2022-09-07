from discord.ext import commands
from discord import Embed
from cogs.handle_db import HandlingDatabase as db


class DisplayEmbed(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command() 
    async def embed(self,ctx):
        discord_classes = {}
        for row in await db.check_classes(self,ctx):
            discord_classes[row[0]] = row[1]
            
        dps = []
        tank = []
        magician = []
        healer = []
        support = []
        leech = []
        other = []
        
        for i in await db.check_party(self,ctx):
            if i[3] == "DPS":
                if discord_classes.get(i[2]) == None:
                    dps.append(f'{i[1]}')
                    continue
                dps.append(f'{discord_classes.get(i[2])} {i[1]}')
            elif i[3] == 'TANK':
                if discord_classes.get(i[2]) == None:
                    tank.append(f'{i[1]}')
                    continue
                tank.append(f'{discord_classes.get(i[2])} {i[1]}')
            elif i[3] == 'MAGICIAN':
                if discord_classes.get(i[2]) == None:
                    magician.append(f'{i[1]}')
                    continue
                magician.append(f'{discord_classes.get(i[2])} {i[1]}')
            elif i[3] == 'HEALER':
                if discord_classes.get(i[2]) == None:
                    healer.append(f'{i[1]}')
                    continue
                healer.append(f'{discord_classes.get(i[2])} {i[1]}')
            elif i[3] == 'SUPPORT':
                if discord_classes.get(i[2]) == None:
                    support.append(f'{i[1]}')
                    continue
                support.append(f'{discord_classes.get(i[2])} {i[1]}')
            elif i[3] == 'LEECH':
                if discord_classes.get(i[2]) == None:
                    leech.append(f'{i[1]}')
                    continue
                leech.append(f'{discord_classes.get(i[2])} {i[1]}')
            elif i[3] == 'OTHER' or i[3] not in [i[0] for i in await db.check_roles(self,ctx)] and i[3] != None:
                if discord_classes.get(i[2]) == None:
                    other.append(f'{i[1]}')
                    continue
                other.append(f'{discord_classes.get(i[2])} {i[1]}')
        
        users_count = [i[1] for i in await db.check_party(self,ctx)]   
        dps = "\n".join(dps)
        tank = "\n".join(tank)
        magician = "\n".join(magician)
        healer = "\n".join(healer)
        support = "\n".join(support)
        leech = "\n".join(leech)    
        other = "\n".join(other)    
        description = [i[4] for i in await db.check_party(self,ctx)][0]
        db_party_name = [i[0] for i in await db.get_date_time(self,ctx)][0]
        db_date = [i[1] for i in await db.get_date_time(self,ctx)][0]
        db_time = [i[2] for i in await db.get_date_time(self,ctx)][0]
        db_organize_person = [i[3] for i in await db.get_date_time(self,ctx)][0]
        
        embed = Embed(
            title = f''' Group info:  
:calendar: `{db_date}`  
:alarm_clock: `{db_time}`''',
            description = f"""**Description:**\n{description}\n
**{'Organized by**'} {db_organize_person}
**{'Members in group'} ( {len(users_count) - 1} )**""",
            color = 0x009ef7
            )
        if dps != "":
            embed.add_field(name = f':crossed_swords: __DPS__', value=f"{dps}\n\u200b",inline=True)
        else:
            embed.add_field(name = f':crossed_swords: __DPS__', value=f"** **\n\u200b",inline=True)
        if tank != "":
            embed.add_field(name = ':shield: __TANK__', value = f"{tank}\n\u200b",inline=True)        
        else:
            embed.add_field(name = ':shield: __TANK__', value = f"** **\n\u200b",inline=True)        
        if magician != "":
            embed.add_field(name = ':magic_wand: __MAGICIAN__', value = f"{magician}\n\u200b",inline=True) 
        else:
            embed.add_field(name = ':magic_wand: __MAGICIAN__', value = f"** **\n\u200b",inline=True)        
        if support != "":
            embed.add_field(name = ':cross: __SUPPORT__', value = f"{support}\n\u200b",inline=True)  
        else:
            embed.add_field(name = ':cross: __SUPPORT__', value = f"** **\n\u200b",inline=True)        
        if healer != "":
            embed.add_field(name = ':syringe: __HEALER__', value = f"{healer}\n\u200b",inline=True)   
        else:
            embed.add_field(name = ':syringe: __HEALER__', value = f"** **\n\u200b",inline=True)   
        if leech != "":
            embed.add_field(name = ':bug: __LEECH__', value = f"{leech}\n\u200b",inline=True) 
        else:
            embed.add_field(name = ':bug: __LEECH__', value = f"** **\n\u200b",inline=True) 
        if other != "":
            embed.add_field(name = ':x: __OTHER__', value = f"{other}\n\u200b",inline=True) 
        else:
            embed.add_field(name = ':x: __OTHER__', value = f"** **\n\u200b",inline=True) 

                   
        embed.set_author(name = f'{db_party_name}')
        embed.set_footer(text = f'Used by {ctx.author.name}\nThis message will be deleted in 60s',icon_url= "https://cdn-icons-png.flaticon.com/512/751/751381.png")
        embed.set_thumbnail(url="attachment://pngegg.png")
        await ctx.send(embed = embed,delete_after=60)     
        
def setup(bot):
    bot.add_cog(DisplayEmbed(bot))
    
