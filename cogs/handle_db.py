from discord.ext import commands
import sqlite3

class HandlingDatabase(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
        
    @commands.command()     
    async def admin_add_table_roles(self,guild):
        conn = sqlite3.connect(f"databases//{guild.name} - {str(guild.id)}.db")
        cursor = conn.cursor()
        table = f"""CREATE TABLE IF NOT EXISTS Roles(
                role VARCHAR(255) NOT NULL,
                UNIQUE (role));"""
        cursor.execute(table)
        conn.close()
        
    @commands.command()     
    async def admin_add_table_class(self,guild):
        conn = sqlite3.connect(f"databases//{guild.name} - {str(guild.id)}.db")
        cursor = conn.cursor()
        table = f"""CREATE TABLE IF NOT EXISTS Classes(
                class VARCHAR(255) NOT NULL,
                IconClass VARCHAR(255) NOT NULL);"""
        cursor.execute(table)
        conn.close()
        
    @commands.command()     
    async def admin_add_table_channel(self,guild):
        conn = sqlite3.connect(f"databases//{guild.name} - {str(guild.id)}.db")
        cursor = conn.cursor()
        table = f"""CREATE TABLE IF NOT EXISTS Channels(
                Channel_name VARCHAR(255),
                Channel_id VARCHAR(255) NOT NULL,
                UNIQUE (Channel_id));"""
        cursor.execute(table)
        conn.close()
    
    @commands.command()     
    async def admin_add_role(self,roles,guild):
        conn = sqlite3.connect(f"databases//{guild.name} - {str(guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"INSERT OR IGNORE INTO Roles(role) VALUES ('{roles}')")
        conn.commit()
        conn.close()   
        
# --------------------------------------------------------------------------------------------------------------------------------


    @commands.command()     
    async def add_table(self,ctx):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        table = f"""CREATE TABLE '{str(ctx.channel.id)}' (
                Party_name VARCHAR(255),
                Date INT(20),
                Time INT(20),
                Organize_person VARCHAR(255),
                Person_ID VARCHAR(25),
                Person VARCHAR(255),
                Role VARCHAR(20),
                Class VARCHAR(20),
                Description VARCHAR(500));"""
        cursor.execute(table)   
        conn.commit()
        conn.close()
        
    @commands.command()     
    async def add_date_time(self,ctx,party_name,date,time):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO '{str(ctx.channel.id)}' VALUES ('{party_name}','{date}','{time}','{ctx.author.mention}',NULL,NULL,NULL,NULL,'')")
        conn.commit()
        conn.close()

    @commands.command()     
    async def add_user(self,ctx,user_name,user_class,user_role):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO '{ctx.channel.id}' VALUES (NULL,NULL,NULL,NULL,{ctx.author.id},'{user_name}','{user_class}','{user_role}',NULL)")
        conn.commit()
        conn.close()
        
    @commands.command()     
    async def add_class(self,ctx,class_name,icon):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO Classes VALUES ('{class_name}','{icon}')")
        conn.commit()
        conn.close()
        
        
    @commands.command()     
    async def remove_class(self,ctx,class_name):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM Classes WHERE class = '{class_name}'")
        conn.commit()
        conn.close()        
        
    @commands.command()     
    async def remove_user(self,ctx,user_name):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM '{ctx.channel.id}' WHERE Person = '{user_name}'")
        conn.commit()
        conn.close()
   
    @commands.command()     
    async def update_class_user(self,ctx,user_name,update_class):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE '{ctx.channel.id}' SET Class = '{update_class}' WHERE Person = '{user_name}'")
        conn.commit()
        conn.close()

    @commands.command()     
    async def update_role_user(self,ctx,user_name,update_role):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE '{ctx.channel.id}' SET Role = '{update_role}' WHERE Person = '{user_name}'")
        conn.commit()
        conn.close()
        
    @commands.command()     
    async def add_description_user(self,ctx,description,user):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE '{ctx.channel.id}' SET Description = '{description}' WHERE Organize_person = '{user}'")
        conn.commit()
        conn.close()

    @commands.command()     
    async def remove_description_user(self,ctx,user):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE '{ctx.channel.id}' SET Description = '' WHERE Organize_person = '{user}'")
        conn.commit()
        conn.close()
        
    @commands.command()     
    async def delete_party_user(self,ctx):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE '{ctx.channel.id}'")
        conn.commit()
        conn.close()


# --------------------------------------------------------------------------------------------------------------------------------


    @commands.command()     
    async def check_party(self,ctx):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT Person_ID,Person,Class,Role,Description FROM '{str(ctx.channel.id)}'")
        rows = cursor.fetchall()
        conn.close()
        return rows
        
    @commands.command()     
    async def get_date_time(self,ctx):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT Party_name,Date,Time,Organize_person FROM '{ctx.channel.id}' ")
        except:
            pass
        return cursor.fetchmany()
    
    @commands.command()     
    async def check_classes(self,ctx):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT class,Iconclass FROM Classes")
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows
    

    @commands.command()     
    async def check_roles(self,ctx):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT role FROM Roles")
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows


    @commands.command()     
    async def add_channel(self,ctx,channel_name,channel_id):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO Channels VALUES ('{channel_name}','{channel_id}')")
        conn.commit()
        conn.close()


    @commands.command()     
    async def check_channels(self,ctx):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT Channel_name, Channel_id FROM Channels")
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows


    @commands.command()     
    async def delete_channel(self,ctx,channel_id):
        conn = sqlite3.connect(f"databases//{ctx.guild.name} - {str(ctx.guild.id)}.db")
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM Channels WHERE Channel_id = '{channel_id}'")
        conn.commit()
        conn.close()




def setup(bot):
    bot.add_cog(HandlingDatabase(bot))