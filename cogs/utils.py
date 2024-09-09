# type: ignore

import discord
from discord.ext import commands
from discord.commands import Option
import random


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.slash_command(name="ping", description="Returns the bot's latency")
    async def ping(self, ctx: discord.ApplicationContext) -> None:
        await ctx.respond(f"Pong! {round(self.bot.latency * 1000)} ms")

    @discord.slash_command(name="8ball", description="Find out your fate")
    async def eightball(self, ctx: discord.ApplicationContext, question: str) -> None:
        possible_answears = ["It is certain", "It is decidedly so",
                             "Without a doubt", "Yes, definitely", "You may rely on it"]
        await ctx.respond(random.choice(possible_answears))

    @discord.slash_command(name="roll", description="Roll a dice")
    async def roll(self, ctx: discord.ApplicationContext, dice_number: int) -> None:
        dice_result = random.randint(0, dice_number)
        await ctx.respond(f"You rolled a {dice_result} from a {dice_number} sided dice")

    @discord.slash_command(name="avatar", description="Get someone's avatar")
    async def avatar(self, ctx: discord.ApplicationContext, user: Option(discord.Member, "The user to get the avatar", required=False)) -> None:
        if user is None:
            user = ctx.author
        await ctx.respond(user.avatar.url)

    @discord.slash_command(name="rps", description="Play Rock, Paper, Scissors")
    async def rps(self, ctx: discord.ApplicationContext, choice: Option(str, "Your choice", choices=["🪨", "📃", "✂️"], required=True)) -> None:

        possibilities = ["🪨", "📃", "✂️"]
        bot_choice = possibilities[random.randint(0, 2)]

        if choice == bot_choice:
            await ctx.respond(f"Your choice: {choice} \nBot choice: {bot_choice} \n\n**It is a Draw!**")

        elif choice == "🪨" and bot_choice == "✂️":
            await ctx.respond(f"Your choice: {choice} \nBot choice: {bot_choice} \n\n**You Win!**")

        elif choice == "📃" and bot_choice == "🪨":
            await ctx.respond(f"Your choice: {choice} \nBot choice: {bot_choice} \n\n**You Win!**")

        elif choice == "✂️" and bot_choice == "📃":
            await ctx.respond(f"Your choice: {choice} \nBot choice: {bot_choice} \n\n**You Win!**")
            
        else:
            await ctx.respond(f"Your choice: {choice} \nBot choice: {bot_choice} \n\n**You Lose!**")

def setup(bot: commands.Bot):
    bot.add_cog(Misc(bot))
