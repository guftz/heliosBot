import discord
from discord.ext import commands
from database_handler import Database
from embed_builder import EmbedBuilder
import random


class Gambling(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    bot = discord.Bot()
    gambling = bot.create_group("gambling", "Gambling Subcommands")
    
    @gambling.command(name="coinflip", description="Do a coinflip")
    async def coinflip(self, ctx: discord.ApplicationContext, amount: int):
        
        try:
            with Database.connect("database/users.db") as connection:
                if not connection:
                    raise Exception("Failed to connect to the database.")
                
                Database.insert_user_on_database(connection, ctx.author.id, ctx.author.name)
                result = Database.select_data(connection, "profiles", ["points"], {"user_id": ctx.author.id})
                
                if not result:
                            raise Exception("Profile not found.")
                
                if result[0]["points"] < amount:
                    await ctx.respond("You do not have enough points to execute this command", ephemeral=True)
                else:
                    odd = random.choice([0, 1])
                    if odd == 1:
                        new_amount = result[0]["points"] + amount
                        
                        if ctx.author.avatar:
                            author_profile_pic = ctx.author.avatar.url
                        else:
                            author_profile_pic = "https://dummyimage.com/512x512/000/fff.jpg&text=No+Image"
                        
                        embed = (EmbedBuilder(title="You Won")
                            .set_author(name=f"{ctx.author.name}", icon_url=author_profile_pic)
                            .add_field("Gambled amount", f"{amount}")
                            .add_field("Your points", f"{new_amount}")
                            .set_footer()
                            .set_timestamp()
                            .set_color(discord.Color.green())
                            .build())
                        
                        Database.update_data(connection, "profiles", {"points": new_amount}, {"user_id": ctx.author.id})
                        
                        await ctx.respond(embed=embed)
                    else:
                        new_amount = result[0]["points"] - amount
                        
                        if ctx.author.avatar:
                            author_profile_pic = ctx.author.avatar.url
                        else:
                            author_profile_pic = "https://dummyimage.com/512x512/000/fff.jpg&text=No+Image"
                        
                        embed = (EmbedBuilder(title="You Lost")
                            .set_author(name=f"{ctx.author.name}", icon_url=author_profile_pic)
                            .add_field("Your points", f"{new_amount}")
                            .set_footer()
                            .set_timestamp()
                            .set_color(discord.Color.red())
                            .build())
                        Database.update_data(connection, "profiles", {"points": new_amount}, {"user_id": ctx.author.id})
                        await ctx.respond(embed=embed)
        except Exception as e:
            embederror = (EmbedBuilder(title="An error occurred", description=f"{e}")
                          .set_footer()
                          .set_timestamp()
                          .set_color(discord.Color.red())
                          .build())
            await ctx.respond(embed=embederror)
            raise Exception(e)
                
            
    bot.add_application_command(gambling)
        
def setup(bot:commands.Bot):
    bot.add_cog(Gambling(bot))