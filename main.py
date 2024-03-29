import settings
import discord
from discord.ext import commands
from discord import *
import random
import datetime as dt

logger = settings.logging.getLogger("bot")



with open("alters.txt", "r") as f:
    alters = [line.strip() for line in f.readlines()]
with open("id.txt", 'r') as f:
    ids = f.readlines()

global alter
alter = random.choice(alters)




def run():

    intents = discord.Intents.all()
    bot = commands.Bot("!", intents=intents)
    

    @bot.event
    async def on_ready():
        global alter
        logger.info(f"BOT : {bot.user} (ID : {bot.user.id})")
        alter = random.choice(alters)


    @bot.command(aliases=['p'],
                 help="show your latency.",
                 description="Show your latency in ms.",
                 brief="Answer with pong and your latency.")
    async def ping(ctx):
        latency = round(bot.latency * 1000)
        await ctx.send(f"Pong ! {latency} ms !")

    
    



    @bot.command()
    async def roll(ctx, role: discord.Role = alter):
        """Roll Command

        Args:
            ctx : The context of the channel
            role (discord.Role, optional): The role to add to the person. Defaults to alter.

        Raises:
            ValueError: If the 2 list doesn't have the same length.
            ValueError: If the searched value isn't in the list
        """
        
        if ctx.channel.id == int(1209468326150148116):
            global alter
            alter = random.choice(alters)
            if len(alters) != len(ids):
                raise ValueError("The 2 list should have the same length.")
            index = alters.index(alter[0:])
            if index > 0:
                alter_id = ids[index]
            else:
                raise ValueError("La valeur n'est pas présente dans la liste")
            await ctx.send(f"Vous avez obtenu {alter}!")
            role_to_add = Guild.get_role(ctx.guild, int(alter_id))
            has_alter = Guild.get_role(ctx.guild, int(1209479085806583808))
            await ctx.message.author.add_roles(role_to_add)
            await ctx.message.author.add_roles(has_alter)
            await ctx.message.author.edit(reason=f"Role assigé via la commande roll: {alter}")
            logger.info(f"Role assigé via la commande roll: {alter}")
        else:
            logger.error(f"{ctx.message.author} is in the wrong channel !")
            await ctx.send(f"Tu es dans le mauvais salon ! Va dans le salon https://discord.com/channels/1086621938480332870/1209468326150148116.")
    
    @bot.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clear(ctx, amount : int):
        """Clear Command

        Args:
            ctx: The context of the channel
            amout (int): Amount of message you want to delete
        """
    async def clear(ctx, amount : int):
        """Clear Command

        Args:
            ctx: The context of the channel
            amout (int): Amount of message you want to delete
        """
        channel = discord.Message.channel
        z = await ctx.channel.purge(limit=int(amount)+1)
        z = await ctx.channel.purge(limit=int(amount)+1)
        await ctx.send(f"Salon Nettoyé ! ({len(z)} messages supprimés)")
    
    @clear.error
    async def clearerror(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Tu N'as pas la permission de nettoyer le salon !")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send("La commande est en cooldown ! Attends un peu avant de rééssayer !")
        else:
            raise error
    
    @bot.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(ctx, channel : discord.TextChannel=None):
        """Lock command

        Args:
            ctx : The context of the channel
            channel (discord.TextChannel, optional): The channel you want to lock. Defaults to current channel.
        """
        """Lock command

        Args:
            ctx : The context of the channel
            channel (discord.TextChannel, optional): The channel you want to lock. Defaults to current channel.
        """
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send('Salon Fermé.')
    
    @bot.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(ctx, channel : discord.TextChannel=None):
        """Unlock Command

        Args:
            ctx : The context of the channel
            channel (discord.TextChannel, optional): The channel you want to unlock. Defaults to current channel.
        """
        """Unlock Command

        Args:
            ctx : The context of the channel
            channel (discord.TextChannel, optional): The channel you want to unlock. Defaults to current channel.
        """
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send('salon Réouvert.')
        
    
    now = dt.datetime.now().strftime("%D/%m/%Y %H:%M:%S")

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def mute(ctx, member: discord.Member):
        """Mute Command

        Args:
            ctx : The context of the channel
            member (discord.Member): The member you want to mute
        """
        """Mute Command

        Args:
            ctx : The context of the channel
            member (discord.Member): The member you want to mute
        """
        role = ctx.guild.get_role(int(1210512003454599198))
        guild = ctx.guild
        await member.add_roles(role) 
        await ctx.send(f"Successfully muted ({member})")
    
    

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def unmute(ctx, member: discord.Member):
        """Unmute Command

        Args:
            ctx : The context of the channel
            member (discord.Member): The member you want to unmute.
        """
        """Unmute Command

        Args:
            ctx : The context of the channel
            member (discord.Member): The member you want to unmute.
        """
        role = ctx.guild.get_role(int(1210512003454599198))
        await member.remove_roles(role)
        await ctx.send(f"{member} a été demute.")



    @bot.command()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kick(ctx, member : discord.Member, reason):
        """Kick Command

        Args:
            ctx : The context of the channel.
            member (discord.Member): The Member you want to kick.
            reason (_type_): The Reason of the kick.
        """
        """Kick Command

        Args:
            ctx : The context of the channel.
            member (discord.Member): The Member you want to kick.
            reason (_type_): The Reason of the kick.
        """
        await member.kick(reason="Kicked by " + str(ctx.author))
        embed = discord.Embed(color=discord.Color.brand_red(), title="Kick", description="Exclusion")
        embed.set_author(name=f"Demandé par {ctx.author}", icon_url=ctx.author.avatar)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_image(url=ctx.guild.icon)
        embed.add_field(name="Infos", value=f"{member.display_name} a été exclue par {ctx.author.display_name}", inline=False)
        embed.add_field(name="Raison", value=reason)


        await ctx.send(embed = embed)

    @kick.error
    async def kick_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Tu n'as pas les permmissions requises")
        else:
            await ctx.send(error)

    @bot.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban(ctx, member : discord.Member, reason):
        """Ban Command

        Args:
            ctx : The context of the channel
            member (discord.Member): The Member you want to ban.
            reason (_type_): The reason of the ban
        """
        """Ban Command

        Args:
            ctx : The context of the channel
            member (discord.Member): The Member you want to ban.
            reason (_type_): The reason of the ban
        """
        await member.ban(reason=reason, delete_message_days=1)
        embed = discord.Embed(color=discord.Color.brand_red(), title="Ban", description="Bannissement")
        embed.set_author(name=f"Demandé par {ctx.author}", icon_url=ctx.author.avatar)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_image(url=ctx.guild.icon)
        embed.add_field(name="Infos", value=f"{member.display_name} a été bannie par {ctx.author.display_name}", inline=False)
        embed.add_field(name="Raison", value=reason)

        await ctx.send(embed = embed)
    
    @ban.error
    async def ban_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Tu n'as pas les permmissions requises")
        else:
            await ctx.send(error)

        
        
        

        
    bot.run(settings.TOKEN, root_logger=True)



if __name__ == '__main__':
    run()
    
