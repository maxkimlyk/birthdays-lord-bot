PARSE_MODE_PLAIN = None
PARSE_MODE_HTML = 'HTML'


def make_google_sheets_edit_link(spreadsheet_id: str) -> str:
    return 'https://docs.google.com/spreadsheets/d/{}/edit'.format(
        spreadsheet_id,
    )
