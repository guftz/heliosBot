import discord
from discord.ext import commands
from database_handler import Database 
from embed_builder import EmbedBuilder
from dotenv import load_dotenv
import re

load_dotenv('.env')

class Profile(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    bot = discord.Bot()
    profile = bot.create_group("profile", "Profile Subcommands")

    @profile.command(name="view", description="See your profile")
    async def view(self, ctx: discord.ApplicationContext) -> None:
        try:

            with Database.connect("database/users.db") as connection:
                if not connection:
                    raise Exception("Failed to connect to the database.")

                Database.insert_user_on_database(connection, ctx.author.id, ctx.author.name)
                result = Database.select_data(connection, "profiles", ["username", "points", "bio", "color"], {"user_id": ctx.author.id})
                
                if not result:
                    raise Exception("Profile not found.")
                
                result_username = result[0]["username"]
                result_points = result[0]["points"]
                result_bio = result[0]["bio"]
                result_color = result[0]["color"].lstrip("#").upper()
                color_int = int(result_color, 16)

                badge_list = Database.select_data(connection, "user_badges", ["badge_id"], {"user_id": ctx.author.id})
                badge_ids = [badge['badge_id'] for badge in badge_list]
                badges = "\n".join(Database.select_data(connection, "badges", ["name"], {"badge_id": item})[0]['name'] for item in badge_ids)

                embed = (EmbedBuilder(title="My Profile", description=f"{result_bio}")
                         .set_author(name=f"{result_username}", icon_url=f"{ctx.author.avatar.url}")
                         .add_field(name=":star: Points", value=f"{result_points}", inline=True)
                         .add_field(name=":eyes: Badges", value=badges, inline=False)
                         .set_thumbnail(url=f"{ctx.author.avatar.url}")
                         .set_footer()
                         .set_timestamp()
                         .set_color(color_int)
                         .build())

                await ctx.respond(embed=embed)
                
        except Exception as e:
            embederror = (EmbedBuilder(title="An error occurred", description=f"{e}")
                          .set_footer()
                          .set_timestamp()
                          .set_color(discord.Color.red())
                          .build())
            await ctx.respond(embed=embederror)

    @profile.command(name="setcolor", description="Set your profile color")
    async def set_color(self, ctx: discord.ApplicationContext, color: str) -> None:
        try:
            with Database.connect("database/users.db") as connection:
                if not connection:
                    raise Exception("Failed to connect to the database.")

                Database.insert_user_on_database(connection, ctx.author.id, ctx.author.name)
                check_color = Database.select_data(connection, "profiles", ["color"], {"user_id": ctx.author.id})

                if check_color and check_color[0]["color"] == color:
                    await ctx.respond("You cannot choose the same color!", ephemeral=True)
                    return

                if re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
                    Database.update_data(connection, "profiles", {"color": color}, {"user_id": ctx.author.id})
                    embed = (EmbedBuilder(title="Color changed successfully", description=f"Color set to {color}")
                             .set_footer()
                             .set_timestamp()
                             .set_color(discord.Color.embed_background())
                             .build())
                    await ctx.respond(embed=embed, ephemeral=True)
                else:
                    await ctx.respond("Wrong color format. Try using **#FFFFFF**", ephemeral=True)
        except Exception as e:
            embederror = (EmbedBuilder(title="An error occurred", description=f"{e}")
                          .set_footer()
                          .set_timestamp()
                          .set_color(discord.Color.red())
                          .build())
            await ctx.respond(embed=embederror)

    @profile.command(name="setbio", description="Set your profile's bio")
    async def set_bio(self, ctx: discord.ApplicationContext, bio: str) -> None:
        try:
            with Database.connect("database/users.db") as connection:
                if not connection:
                    raise Exception("Failed to connect to the database.")

                Database.insert_user_on_database(connection, ctx.author.id, ctx.author.name)
                Database.update_data(connection, "profiles", {"bio": bio}, {"user_id": ctx.author.id})

                embed = (EmbedBuilder(title="Bio updated successfully", description=f"Bio set to: {bio}")
                         .set_footer()
                         .set_timestamp()
                         .set_color(discord.Color.embed_background())
                         .build())
                await ctx.respond(embed=embed, ephemeral=True)
        except Exception as e:
            embederror = (EmbedBuilder(title="An error occurred", description=f"{e}")
                          .set_footer()
                          .set_timestamp()
                          .set_color(discord.Color.red())
                          .build())
            await ctx.respond(embed=embederror)
            
    bot.add_application_command(profile)

def setup(bot:commands.Bot):
    bot.add_cog(Profile(bot))
