from typing import List, Dict


class Formatter:
    header_mapping = {}

    def format_headers(self, headers: str) -> List[str]:
        new_headers = []
        for header in headers:
            new_header = self.header_mapping.get(header, header)
            new_headers.append(new_header)

        return new_headers

    def format_row(self, row_values: Dict[str, str]) -> List[str]:
        raise NotImplementedError
