import discord
from discord.ext import commands
from database_handler import Database
from embed_builder import EmbedBuilder


class Daily(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
    @discord.slash_command(name = "daily", description = "Get daily reward")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def command(self, ctx: discord.ApplicationContext) -> None:
        try:
            points_to_add = 100
            with Database.connect("database/users.db") as connection:
                if not connection:
                    raise Exception("Failed to connect to the database.")
                
                Database.insert_user_on_database(connection, ctx.author.id, ctx.author.name)
                current_points = Database.select_data(connection, "profiles", ["points"], {"user_id": ctx.author.id})
                Database.update_data(connection, "profiles", {"points": current_points[0]["points"] + points_to_add}, {"user_id": ctx.author.id})
                
                embed = (EmbedBuilder(title="Good to see you again!", description=f"Here is your daily bonus")
                    .add_field(name="Daily Bonus", value=f"+{points_to_add}", inline=True)
                    .add_field(name="<:star:1276191913988329553> Points", value=current_points[0]["points"] + points_to_add, inline=True)
                    .set_footer()
                    .set_timestamp()
                    .set_color(0xfbbb02)
                    .build())
                
                await ctx.respond(embed=embed)
        except Exception as e:
            embederror = (EmbedBuilder(title="An error occurred", description=f"{e}")
                .set_footer()
                .set_timestamp()
                .set_color(discord.Color.red())
                .build())
            await ctx.respond(embed=embederror)
        finally:
            if self.connection:
                self.connection.close()
        
            
def setup(bot:commands.Bot):
    bot.add_cog(Daily(bot))