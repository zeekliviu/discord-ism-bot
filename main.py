import discord
from discord.ext import commands
from os import getenv

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

class RoleButton(discord.ui.Button):
    def __init__(self, label, role_id):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(self.role_id)
        if role:
            if role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"Acum faci parte din {role.name}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"Deja faci parte din {role.name}!", ephemeral=True)

class RoleView(discord.ui.View):
    def __init__(self, roles):
        super().__init__(timeout=None)
        for label, role_id in roles.items():
            self.add_item(RoleButton(label, role_id))

@bot.command()
async def role_buttons(ctx):
    roles = {
        "1137": 1288142856674086943,
        "1138": 1288142664625295421
    }
    view = RoleView(roles)
    await ctx.send("Choose the group role you want:", view=view)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

bot.run(getenv("BOT_SECRET"))