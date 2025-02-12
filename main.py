import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

class RoleButton(discord.ui.Button):
    def __init__(self, label, role_id):
        custom_id = f"role_button:{role_id}:{label}"
        super().__init__(label=label, style=discord.ButtonStyle.primary, custom_id=custom_id)
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(self.role_id)
        if role:
            if role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"You are now part of {role.name}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"You are already part of {role.name}!", ephemeral=True)

ROLES = {
        "1137": 1288142856674086943,
        "1138": 1288142664625295421,
        "Visitor": 1302953783575187547
}

class RoleView(discord.ui.View):
    def __init__(self, roles):
        super().__init__(timeout=None)
        for label, role_id in roles.items():
            self.add_item(RoleButton(label, role_id))

@bot.command()
async def role_buttons(ctx):
    view = RoleView(ROLES)
    await ctx.send("Choose the role you want:", view=view)

@bot.event
async def on_ready():
    bot.add_view(RoleView(ROLES))
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

bot.run('BOT_SECRET')
