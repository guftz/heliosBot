import discord
import random
from typing import Optional

class EmbedBuilder:
    def __init__(self, title: Optional[str] = None, description: Optional[str] = None, color: discord.Color = discord.Color.default()):
        self.embed = discord.Embed(title=title, description=description, color=color)

    def set_author(self, name: str, icon_url: Optional[str] = None, url: Optional[str] = None) -> 'EmbedBuilder':      
        self.embed.set_author(name=name, icon_url=icon_url, url=url)
        return self

    def set_thumbnail(self, url: str) -> 'EmbedBuilder':
        self.embed.set_thumbnail(url=url)
        return self

    def set_image(self, url: str) -> 'EmbedBuilder':
        self.embed.set_image(url=url)
        return self

    def add_field(self, name: str, value: str, inline: bool = True) -> 'EmbedBuilder':
        self.embed.add_field(name=name, value=value, inline=inline)
        return self

    def set_footer(self, text: Optional[str] = None, icon_url: Optional[str] = None) -> 'EmbedBuilder':
        if not text:
            text = random.choice([
                "Thanks for using the bot",
                "If any bug occurs, try contacting the developer",
                "Helios Bot"
            ])
            
        self.embed.set_footer(text=text, icon_url=icon_url)
        return self

    def set_timestamp(self, timestamp: Optional[discord.utils.utcnow] = None) -> 'EmbedBuilder':
        self.embed.timestamp = timestamp if timestamp else discord.utils.utcnow()
        return self

    def set_color(self, color: discord.Color) -> 'EmbedBuilder':
        self.embed.color = color
        return self

    def build(self) -> discord.Embed:
        return self.embed
