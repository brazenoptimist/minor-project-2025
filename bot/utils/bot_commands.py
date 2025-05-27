from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from bot.settings import settings


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="👋 Start"),
        BotCommand(command="help", description="👋 Help"),
    ]

    admin_commands = [
        BotCommand(command="botinfo", description="ℹ️ Bot Information")
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())

    for admin_id in settings.admins:
        admin_scope = BotCommandScopeChat(chat_id=admin_id)
        await bot.set_my_commands(admin_commands + commands, admin_scope)