import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Setting up the bot's intents. We need message content for command processing
intents = discord.Intents.default()
intents.message_content = True

# Creating our bot instance with '!' as the command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

# The name of the channel where we'll handle music commands
COMANDO_CANAL_NOMBRE = 'sala-de-musica'

# This class handles all our music control buttons
class ControlButtons(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    # Play/Pause button
    @discord.ui.button(emoji="⏯️", style=discord.ButtonStyle.green, custom_id="play_pause")
    async def play_pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        ctx = await self.bot.get_context(interaction.message)
        music_cog = self.bot.get_cog('Music')
        
        if ctx.voice_client is None:
            await interaction.followup.send("No estoy conectado a un canal de voz.", ephemeral=True)
            return

        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await interaction.followup.send("Reproducción reanudada.", ephemeral=True)
        elif ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await interaction.followup.send("Reproducción pausada.", ephemeral=True)
        else:
            if music_cog and ctx.guild.id in music_cog.now_playing:
                current_song = music_cog.now_playing[ctx.guild.id]
                await interaction.followup.send(f"No hay nada reproduciéndose actualmente. Última canción en cola: {current_song['title']}", ephemeral=True)
            else:
                await interaction.followup.send("No hay nada en la cola de reproducción.", ephemeral=True)

    # Skip button
    @discord.ui.button(emoji="⏭️", style=discord.ButtonStyle.primary, custom_id="skip")
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        ctx = await self.bot.get_context(interaction.message)
        music_cog = self.bot.get_cog('Music')
        if music_cog:
            await music_cog.skip(ctx)
            await interaction.response.send_message("Canción saltada.", ephemeral=True)
        else:
            await interaction.response.send_message("Error: No se pudo acceder al cog de música.", ephemeral=True)

    # Stop button
    @discord.ui.button(emoji="⏹️", style=discord.ButtonStyle.red, custom_id="stop")
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        ctx = await self.bot.get_context(interaction.message)
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await interaction.response.send_message("Reproducción detenida y bot desconectado.", ephemeral=True)
        else:
            await interaction.response.send_message("El bot no está conectado a ningún canal de voz.", ephemeral=True)

    # Queue button
    @discord.ui.button(emoji="🔀", style=discord.ButtonStyle.secondary, custom_id="queue")
    async def queue(self, interaction: discord.Interaction, button: discord.ui.Button):
        music_cog = self.bot.get_cog('Music')
        if music_cog:
            if interaction.guild.id in music_cog.queue and music_cog.queue[interaction.guild.id]:
                queue_list = "\n".join([f"{i+1}. {song['title']}" for i, song in enumerate(music_cog.queue[interaction.guild.id])])
                await interaction.response.send_message(f"Cola actual:\n{queue_list}", ephemeral=True)
            else:
                await interaction.response.send_message("La cola está vacía.", ephemeral=True)
        else:
            await interaction.response.send_message("Error: No se pudo acceder al cog de música.", ephemeral=True)

    # Volume down button
    @discord.ui.button(emoji="🔉", style=discord.ButtonStyle.secondary, custom_id="volume_down")
    async def volume_down(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.defer(ephemeral=True)
            ctx = await self.bot.get_context(interaction.message)
            music_cog = self.bot.get_cog('Music')
            if music_cog and ctx.voice_client:
                current_volume = int(music_cog.volume.get(ctx.guild.id, 1.0) * 100)
                new_volume = max(0, current_volume - 10)
                await music_cog.set_volume(ctx, new_volume)
                await interaction.followup.send(f"Volumen bajado al {new_volume}%", ephemeral=True)
            else:
                await interaction.followup.send("No se pudo ajustar el volumen. Asegúrate de que el bot esté reproduciendo música.", ephemeral=True)
        except Exception as e:
            print(f"Error en volume_down: {str(e)}")
            await interaction.followup.send(f"Ocurrió un error: {str(e)}", ephemeral=True)

    # Volume up button
    @discord.ui.button(emoji="🔊", style=discord.ButtonStyle.secondary, custom_id="volume_up")
    async def volume_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.defer(ephemeral=True)
            ctx = await self.bot.get_context(interaction.message)
            music_cog = self.bot.get_cog('Music')
            if music_cog and ctx.voice_client:
                current_volume = int(music_cog.volume.get(ctx.guild.id, 1.0) * 100)
                new_volume = min(100, current_volume + 10)
                await music_cog.set_volume(ctx, new_volume)
                await interaction.followup.send(f"Volumen subido al {new_volume}%", ephemeral=True)
            else:
                await interaction.followup.send("No se pudo ajustar el volumen. Asegúrate de que el bot esté reproduciendo música.", ephemeral=True)
        except Exception as e:
            print(f"Error en volume_up: {str(e)}")
            await interaction.followup.send(f"Ocurrió un error: {str(e)}", ephemeral=True)

    # Join button
    @discord.ui.button(emoji="➕", style=discord.ButtonStyle.primary, custom_id="join")
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.defer(ephemeral=True)
            if interaction.user.voice:
                channel = interaction.user.voice.channel
                if interaction.guild.voice_client:
                    await interaction.guild.voice_client.move_to(channel)
                else:
                    await channel.connect()
                await interaction.followup.send(f"Me he unido al canal {channel.name}", ephemeral=True)
            else:
                await interaction.followup.send("Necesitas estar en un canal de voz para usar este comando.", ephemeral=True)
        except Exception as e:
            print(f"Error en join: {str(e)}")
            await interaction.followup.send(f"Ocurrió un error al intentar unirme: {str(e)}", ephemeral=True)

# This function creates our help message
def create_help_message():
    return (
        "```md\n"
        "# Comandos del bot de música\n\n"
        "* !play <canción/URL>: Reproduce una canción\n"
        "* !pause: Pausa la reproducción\n"
        "* !resume: Reanuda la reproducción\n"
        "* !skip: Salta a la siguiente canción\n"
        "* !queue: Muestra la cola de reproducción\n"
        "* !playlist <nombre>: Carga una playlist\n"
        "* !save_playlist <nombre>: Guarda la cola actual como playlist\n"
        "* !load_playlist <nombre>: Carga una playlist guardada\n"
        "* !delete_playlist <nombre>: Elimina una playlist guardada\n"
        "* !list_playlists: Muestra tus playlists guardadas\n"
        "* !show_playlist <nombre>: Muestra las canciones de una playlist\n"
        "\nPara más comandos, usa !help\n"
        "```"
    )

# This event runs when the bot is ready
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    for guild in bot.guilds:
        print(f"Verificando permisos en {guild.name}")
        permissions = guild.me.guild_permissions
        if not permissions.connect or not permissions.speak:
            print(f"¡Advertencia! El bot no tiene los permisos necesarios en {guild.name}")
            print(f"Conectar: {permissions.connect}, Hablar: {permissions.speak}")
        await crear_canal_comandos(guild)

# This event runs when the bot joins a new guild
@bot.event
async def on_guild_join(guild):
    await crear_canal_comandos(guild)

# This function creates the command channel in a guild
async def crear_canal_comandos(guild):
    try:
        if not guild.me.guild_permissions.manage_channels:
            print(f"El bot no tiene permisos para crear canales en {guild.name}")
            return

        canal = discord.utils.get(guild.text_channels, name=COMANDO_CANAL_NOMBRE)
        if not canal:
            print(f"Creando canal '{COMANDO_CANAL_NOMBRE}' en {guild.name}")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(send_messages=True),
                guild.me: discord.PermissionOverwrite(send_messages=True, manage_messages=True)
            }
            canal = await guild.create_text_channel(COMANDO_CANAL_NOMBRE, overwrites=overwrites)
            print(f"Canal '{COMANDO_CANAL_NOMBRE}' creado en {guild.name}")
            
            # Sending the help message
            help_message = create_help_message()
            await canal.send(help_message)
            
            # Sending the control buttons
            await canal.send("Controles de música:", view=ControlButtons(bot))
            print(f"Mensaje de controles enviado en {guild.name}")
    except discord.errors.Forbidden:
        print(f"El bot no tiene permisos para crear canales en {guild.name}")
    except Exception as e:
        print(f"Error al crear el canal en {guild.name}: {str(e)}")

# This event handles all incoming messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name == COMANDO_CANAL_NOMBRE:
        # Process commands before deleting messages
        await bot.process_commands(message)
        
        # Delete all messages except the queue and controls
        async for msg in message.channel.history(limit=None):
            if msg.author != bot.user or (not msg.content.startswith("Cola actual:") and not msg.content.startswith("Controles de música:")):
                try:
                    await msg.delete()
                except discord.errors.Forbidden:
                    print(f"No se pudo borrar un mensaje en {message.guild.name}")
    else:
        ctx = await bot.get_context(message)
        if ctx.valid:
            canal_comandos = discord.utils.get(message.guild.channels, name=COMANDO_CANAL_NOMBRE)
            if canal_comandos:
                await message.channel.send(f"Por favor, usa los comandos en el canal {canal_comandos.mention}")
            else:
                print(f"No se encontró el canal '{COMANDO_CANAL_NOMBRE}' en {message.guild.name}")
                await crear_canal_comandos(message.guild)
        
        # Process commands outside the command channel
        await bot.process_commands(message)

# This command forces the creation of the music channel (admin only)
@bot.command()
@commands.has_permissions(administrator=True)
async def force_create_channel(ctx):
    """Command to force the creation of the music channel"""
    await crear_canal_comandos(ctx.guild)
    await ctx.send("Se ha intentado crear el canal de música.")

# This command updates the help message and control buttons
@bot.command()
async def update_help(ctx):
    if ctx.channel.name == COMANDO_CANAL_NOMBRE:
        # Delete old messages
        await ctx.channel.purge(limit=100)
        
        # Send the new help message
        help_message = create_help_message()
        await ctx.channel.send(help_message)
        
        # Send the control buttons
        await ctx.channel.send("Controles de música:", view=ControlButtons(bot))
        
        await ctx.send("Mensaje de ayuda actualizado.", delete_after=5)
    else:
        await ctx.send("Este comando solo puede usarse en el canal de música.")

# Our main function that runs the bot
async def main():
    async with bot:
        await bot.load_extension('cogs.music')
        await bot.start(TOKEN)

# This is where we start our bot, with error handling and auto-restart
if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("Bot stopped manually.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            print("Restarting the bot in 5 seconds...")
            asyncio.sleep(5)