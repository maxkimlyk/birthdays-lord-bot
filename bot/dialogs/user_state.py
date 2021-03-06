import aiogram  # type: ignore
import aiogram.dispatcher.filters.state  # type: ignore
import aiogram.contrib.fsm_storage.memory  # type: ignore

class UserState(aiogram.dispatcher.filters.state.StatesGroup):
    on_set_spreadsheet_id = aiogram.dispatcher.filters.state.State()
    on_guide_step2 = aiogram.dispatcher.filters.state.State()
    on_set_notification_time = aiogram.dispatcher.filters.state.State()
