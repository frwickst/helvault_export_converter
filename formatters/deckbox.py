from formatters.base import Formatter
from utils.languages import ISO639_1


class DeckboxFormatter(Formatter):
    header_mapping = {
        "name": "Name",
        "set_name": "Edition",
        "language": "Language",
        "collector_number": None,
        "extras": None,
        "oracle_id": None,
        "quantity": "Count",
        "scryfall_id": None,
        "set_code": None,
    }

    def format_row(self, row_values):
        row_values["Language"] = ISO639_1[row_values["Language"]]

        return list(row_values.values())
