from typing import Callable

from pyrogram.filters import Filter
from pyrogram.handlers.chosen_inline_result_handler import ChosenInlineResultHandler
from pyrogram.handlers.handler import Handler
from pyrogram.handlers.inline_query_handler import InlineQueryHandler
from pyrogram.handlers.message_handler import MessageHandler


def _add_decorator(HandlerType: type[Handler]):
    def bind_handlers(handlers: list[tuple[Handler, int]]):
        def bind_filters_group(*filters: Filter, group: int=0):
            def bind_func(func: Callable):
                handler = HandlerType(func, *filters)
                handlers.append((handler, group))
                return func
            return bind_func
        return bind_filters_group
    return bind_handlers


on_message = _add_decorator(MessageHandler)
on_inline_query = _add_decorator(InlineQueryHandler)
on_chosen_inline_result = _add_decorator(ChosenInlineResultHandler)
