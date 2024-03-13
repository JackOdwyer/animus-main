import os

import discord
from discord import user, guild

from discord.ext import commands
import aiohttp
import datetime
from discord.ui import button
from discord.ui import Select
import asyncio
import json
from datetime import timedelta
import random
import requests
from discord.ui import View
from others.variables import staff_ids
from others.variables import BADGE_NAMES

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("?"), intents=intents)
warnings = {}
configurations = {}
whitelisted_users = [968066034051477544, 1005780651825430600]


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="/help | Animus Systems"))
    print(f'Logged in as {bot.user.name} | ID: {bot.user.id}')
    await bot.load_extension("jishaku")


class ViewRblxPf(discord.ui.View):
  def __init__(self):
      super().__init__(timeout=30)  # times out after 30 seconds
      button = discord.ui.Button(label='Upload Audition Now', style=discord.ButtonStyle.url, url='')
      self.add_item(button)


@bot.event
async def on_guild_join(guild):
    # Replace 'CHANNEL_ID' with the ID of the desired channel
    channel_id = 1206065941834633226
    # Get the channel object from the guild using the channel ID
    channel = guild.get_channel(channel_id)

    # Check if the channel exists and is a text channel
    if channel and isinstance(channel, discord.TextChannel):
        # Create a webhook in the channel with the server name as the webhook name
        webhook = await channel.create_webhook(name=guild.name)

        # Post a message using the webhook
        await webhook.send(f"Animus has been added to ``{guild.name}`` ")


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.tree.command(name='add', description='Add two numbers')
async def add(interaction: discord.Interaction, num1: int, num2: int):
    """Add two numbers"""
    result = num1 + num2
    await interaction.response.send_message(content=f'The sum of {num1} and {num2} is {result}')


@bot.tree.command(name='warn', description='Warn a user')
async def warn_user(interaction: discord.Interaction, member: discord.Member, *, reason: str):
    """Warn a user"""
    if interaction.user == member:  # Use interaction.user instead of interaction.author
        embed = discord.Embed(title='Error', description='You cannot warn yourself.', color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    try:
        # Your logic here to warn a user
        embed = discord.Embed(title='User Warned', description=f'User {member.name} has been warned. Reason: {reason}',
                              color=discord.Color(int("302c34", 16)))
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f'Error in warn command: {e}')


@bot.tree.command()
async def ping(interaction: discord.Interaction):
    """Show bot's ping, latency and uptime status."""
    latency = round(bot.latency * 1000)

    # Define border color
    border_color = discord.Color(int("302c34", 16))

    # Calculate bot uptime in hours
    created_at_naive = bot.user.created_at.replace(tzinfo=None)
    uptime_seconds = (datetime.datetime.utcnow() - created_at_naive).total_seconds()
    uptime_hours = round(uptime_seconds / 3600)

    # Create the embed
    embed = discord.Embed(title=f"**{interaction.user.name}, here is my latency info:** ", color=border_color)

    # Add fields to the embed
    embed.add_field(name="**Bot Status**", value="🟢 Online")
    embed.add_field(name="**Bot Latency**", value=f"<:correct:1204702940015624202> {latency} ms", inline=False)
    embed.add_field(name="**Bot Server**", value="<:correct:1204702940015624202> Connected", inline=False)
    embed.add_field(name="**Bot Databse**", value="<:correct:1204702940015624202> Connected", inline=False)
    embed.add_field(name="Uptime", value=f"<:correct:1204702940015624202> {uptime_hours} hours ago", inline=False)
    embed.set_footer(text=f"Requested by {interaction.user.id}", icon_url=interaction.user.avatar)

    # Set the bot's avatar as thumbnail
    embed.set_thumbnail(url=bot.user.avatar)

    # Send the embed
    await interaction.response.send_message(embed=embed)



@bot.tree.command(name='getavatar', description='Get the avatar of a user')
async def getavatar(interaction: discord.Interaction, user: discord.User = None):
    """Get the avatar of a user"""
    try:
        # If user is not provided, default to the invoking user
        user = user or interaction.user

        avatar_url = user.avatar.url

        embed = discord.Embed(title=f'{user.name}\'s Avatar', color=discord.Color.purple())
        embed.set_image(url=avatar_url)

        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error in getavatar command: {e}")


@bot.tree.command(name='cat', description='Get a picture of a cat')
async def cat(interaction: discord.Interaction):
    """Get a picture of a cat"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.thecatapi.com/v1/images/search') as response:
                data = await response.json()

        cat_url = data[0]['url']

        embed = discord.Embed(title='Cat', color=discord.Color(int("302c34", 16)))
        embed.set_image(url=cat_url)

        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error in catimg command: {e}")


@bot.tree.command(name='doggo', description='Get a picture of a dog')
async def dog(interaction: discord.Interaction):
    """Get a picture of a dog"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dog.ceo/api/breeds/image/random') as response:
                data = await response.json()

        dog_url = data['message']

        embed = discord.Embed(title='Doggo', color=discord.Color(int("302c34", 16)))
        embed.set_image(url=dog_url)

        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error in dogimg command: {e}")


@bot.command(name='purge', description='Purge messages in the channel')
async def purge(ctx, limit: int):
    try:
        # Fetch messages and delete them in batches
        messages = await ctx.channel.history(limit=limit + 1).flatten()
        await ctx.channel.purge(limit=limit + 1)

        # Inform the user about the number of messages deleted
        await ctx.send(f'Successfully purged {len(messages) - 1} messages.')

    except discord.Forbidden:
        await ctx.send('I do not have the required permissions to delete messages.')

    except Exception as e:
        print(f"Error in purge command: {e}")


@bot.tree.command(name='role-add', description='Add a role to a user')
async def add_role(interaction: discord.Interaction, user: discord.User, role: discord.Role):
    """Add a role to a user."""
    try:
        member = interaction.guild.get_member(user.id)
        if member is not None:
            await member.add_roles(role)
            # Prepare the embed
            embed = discord.Embed(title="<:correct:1204702940015624202> Role Added",
                                  color=discord.Color(int("302c34", 16)))
            embed.add_field(name="User", value=f"{user.name}#{user.discriminator}")
            embed.add_field(name="Role", value=role.name)
            embed.set_footer(text="Role added successfully.")
            # Send the embed
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(content=f'{user.name} is not a member of this server.')
    except Exception as e:
        print(f"Error in addrole command: {e}")


@bot.tree.command(name='role-remove', description='Remove a role from a user')
async def delrole(interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    """Remove a role from a user."""
    try:
        if role in user.roles:
            await user.remove_roles(role)
            # Prepare the embed
            embed = discord.Embed(title="<:correct:1204702940015624202> Role Removed",
                                  color=discord.Color(int("302c34", 16)))
            embed.add_field(name="User", value=user.mention)
            embed.add_field(name="Role", value=role.name)
            embed.set_footer(text="Role removed successfully.")
            # Send the embed
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(content=f"{user.mention} does not have the role `{role.name}`.")
    except Exception as e:
        print(f"Error in delrole command: {e}")


@bot.tree.command()
async def say(interaction: discord.Interaction, message: str):
    '''Broadcasts a message in the channel'''
    channel = interaction.channel
    try:
        await interaction.response.send_message("Message sent.", ephemeral=True)
        await channel.send(message)
    except:
        await channel.send('Failed to process command.')


@bot.command(name='loa', description='Submit a Leave of Absence request')
async def loa_request(ctx, time: str, *, reason: str):
    """Submit a Leave of Absence request"""
    try:
        # Attempt to parse the time, raise ValueError if invalid
        parsed_time = int(time)
    except ValueError:
        # Invalid time format, send an embed with an error message
        embed = discord.Embed(title='Invalid Time', description='The time you provided was invalid or incorrect',
                              color=discord.Color(int("302c34", 16)))
        await ctx.send(embed=embed)
        return

    # Successful time parsing, send success message in a green embed
    emoji_id = 1163149118366040106
    success_embed = discord.Embed(
        title=f'<:loa:1207933665330462780> Request Sent',
        description=f'Your LOA Request has been saved and sent!', color=0x00FF00)
    await ctx.send(embed=success_embed)

    # Schedule a delayed notification when the LOA is up
    await schedule_loa_notification(ctx.author, parsed_time)


async def schedule_loa_notification(user, loa_duration):
    # Calculate the datetime when LOA is up
    loa_end_time = datetime.utcnow() + timedelta(days=loa_duration)

    # Sleep until LOA is up
    await asyncio.sleep(loa_duration * 24 * 60 * 60)

    # Send a notification to the user that LOA is up
    notification_message = f"{user.mention}, Your LOA time is up!"
    await user.send(notification_message)


@bot.command(name='rconfigview')
async def rconfigview(ctx):
    # Check if user has a previous configuration
    if ctx.author.id in configurations:
        staff_role, management_role, developer_role, member_role = configurations[ctx.author.id]
        # Display the current configuration
        await ctx.send(embed=discord.Embed(
            description=f"Current Configuration:\nStaff Role: {staff_role}\nManagement Role: {management_role}\nDeveloper Role: {developer_role}\nMember Role: {member_role}",
            color=0xFFFFFF))
    else:
        await ctx.send(
            embed=discord.Embed(description="No configuration found. Run rconfig to set up roles.", color=0xFFFFFF))


@bot.command(name='rconfigdelete')
async def rconfigdelete(ctx):
    # Check if user has a previous configuration
    if ctx.author.id in configurations:
        # Delete the configuration
        del configurations[ctx.author.id]
        await ctx.send(embed=discord.Embed(description="Configuration deleted.", color=0xFFFFFF))
    else:
        await ctx.send(embed=discord.Embed(description="No configuration found to delete.", color=0xFFFFFF))


async def ask_role(ctx, question):
    await ctx.send(embed=discord.Embed(description=question, color=0xFFFFFF))
    try:
        response = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
        # Extract role mentions from the message
        role_mentions = [role.mention for role in response.role_mentions]
        return role_mentions[0] if role_mentions else "default_role"
    except asyncio.TimeoutError:
        return "default_role"


@bot.command(name='server-info')
async def server_info(ctx):
    server = ctx.guild

    # Basic Information
    created_at = server.created_at.strftime('%B %d, %Y %I:%M %p')
    joined_at = ctx.author.joined_at.strftime('%B %d, %Y %I:%M %p')
    member_count = len(server.members)
    online_members = sum(m.status != discord.Status.offline for m in server.members)
    boosts = server.premium_subscription_count

    # Security
    verification_level = server.verification_level
    explicit_content_filter = server.explicit_content_filter
    verification_gate = "Enabled" if server.verification_level != discord.VerificationLevel.none else "Disabled"

    # Server Configuration

    system_channel = server.system_channel
    rules_channel = discord.utils.get(server.channels, name='guidelines')

    # Channels
    text_channels = sum(1 for channel in server.channels if isinstance(channel, discord.TextChannel))
    voice_channels = sum(1 for channel in server.channels if isinstance(channel, discord.VoiceChannel))
    announcement_channels = sum(
        1 for channel in server.channels if channel.category and channel.category.name == 'Announcement')

    # Roles
    roles = '\n'.join([role.mention for role in server.roles])

    # Features
    features = ', '.join(server.features) if server.features else 'None'

    # Create Embed
    embed = discord.Embed(title="Server Information", color=discord.Color.from_rgb(47, 49, 54))

    # Basic Information
    embed.add_field(name="Name", value=server.name, inline=False)
    embed.add_field(name="Owner", value=server.owner.mention, inline=False)
    embed.add_field(name="Created", value=created_at, inline=False)
    embed.add_field(name="Notifications", value="Only @Mentions", inline=False)
    embed.add_field(name="Members", value=f"{member_count} ({online_members} online)", inline=False)
    embed.add_field(name="Nitro Boosts", value=f"{boosts} Boosts", inline=False)

    # Security
    embed.add_field(name="2FA Settings", value="Not Required", inline=False)
    embed.add_field(name="Verification Level", value=str(verification_level).title(), inline=False)
    embed.add_field(name="Explicit Content Filter", value=explicit_content_filter.name, inline=False)
    embed.add_field(name="Member Verification Gate", value=verification_gate, inline=False)

    # Server Configuration
    embed.add_field(name="System Messages Channel", value=system_channel.mention if system_channel else 'Not Set',
                    inline=False)
    embed.add_field(name="Rules Channel", value=rules_channel.mention if rules_channel else 'Not Set', inline=False)

    # Channels
    text_channels = sum(1 for channel in server.channels if isinstance(channel, discord.TextChannel))
    voice_channels = sum(1 for channel in server.channels if isinstance(channel, discord.VoiceChannel))
    # Roles
    embed.add_field(name="Roles", value=roles, inline=False)

    # Features
    embed.add_field(name="Features", value=features, inline=False)

    # Send the Embed
    await ctx.send(embed=embed)


@bot.command(name='newconfig')
async def rconfig(ctx):
    # Check if user has a previous configuration
    if ctx.author.id in configurations:
        staff_role, management_role, developer_role, member_role = configurations[ctx.author.id]
    else:
        staff_role = "default_staff_role"
        management_role = "default_management_role"
        developer_role = "default_developer_role"
        member_role = "default_member_role"

    emoji_id = 1184700629214572635

    try:
        emoji = await ctx.guild.fetch_emoji(emoji_id)
    except discord.NotFound:
        emoji = None  # Handle if the emoji is not found

    embed = discord.Embed(title=f"<:Settings:1184700629214572635> **Role Configuration**", color=0xFFFFFF)
    embed.add_field(name="**Staff Role Setup**",
                    value=f"The staff role configuration is going to help W1ZARD define who is staff and who is not, making it easier to assign roles such as on duty etc",
                    inline=False)
    embed.add_field(name="**Manager/Management Role Setup**",
                    value=f"This is the role that helps with permissions, managing requests, managing community and managing punishments.",
                    inline=False)
    embed.add_field(name="**Developer Role Setup**",
                    value=f"This is the role for developers who will have special permissions.", inline=False)
    embed.add_field(name="**Member Role Setup**", value=f"This is the role for regular members.", inline=False)

    # Send the embed
    await ctx.send(embed=embed)

    # Ask questions and await user responses
    staff_role = await ask_role(ctx, "What is your desired Staff Role?")
    management_role = await ask_role(ctx, "What is your desired Management Role?")
    developer_role = await ask_role(ctx, "What is your desired Developer Role?")
    member_role = await ask_role(ctx, "What is your desired Member Role?")

    # Save the configuration
    configurations[ctx.author.id] = (staff_role, management_role, developer_role, member_role)

    # Display the updated configuration
    await ctx.send(embed=discord.Embed(
        description=f"Updated Configuration:\nStaff Role: {staff_role}\nManagement Role: {management_role}\nDeveloper Role: {developer_role}\nMember Role: {member_role}",
        color=0xFFFFFF))


@bot.tree.command(name="bird")
async def birdimg(interaction: discord.Interaction):
    """Get a random bird image."""
    # You need to replace 'YOUR_ACCESS_KEY' with your actual Unsplash access key
    access_key = 'fCoChV-umUMmA_rd-h05M3MzaJ05Bmf6ZENhS_-Qnu8'
    url = f"https://api.unsplash.com/photos/random?query=bird&client_id={access_key}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                image_url = data.get('urls', {}).get('regular')
                if image_url:
                    embed = discord.Embed(title="Birb", color=discord.Color(int("302c34", 16)))
                    embed.set_image(url=image_url)
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message(content="Sorry, no bird image found.")
            else:
                await interaction.response.send_message(content="Sorry, could not fetch bird image.")


@bot.tree.command()
async def ban(interaction: discord.Interaction, member: discord.Member, *, reason: str):
    """Ban a member from the server."""
    # Check if the user who triggered the interaction has permission to ban members
    if interaction.user.guild_permissions.ban_members:
        # Check if the bot has permission to ban members
        if interaction.guild.me.guild_permissions.ban_members:
            # Perform the ban
            try:
                await member.ban(reason=reason)
                await interaction.response.send_message(f"{member} has been banned from the server.")
            except discord.Forbidden:
                await interaction.response.send_message("I don't have permission to ban members.")
        else:
            await interaction.response.send_message("I don't have permission to ban members.")
    else:
        await interaction.response.send_message("You don't have permission to use this command.")


@bot.tree.command()
async def kick(interaction: discord.Interaction, member: discord.Member, *, reason: str):
    """Kick a member from the server."""
    # Check if the user who triggered the interaction has permission to kick members
    if interaction.user.guild_permissions.kick_members:
        # Check if the bot has permission to kick members
        if interaction.guild.me.guild_permissions.kick_members:
            # Perform the kick
            try:
                await member.kick(reason=reason)
                await interaction.response.send_message(f"{member} has been kicked from the server.")
            except discord.Forbidden:
                await interaction.response.send_message("I don't have permission to kick members.")
        else:
            await interaction.response.send_message("I don't have permission to kick members.")
    else:
        await interaction.response.send_message("You don't have permission to use this command.")


@bot.command()
async def dropdown(ctx):
    # Define the options for the dropdown menu
    options = [
        discord.SelectOption(label="Option 1", value="option1"),
        discord.SelectOption(label="Option 2", value="option2"),
        discord.SelectOption(label="Option 3", value="option3")
    ]

    # Create the select dropdown
    select = Select(
        placeholder="Select an option",
        options=options
    )

    # Create a view with the dropdown
    view = View()
    view.add_item(select)

    # Send the message with the dropdown
    message = await ctx.send("Please select an option:", view=view)

    # Wait for the user to make a selection
    interaction = await bot.wait_for("select_option", check=lambda i: i.component.id == select.custom_id)
    selected_option = interaction.values[0]

    # Send a message based on the selected option
    if selected_option == "option1":
        await ctx.send("You selected Option 1!")
    elif selected_option == "option2":
        await ctx.send("You selected Option 2!")
    elif selected_option == "option3":
        await ctx.send("You selected Option 3!")


@bot.command(name='whois')
async def whois(ctx, *, user_info=None, embed=None):
    guild_id = str(ctx.guild.id)
    if user_info is None:
        member = ctx.author
    else:
        if user_info.startswith('<@') and user_info.endswith('>'):
            user_id = int(user_info[2:-1])
            member = ctx.guild.get_member(user_iqd)
        else:
            member = discord.utils.find(lambda m: m.name == user_info, ctx.guild.members)
            admin_staff_roles = [role for role in member.roles if
                                 role.permissions.administrator and role.id in staff_ids]

            # Get the names of the filtered roles
            staff_roles_with_admin = [role.name for role in admin_staff_roles]
            staff_roles_with_admin2 = ", ".join(staff_roles_with_admin) if staff_roles_with_admin else "None"

    if member:
        # Create the embed
        embed = discord.Embed(title="User Information", color=discord.Color.from_rgb(47, 49, 54))

        # Add user info as fields
        embed.add_field(name="Username", value=f"{member.name}\n{member.mention}", inline=True)

        embed.add_field(name="User ID", value=member.id, inline=True)

        # Translate public flags to user-friendly format
        flags = [BADGE_NAMES[flag[0]] for flag in member.public_flags.all()]
        if not flags:
            flags = "None"
        else:
            flags = "\n".join(flags)
        embed.add_field(name="Discord Badges", value=flags, inline=True)
        if member:
            admin_roles_mentions = "\n".join(role.mention for role in member.roles if role.permissions.administrator)
        embed.add_field(name="Admin Roles", value=admin_roles_mentions, inline=True)

        embed.add_field(name="Animus Staff", value=(True if member.id in staff_ids else False), inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime('%b %d, %Y'), inline=True)

        # Find and display the highest role
        if len(member.roles) > 1:
            highest_role = max(member.roles, key=lambda r: r.position)
            embed.add_field(name="Highest Role", value=highest_role.mention, inline=True)
        else:
            embed.add_field(name="Highest Role", value="None", inline=True)

        # Add an image (the member's avatar)
        embed.set_thumbnail(url=member.avatar.url)

        # Set the footer
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        # Send the embed
        await ctx.send(embed=embed)
    else:
        await ctx.send("User not found.")


@bot.command(name='say', description='Make the bot say something')
async def say(ctx, *, message: str):
    await ctx.send(message)


@bot.tree.command(name="8ball", description="Ask the eightball a question!")
async def eightball(interaction: discord.Interaction, *, question: str):
    """Ask the eightball a question!"""
    responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
                 "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.",
                 "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.",
                 "Outlook not so good.", "Very doubtful."]
    response = random.choice(responses)

    # Prepare the embed
    embed = discord.Embed(title="8ball Response", description=f"Question: {question}\nAnswer: {response}",
                          color=discord.Color(int("302c34", 16)))

    # Send the embed
    await interaction.response.send_message(embed=embed)


@bot.tree.command()
async def info(interaction: discord.Interaction):
    """View the information of the bot"""
    embed = discord.Embed(
        title="<:anmiusforweb:1207930143331459083> Animus Information",
        description="<:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672><:4372lineblue:1207939592859164672>\n"
                    "Animus is a management and fun bot with cutting edge commands and modules. Add the bot and immerse your server members in its many spectacular commands",
        color=discord.Color(int("302c34", 16))
    )
    embed.add_field(name="Information", value="Prefix: ``'!', Mention and Slash commands``\nVersion: ``V3.1.00``",
                    inline=False)
    embed.add_field(name="Development Info", value="Database: ``MongoDB``\nLibraries: ``discord.py, jishaku``",
                    inline=False)
    embed.add_field(name="Operators",
                    value="[@Draunt](https://discord.com/users/968066034051477544), [@Link](https://discord.com/users/1005780651825430600)",
                    inline=False)

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='loa-request', description='Submit a Leave of Absence request')
async def loa_request(interaction: discord.Interaction, time: str, *, reason: str):
    """Submit a Leave of Absence request"""
    time_multipliers = {'d': 86400, 'w': 604800, 'm': 2629746}

    # Parse the time input
    try:
        parsed_time = int(time[:-1]) * time_multipliers[time[-1]]
    except (ValueError, KeyError):
        embed = discord.Embed(
            title='Invalid Time', description='Please provide time in the format: e.g., 1d, 5w, 1m',
            color=discord.Color(int("302c34", 16))
        )
        await interaction.response.send_message(embed=embed)
        return

    success_embed = discord.Embed(
        title='<:loa:1207933665330462780> Request Sent',
        description='Your LOA Request has been saved and sent!',
        color=discord.Color(int("302c34", 16))
    )
    await interaction.response.send_message(embed=success_embed)


@bot.command()
async def trivia(ctx):
    # Fetch trivia data from Open Trivia Database
    response = requests.get('https://opentdb.com/api.php?amount=1&type=multiple')
    trivia_data = response.json()['results'][0]

    # Extract question and correct answer from the trivia data
    question = trivia_data['question']
    correct_answer = trivia_data['correct_answer']
    incorrect_answers = trivia_data['incorrect_answers']

    # Shuffle the correct and incorrect answers together
    answers = incorrect_answers + [correct_answer]
    random.shuffle(answers)

    # Create the embed to display the trivia question
    embed = discord.Embed(title='Trivia', description=question, color=discord.Color(int("302c34", 16)))
    for i, answer in enumerate(answers):
        embed.add_field(name=f'Option {i + 1}', value=answer, inline=False)

    # Send the embed with the trivia question
    await ctx.send(embed=embed)

    # Wait for the user to respond with their answer
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        user_response = await bot.wait_for('message', check=check, timeout=30)
    except asyncio.TimeoutError:
        await ctx.send("Time's up! You didn't answer in time.")
        return

    # Determine if the user's answer is correct
    user_answer = user_response.content.lower()
    if user_answer == correct_answer.lower():
        await ctx.send(f'Correct! The answer is {correct_answer}.')
    else:
        await ctx.send(f'Sorry, the correct answer is {correct_answer}.')


@bot.command()
async def github(ctx, username):
    # Send a GET request to the GitHub API user endpoint
    response = requests.get(f"https://api.github.com/users/{username}")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response and extract the profile information
        profile = response.json()
        # Create an embed to display the profile information
        embed = discord.Embed(title=f"GitHub Profile for {profile['login']}", color=discord.Color(int("302c34", 16)))
        embed.add_field(name="Name", value=profile['name'], inline=True)
        embed.add_field(name="Bio", value=profile['bio'], inline=False)
        embed.add_field(name="Location", value=profile['location'], inline=True)
        embed.add_field(name="Public Repositories", value=profile['public_repos'], inline=True)
        embed.add_field(name="Followers", value=profile['followers'], inline=True)
        embed.add_field(name="Following", value=profile['following'], inline=True)
        embed.set_thumbnail(url=profile['avatar_url'])
        # Send the embed in the channel where the command was invoked
        await ctx.send(embed=embed)
    else:
        # If the request was not successful, send an error message
        await ctx.send("Error fetching GitHub profile.")


class PollView(View):
    def __init__(self, question: str, options: list[str]):
        super().__init__()
        self.question = question
        self.options = options

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        self.stop()


@bot.tree.command(name="getinfo", description="Get a roblox user's info.")
async def getinfo(interaction: discord.Interaction, username: str):
    """Get info on a roblox user."""
    users_json = requests.get(f"https://www.roblox.com/search/users/results?keyword={username}&maxRows=1&startIndex=0")
    users = json.loads(users_json.text)
    user_id = users['UserSearchResults'][0]['UserId']

    profile_json = requests.get(f"https://users.roblox.com/v1/users/{user_id}")
    profile = json.loads(profile_json.text)
    display_name = profile["displayName"]
    created_date = profile["created"]
    description = profile["description"]

    thumbnail_json = requests.get(
        f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=100x100&format=Png&isCircular=false")
    thumbnail = json.loads(thumbnail_json.text)
    thumbnail_url = thumbnail['data'][0]['imageUrl']

    embed = discord.Embed(title=f"{display_name}", url=f"https://www.roblox.com/users/{user_id}/profile",
                          color=discord.Color(int("302c34", 16)))
    embed.set_author(name=f"Roblox User Info For {username}")
    embed.set_footer(text="https://discord.gg/gz6Z6Q6RNP")

    embed.add_field(name="ID", value=f"{user_id}", inline=True)
    embed.add_field(name="Username", value=f"@{username}", inline=True)
    embed.add_field(name="Account Created", value=f"{created_date}", inline=True)
    embed.add_field(name="description", value=f"{description}", inline=False)
    embed.set_thumbnail(url=f"{thumbnail_url}")
    await interaction.response.send_message(embed=embed)


@bot.command()
async def guildcount(ctx, member_id=discord.User.id):
    if member_id in staff_ids:
        '''Show the total number of guilds the bot is in'''
        guild_count = len(bot.guilds)
        await ctx.send(f"The bot is in {guild_count} guilds.")


@bot.tree.command()
async def joke(interaction: discord.Interaction):
    '''Sends a random dad joke'''
    async with aiohttp.ClientSession() as session:
        async with session.get('https://icanhazdadjoke.com/', headers={'Accept': 'application/json'}) as response:
            data = await response.json()
            await interaction.response.send_message(data['joke'])


@bot.tree.command()
async def passapp(interaction: discord.Interaction, member: discord.Member, server_message: str, feedback: str):
    '''Post Passed Application Result'''
    guild_id = interaction.guild.id
    management_role = get_management_roles(guild_id)
    if not any(role.id in management_role for role in interaction.message.author.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.")
        return
    else:
        channel = interaction.channel
        embed = discord.Embed(title=f"{interaction.guild.name} Application Passed.", color=0x00FF00)
        embed.add_field(name="Staff Name", value=member.mention)
        embed.add_field(name="Server Message", value=server_message)
        embed.add_field(name="Feedback", value=feedback)
        embed.add_field(name="Signed By", value=interaction.message.author.mention)
        await interaction.response.send_message("Result Sent")
        await channel.send(member.mention, embed=embed)


def get_management_roles(guild_id):
    pass


@bot.tree.command()
async def failapp(interaction: discord.Interaction, member: discord.Member, feedback: str):
    '''Post Failed Application Result'''
    guild_id = interaction.guild_id
    management_role = interaction.guild.roles.list
    if not any(role.id in management_role for role in interaction.message.author.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.")
        return
    else:
        channel = interaction.channel
        embed = discord.Embed(title=f"{interaction.guild.name} Application Failed.", color=0xFF0000)
        embed.add_field(name="Staff Name", value=member.mention)
        embed.add_field(name="Feedback", value=feedback)
        embed.add_field(name="Signed By", value=interaction.message.author.mention)
        await interaction.response.send_message("Result Sent")
        await channel.send(member.mention, embed=embed)


@bot.tree.command(name='server-info', description="Get info on a guild")
async def server_info(interaction: discord.Interaction):
    """Get info on a guild"""
    server = interaction.guild

    # Basic Information
    created_at = server.created_at.strftime('%B %d, %Y %I:%M %p')
    joined_at = interaction.user.joined_at.strftime('%B %d, %Y %I:%M %p')
    member_count = len(server.members)
    online_members = sum(m.status != discord.Status.offline for m in server.members)
    boosts = server.premium_subscription_count

    # Security
    verification_level = server.verification_level
    explicit_content_filter = server.explicit_content_filter
    verification_gate = "Enabled" if server.verification_level != discord.VerificationLevel.none else "Disabled"

    # Server Configuration

    system_channel = server.system_channel
    rules_channel = discord.utils.get(server.channels, name='guidelines')

    # Channels
    text_channels = sum(1 for channel in server.channels if isinstance(channel, discord.TextChannel))
    voice_channels = sum(1 for channel in server.channels if isinstance(channel, discord.VoiceChannel))
    announcement_channels = sum(
        1 for channel in server.channels if channel.category and channel.category.name == 'Announcement')

    # Roles
    roles = '\n'.join([role.mention for role in server.roles])

    # Features
    features = ', '.join(server.features) if server.features else 'None'

    # Create Embed
    embed = discord.Embed(title="Server Information", color=discord.Color.from_rgb(47, 49, 54))

    # Basic Information
    embed.add_field(name="Name", value=server.name, inline=False)
    embed.add_field(name="Owner", value=server.owner.mention, inline=False)
    embed.add_field(name="Created", value=created_at, inline=False)
    embed.add_field(name="Notifications", value="Only @Mentions", inline=False)
    embed.add_field(name="Members", value=f"{member_count} ({online_members} online)", inline=False)
    embed.add_field(name="Nitro Boosts", value=f"{boosts} Boosts", inline=False)

    # Security
    embed.add_field(name="2FA Settings", value="Not Required", inline=False)
    embed.add_field(name="Verification Level", value=str(verification_level).title(), inline=False)
    embed.add_field(name="Explicit Content Filter", value=explicit_content_filter.name, inline=False)
    embed.add_field(name="Member Verification Gate", value=verification_gate, inline=False)

    # Server Configuration
    embed.add_field(name="System Messages Channel", value=system_channel.mention if system_channel else 'Not Set',
                    inline=False)
    embed.add_field(name="Rules Channel", value=rules_channel.mention if rules_channel else 'Not Set', inline=False)

    # Channels
    text_channels = sum(1 for channel in server.channels if isinstance(channel, discord.TextChannel))
    voice_channels = sum(1 for channel in server.channels if isinstance(channel, discord.VoiceChannel))
    # Roles
    embed.add_field(name="Roles", value=roles, inline=False)

    # Features
    embed.add_field(name="Features", value=features, inline=False)

    # Send the Embed
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='ra-request', description='Submit a Reduced Activity Request')
async def ra_request(interaction: discord.Interaction, time: str, *, reason: str):
    """Submit a Leave of Absence request"""
    # Define time multipliers for days, weeks, and months
    time_multipliers = {'d': 86400, 'w': 604800, 'm': 2629746}

    # Parse the time input
    try:
        parsed_time = int(time[:-1]) * time_multipliers[time[-1]]
    except (ValueError, KeyError):
        # Invalid time format, send an embed with an error message
        embed = discord.Embed(
            title='Invalid Time', description='Please provide time in the format: e.g., 1d, 5w, 1m',
            color=discord.Color(int("302c34", 16))
        )
        await interaction.response.send_message(embed=embed)
        return

    # Successful time parsing, send success message in a green embed
    success_embed = discord.Embed(
        title=f'**{interaction.user.name}**, I sent your request.',
        description=f'Your Reduced Activity (R/A) Request for ``{reason}`` has been sent!',
        color=discord.Color(int("302c34", 16))

    )
    await interaction.response.send_message(embed=success_embed, ephemeral=True)
    print(f"{interaction.user.name} has sent an R/A request for {reason} for {time}")


@bot.tree.command(name="help", description="Get latency info and commands")
async def config(interaction: discord.Interaction):
    select = Select(
        max_values=1,
        min_values=1,
        placeholder="Choose an area to get info on",
        options=[
            discord.SelectOption(
                label="Utility",
                emoji="<:utils:1212597045492195388>",
                description="Get a list of Animus' Utility Commands"
            ),
            discord.SelectOption(
                label="Fun",
                emoji="<:fun:1212596739471839292>",
                description="Get a list of Animus' Fun Commands"
            ),
            discord.SelectOption(
                label="Moderation",
                emoji="<:mod:1212597813909921792>",
                description="Get a list of Animus' Moderation Commands"
            ),
            discord.SelectOption(
                label="Modmail",
                emoji="<:mail:1212598219968872539>",
                description="[COMING SOON]"
            )
        ]
    )
    view = View()
    view.add_item(select)

    async def my_callback(interaction):
        selected_option = select.options[0]  # Assuming the first option was chosen
        for option in select.options:
            if option.label == select.values[0]:
                selected_option = option
                break
        embed = discord.Embed(title=f"Animus Help Center - {selected_option.label}", color=discord.Color.from_rgb(47, 49, 54))
        if selected_option.label == "Utility":
            embed.add_field(name="Utility Commands", value="• cat • doggo • bird • ping • add • getavatar • role-add • role-remove • whois • server-info • say • loa-request • ra-request • info • github • poll • getinfo • passapp • failapp • help")
        elif selected_option.label == "Fun":
            embed.add_field(name="Fun Commands", value="• 8ball, • blackjack, • trivia, • joke, • meme, • coinflip")
        elif selected_option.label == "Moderation":
            embed.add_field(name="Moderation Commands", value="• warn, • mute, • kick, • ban, • purge")
        elif selected_option.label == "Modmail":
            embed.add_field(name="Modmail", value="Modmail feature is coming soon!")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    select.callback = my_callback

    embed = discord.Embed(title="Animus Help Center", color=discord.Color.from_rgb(47, 49, 54))
    embed.add_field(name="This is the help center for Animus! This is where you can get info on the bot, commands and more!", value="Note: Some of these are not slash commands.")

    await interaction.response.send_message(embed=embed, view=view)


@bot.tree.command(name='coinflip', description='Flip a coin and get heads or tails.')
async def coinflip(interaction: discord.Interaction):
    # Randomly select heads or tails
    result = random.choice(['heads', 'tails'])

    # Get the appropriate emoji
    emoji = '🪙' if result == 'heads' else '👑'

    # Send the result back to the user
    embed = discord.Embed(title="<:correct:1204702940015624202> Coinflip", colour=discord.Color.from_rgb(47, 49, 54))
    embed.add_field(name="{emoji} {result}!", value=f"", inline=False)

    await interaction.response.send_message(embed=embed)




bot.run("MTE5OTE4MzQ4NjE0NjMyMjUwMw.G28nFm.WlHJVdnEjgMrEGtfp7C4xKIYSxff4ASA0mCTio")

