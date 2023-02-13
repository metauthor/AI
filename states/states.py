from aiogram.dispatcher.filters.state import StatesGroup, State

class extraQuestions(StatesGroup):
    q = State()
    t = State()

class setUserTariff(StatesGroup):
    ids = State()
    t = State()

class changeUserTariff(StatesGroup):
    ids = State()
    t = State()

class addAdmins(StatesGroup):
    ids = State()

class removeAdmins(StatesGroup):
    ids = State()

class feedback(StatesGroup):
    text = State()
    state = State()
    photo = State()

class answerTo(StatesGroup):
    ids = State()
    text = State()
    state = State()
    photo = State()


class BotMailing(StatesGroup):
    text = State()
    state = State()
    photo = State()
