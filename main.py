from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import aioschedule as sch


from users import *
from parse import *

from config import token, ADMINS

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

class Statements(StatesGroup):
    get_sub_state = State()
    del_sut_state = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    if not find_user(message.from_user.id):
        add_user(message.from_user.id)
    await message.answer("Привет!\nЭтот бот отслеживает новые вакансии по дизайну на нескольких сайтах.\nЧтобы воспользоваться этим ботом ты должен/должна быть девушкой разработчика этого бота, либо заплатить 50 рублей.\n По поводу оплаты писать сюда: @seagulls_tea")

@dp.message_handler(commands='all_users')
async def all_users(message: types.Message):
    if message.from_user.id in ADMINS:
        users = get_all()
        for user in users:
            await message.answer(f"{user[0]}  {user[1]}")

@dp.message_handler(commands='get_sub')
async def get_sub_start(message: types.Message):
    if message.from_user.id in ADMINS:
        await Statements.get_sub_state.set()
        await message.answer('Кого нужно подписать?')

@dp.message_handler(state=Statements.get_sub_state)
async def get_sub_fin(message: types.Message, state: FSMContext):
    user = message.text
    if find_user(user):
        get_sub(user)
        await message.answer("Юзер подписан")
    else:
        await message.answer('Такого юзера нет')
    await state.finish()

@dp.message_handler(commands='del_sub')
async def del_sub_start(message: types.Message):
    if message.from_user.id in ADMINS:
        await Statements.del_sut_state.set()
        await message.answer('Кого нужно отписать?')

@dp.message_handler(state=Statements.del_sut_state)
async def get_sub_fin(message: types.Message, state: FSMContext):
    user = message.text
    if find_user(user):
        get_sub(user)
        await message.answer("Юзер отписан")
    else:
        await message.answer('Такого юзера нет')
    await state.finish()

async def do_parse():
    ress = parse()
    if ress:
        ids = get_ids()
        for i in ids:
            for res in ress:
                await bot.send_message(i[0], f"{res[1]}\n\nОплата: {res[3]}\nСрок выполнения: {res[4]}\n\n{res[2]}\n{res[0]}")

async def scheduler():
    sch.every(15).seconds.do(do_parse,)
    while True:
        await sch.run_pending()
        await asyncio.sleep(1)

async def on_startup(x):
    asyncio.create_task(scheduler())

if __name__ == '__main__':
    login()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
