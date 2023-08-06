import telebot


def auto_answer(bot: telebot.TeleBot):
    def _decorator(callback_query_handler):
        def _callback_query_handler(call: telebot.types.CallbackQuery, *args, **kwargs):
            res = callback_query_handler(call, *args, **kwargs)
            bot.answer_callback_query(call.id)
            return res
        return _callback_query_handler
    return _decorator
