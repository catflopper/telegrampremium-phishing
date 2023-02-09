import config
import logging
 
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
 
# log
logging.basicConfig(level=logging.INFO)
 
# init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
 
# prices
PRICE = types.LabeledPrice(label="Telegram Premium", amount=300*100)  # в копейках (руб)
 
 
# buy
@dp.message_handler(commands=['start'])
async def buy(message: types.Message):
    if config.PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Больше свободы, эксклюзивные функции и возможность поддержать Telegram.")
 
    await bot.send_invoice(message.chat.id,
                           title="Telegram Premium",
                           description="Больше свободы, эксклюзивные функции и возможность поддержать Telegram.",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="https://cdn.discordapp.com/attachments/1043799804209287189/1073227096123519106/photo_2023-02-09_15-56-35.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")
 
 
# pre checkout  (must be answered in 10 seconds)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
 
 
# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")
 
    await bot.send_message(message.chat.id,
                           f"Спасибо! Получен платёж на сумму 299,00 RUB. Подписка активирована и будет действовать до 1 Feb 2023 09:32:09 UTC.")
 
 
# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
