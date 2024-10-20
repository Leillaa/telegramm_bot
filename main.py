from aiogram.utils import executor
from loader import dp, shutdown, log_func, setup_bot_commands
from Handlers import default_handlers, lowprice, highprice, user_handlers, custom


def main() -> None:
    log_func()

    user_handlers.register_user_handlers(dp)
    lowprice.register_lowprice_handlers(dp)
    default_handlers.register_default_handlers(dp)
    highprice.register_highprice_handlers(dp)
    custom.register_custom_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands, on_shutdown=shutdown)


if __name__ == '__main__':
    main()
