import pytest
import bot.dialogs.settings

from .test_common import *


@pytest.mark.parametrize(
    'message,expected_value,expected_text',
    [
        (
            '  https://docs.google.com/spreadsheets/d/111-jdisopasdoiwejfjjeifopsodijjdjjskkdklsld/edit?usp=sharing\n',
            '111-jdisopasdoiwejfjjeifopsodijjdjjskkdklsld',
            'Spreadsheet id set successfully!',
        ),
        (
            'https://docs.google.com/',
            None,
            'Sorry but your spreadsheet id seems to be invalid. Check it and try again.',
        ),
    ],
)
@pytest.mark.asyncio
async def test_handle_set_spreadsheet_id_step2(
        mock_context, message, expected_value, expected_text,
):
    state = MockState()
    await bot.dialogs.settings.handle_set_spreadsheet_id_step2(
        mock_context, MockMessage(message), state,
    )
    assert state.finished
    assert mock_context.bot.last_message.text == expected_text

    user_settings = mock_context.settings.get_for_user(MOCK_USER_ID)
    assert user_settings['spreadsheet_id'] == expected_value
