from aiogram import F, Router
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from bot.config_reader import BotConfig

router = Router()


@router.message(F.new_chat_members)
async def on_user_join(
        message: Message,
        bot_config: BotConfig,
):
    """
    Delete "user joined" service messages (if needed)

    :param message: a service message from Telegram "<user> joined the group"
    :param bot_config: bot config
    """
    if bot_config.remove_joins:
        await message.delete()


@router.message(F.sender_chat, ~F.is_automatic_forward)
async def on_posted_as_channel(
        message: Message,
        bot_config: BotConfig,
        l10n: FluentLocalization,
):
    """
    Delete messages sent on behalf of channels (if needed)

    :param message: a message sent on behalf of channel
    :param bot_config: bot config
    :param l10n: fluent localization object
    """
    if bot_config.auto_ban_channels:
        await message.chat.ban_sender_chat(message.sender_chat.id)
        await message.answer(l10n.format_value("channels-not-allowed"))
        await message.delete()
