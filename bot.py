import discord
from discord.ext import commands

# Create bot instance with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)

bot.help_command = MyNewHelp()


bot.run('MTIwNTQ1NTQ0NTI4ODgyMDc4Ng.G45ljQ.RSRqQJ8uZGmFFyfsLAU9yl_bCMAsr9QBNmQUKI')
