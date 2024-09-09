# type: ignore

import discord
from discord.ext import commands
from discord.commands import Option
from database_handler import Database
from embed_builder import EmbedBuilder
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv('.env')

class Badges(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
    bot = discord.Bot()
    badge = bot.create_group("badge", "Badges Subcommands")
    
    @badge.command(name = "give", description = "Give a badge to a user")
    async def give(self, ctx: discord.ApplicationContext, 
                      user: Option(discord.Member, "The user to receive the Badge", required=True), 
                      badge_id: Option(str, "The Badge ID", required=True)) -> None:
        
        if ctx.author.id != int(os.getenv("OWNER_ID")):
            embederror = (EmbedBuilder(title="An error occurred", description=f"You do not have permission to do that")
                          .set_footer()
                          .set_timestamp()
                          .set_color(discord.Color.red())
                          .build())
            await ctx.respond(embed=embederror, ephemeral=True)
            return
        elif ctx.bot.user.id == user.id:
            embederror = (EmbedBuilder(title="An error occurred", description="You are trying to give the bot a badge")
                          .set_footer()
                          .set_timestamp()
                          .set_color(discord.Color.red())
                          .build())
            await ctx.respond(embed=embederror, ephemeral=True)
            return
        
        with Database.connect("database/users.db") as connection:
            if not connection:
                raise Exception("Failed to connect to the database.")
            
            Database.insert_user_on_database(connection, ctx.author.id, ctx.author.name)
            badge_exists = Database.select_data(connection, "badges", [badge_id], {"badge_id": badge_id})

            if badge_exists:
                user_has_badge = Database.select_data(connection, "user_badges", [badge_id], {"user_id": user.id, "badge_id": badge_id})
                if user_has_badge:
                    embederror = (EmbedBuilder(title="An error occurred", description=f"This user already has this badge ({badge_id})")
                          .set_footer()
                          .set_timestamp()
                          .set_color(discord.Color.red())
                          .build())
                    await ctx.respond(embed=embederror, ephemeral=True)
                else:
                    Database.insert_data(connection, "user_badges", {
                        "user_id": user.id, 
                        "badge_id": badge_id, 
                        "date_awarded": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
                    embed = (EmbedBuilder("Badge given", f"Badge given to {user.name} ({badge_id})")
                             .set_color(discord.Color.green())
                             .set_footer()
                             .set_timestamp()
                             .build())
                    await ctx.respond(embed=embed, ephemeral=True)
            else:
                embederror = (EmbedBuilder(title="An error occurred", description="This Badge does not exist")
                          .set_footer()
                          .set_timestamp()
                          .set_color(discord.Color.red())
                          .build())
                await ctx.respond(embed=embederror, ephemeral=True)
            
            
    @badge.command(name = "remove", description = "Remove a Badge from a user")
    async def remove(self, ctx: discord.ApplicationContext, 
                        user: Option(discord.Member, "The use to remove the Badge", required=True), 
                        badge_id: Option(str, "The badge ID", required=True)) -> None:
        
        if ctx.author.id != int(os.getenv("OWNER_ID")):
            embederror = (EmbedBuilder(title="An error occurred", description=f"You do not have permission to do that")
                          .set_footer()
                          .set_timestamp()
                          .set_color(discord.Color.red())
                          .build())
            await ctx.respond(embed=embederror, ephemeral=True)
            return
        elif ctx.bot.user.id == user.id:
            embederror = (EmbedBuilder(title="An error occurred", description="You are trying to remove a badge from the bot")
                          .set_footer()
                          .set_timestamp()
                          .set_color(discord.Color.red())
                          .build())
            await ctx.respond(embed=embederror, ephemeral=True)
            return
            
        with Database.connect("database/users.db") as connection:
            if not connection:
                raise Exception("Failed to connect to the database.")
            
            Database.insert_user_on_database(connection, ctx.author.id, ctx.author.name)
            badge_exists = Database.select_data(connection, "badges", [badge_id], {"badge_id": badge_id})

            if badge_exists:
                user_has_badge = Database.select_data(connection, "user_badges", [badge_id], {"user_id": user.id, "badge_id": badge_id})
                if user_has_badge:
                    Database.delete_data(connection, "user_badges", {
                        "user_id": user.id, 
                        "badge_id": badge_id})
                    (EmbedBuilder("Badge removed", f"Badge removed from {user.name} ({badge_id})")
                             .set_color(discord.Color.red())
                             .set_footer()
                             .set_timestamp()
                             .build())
                    await ctx.respond(embed=embed, ephemeral=True)
                else:
                    embederror = (EmbedBuilder(title="An error occurred", description=f"The user {user.name} does not have this badge ({badge_id})")
                          .set_footer()
                          .set_timestamp()
                          .set_color(discord.Color.red())
                          .build())
                    await ctx.respond(embed=embederror, ephemeral=True)
                    
            else:
                embederror = (EmbedBuilder(title="An error occurred", description="This Badge does not exist")
                          .set_footer()
                          .set_timestamp()
                          .set_color(discord.Color.red())
                          .build())
                await ctx.respond(embed=embederror, ephemeral=True)
    
    bot.add_application_command(badge)
                
                
def setup(bot:commands.Bot):
    bot.add_cog(Badges(bot))