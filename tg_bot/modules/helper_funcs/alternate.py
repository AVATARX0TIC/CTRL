from functools import wraps

from telegram import User, Chat, ChatMember, Update, Bot
from telegram import error, ChatAction

from tg_bot import DEL_CMDS, SUDO_USERS


def send_message(message, text,  *args,**kwargs):
	try:
		return message.reply_text(text, *args,**kwargs)
	except error.BadRequest as err:
		if str(err) == "Reply message not found":
			return message.reply_text(text, quote=False, *args,**kwargs)


def typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, bot, *args, **kwargs):
        bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        return func(update, bot,  *args, **kwargs)

    return command_func


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, bot, *args, **kwargs):
            bot.send_chat_action(chat_id=update.effective_chat.id, action=action)
            return func(update, bot,  *args, **kwargs)
        return command_func

    return decorator
