import telebot
from typing import Union


def auto_answer(bot: telebot.TeleBot, exception_message: Union[None, str]=None):
    def _decorator(callback_query_handler):
        def _callback_query_handler(call: telebot.types.CallbackQuery, *args, **kwargs):
            try:
                res = callback_query_handler(call, *args, **kwargs)
                return res
            except Exception as e:
                if exception_message is not None:
                    bot.send_message(call.message.chat.id, exception_message)
            finally:
                if isinstance(call, telebot.types.CallbackQuery):
                    bot.answer_callback_query(call.id)
        return _callback_query_handler
    return _decorator
