from discord.ext import commands

class BotLogin(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
          
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready")
        

        


def setup(bot):
    bot.add_cog(BotLogin(bot))