import aiogram  # type: ignore
import aiogram.dispatcher.filters.state  # type: ignore
import aiogram.contrib.fsm_storage.memory  # type: ignore

class UserState(aiogram.dispatcher.filters.state.StatesGroup):
    on_set_spreadsheet_id = aiogram.dispatcher.filters.state.State()
