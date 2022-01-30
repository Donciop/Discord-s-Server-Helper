import discord
from discord.ext import commands
from discord_slash import cog_ext  # for slash commands
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_option, create_permission
from main import client
import typing
import asyncio
import random


class ManageChannelsCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.newsChannel = client.get_channel(748120165001986128)
        self.botChannel = client.get_channel(888056072538042428)
        self.testChannel = client.get_channel(902710519646015498)

    @cog_ext.cog_slash(  # slash command decorator
        name="dc_mute",  # name that will be displayed in Discord
        description="Mute someone",  # description of the command
        permissions={
            218510314835148802: [
                create_permission(545658751689031699, SlashCommandPermissionType.ROLE, True),
                create_permission(748144455730593792, SlashCommandPermissionType.ROLE, True),
                create_permission(826094492309258291, SlashCommandPermissionType.ROLE, False),
                create_permission(541960938165764096, SlashCommandPermissionType.ROLE, False),
                create_permission(541961631954108435, SlashCommandPermissionType.ROLE, False)
            ]
        },
        guild_ids=[218510314835148802],  # list of server (guilds) id's that have access to this slash command
        options=[
            create_option(  # parameters in slash command
                name="member",  # name of the variable
                description="Choose who to mute",  # description of the parameter
                option_type=6,  # option_type refers to type of the variable ( 3 - STRING )
                required=True  # this parameter is required
            ),
            create_option(
                name="reason",
                description="Reason why to mute someone",
                option_type=3,
                required=False
            )
        ]
    )
    async def dc_mute(self, ctx, member, reason=None):
        if ctx.channel.id != self.botChannel.id and ctx.channel.id != self.testChannel.id and ctx.channel.id != self.newsChannel.id:
            await ctx.send(f"Don't post commands outside of {self.botChannel.mention}")
            return
        await member.edit(mute=True)
        if reason:
            await ctx.send(f"**{member.display_name}** was muted by **{ctx.author.display_name}**, reason: {reason}")
        else:
            await ctx.send(f"**{member.display_name}** was muted by **{ctx.author.display_name}**")

    @cog_ext.cog_slash(  # slash command decorator
        name="dc_deaf",  # name that will be displayed in Discord
        description="Deafen someone",  # description of the command
        permissions={
            218510314835148802: [
                create_permission(545658751689031699, SlashCommandPermissionType.ROLE, True),
                create_permission(748144455730593792, SlashCommandPermissionType.ROLE, True),
                create_permission(826094492309258291, SlashCommandPermissionType.ROLE, False),
                create_permission(541960938165764096, SlashCommandPermissionType.ROLE, False),
                create_permission(541961631954108435, SlashCommandPermissionType.ROLE, False)
            ]
        },
        guild_ids=[218510314835148802],  # list of server (guilds) id's that have access to this slash command
        options=[
            create_option(  # parameters in slash command
                name="member",  # name of the variable
                description="Choose who to deafen",  # description of the parameter
                option_type=6,  # option_type refers to type of the variable ( 3 - STRING )
                required=True  # this parameter is required
            ),
            create_option(
                name="reason",
                description="Reason why to deafen someone",
                option_type=3,
                required=False
            )
        ]
    )
    async def deaf(self, ctx, member, reason=None):
        if ctx.channel.id != self.botChannel.id and ctx.channel.id != self.testChannel.id and ctx.channel.id != self.newsChannel.id:
            await ctx.send(f"Don't post commands outside of {self.botChannel.mention}")
            return
        await member.edit(deafen=True)
        if reason:
            await ctx.send(f"**{member.display_name}** was deafened by **{ctx.author.display_name}**, reason: {reason}")
        else:
            await ctx.send(f"**{member.display_name}** was deafened by **{ctx.author.display_name}**")

    @commands.command()
    @commands.has_permissions(mute_members=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def mute_cf(self, ctx, member: typing.Optional[discord.Member]):
        mute_minutes_self = mute_minutes = 0
        number = random.randint(0, 100)
        if ctx.channel.id != self.botChannel.id and ctx.channel.id != self.newsChannel.id or ctx.channel.id != self.testChannel.id:
            await ctx.send(f"""
            🛑 Mute Coinflip Failed
            You can't post commands outside of {self.botChannel.mention}
            """)
            return
        if not member:
            await ctx.send("""
            🛑 Mute Coinflip Failed
            You have to specify a Discord member to mute
            """)
            return
        if ctx.message.author == member:
            await ctx.send("""
            🛑 Mute Coinflip Failed
            You can't coinflip with yourself
            """)
        if number >= 50:
            await member.edit(mute=True)
            await ctx.send(f"""
            ✅ Mute Coinflip Successful
            You've rolled {str(number)} and muted {member.display_name} for 1 minute
            """)
            mute_minutes += 1
        else:
            await ctx.author.edit(mute=True)
            await ctx.send(f"""
            🛑 Mute Coinflip Failed
            You've rolled {str(number)} and failed to mute {member.display_name}, however you got muted for 3 minutes
            """)
            mute_minutes_self += 3
        if mute_minutes_self > 0:
            await asyncio.sleep(mute_minutes_self * 60)
            await ctx.author.edit(mute=False)
        if mute_minutes > 0:
            await asyncio.sleep(mute_minutes * 60)
            await member.edit(mute=False)


def setup(client):
  client.add_cog(ManageChannelsCommands(client))
