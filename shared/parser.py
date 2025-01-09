from abc import ABC, abstractmethod
from datetime import datetime

class NationalIDParser(ABC):
    @abstractmethod
    def parse(self, national_id: str):
        """Parse the national ID and return extracted information."""
        pass


class EgyptianIDParser(NationalIDParser):
    GOVERNORATES = {
        "01": "Cairo",
        "02": "Alexandria",
        "03": "Port Said",
        "04": "Suez",
        "88": "Abroad"
    }

    def parse(self, national_id):
        national_id = str(national_id)
        if len(national_id) != 14 or not national_id.isdigit():
            raise ValueError("Invalid Egyptian National ID. Must be a 14-digit number.")

        century = {"2": "19", "3": "20"}.get(national_id[0], "Unknown")
        year = national_id[1:3]
        month = national_id[3:5]
        day = national_id[5:7]

        try:
            birth_date = datetime.strptime(f"{century}{year}-{month}-{day}", "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date in National ID.")

        governorate = self.GOVERNORATES.get(national_id[7:9], "Unknown")
        gender = "Male" if int(national_id[9:13]) % 2 != 0 else "Female"

        return {
            "birth_date": birth_date,
            "governorate_code":national_id[7:9],
            "governorate": governorate,
            "gender": gender,
        }

class NationalIDParserFactory:
    _parsers = {
        "EG": EgyptianIDParser(),
    }

    @staticmethod
    def get_parser(country_code: str) -> NationalIDParser:
        parser = NationalIDParserFactory._parsers.get(country_code.upper())
        if not parser:
            raise ValueError(f"No parser available for country code: {country_code}")
        return parser
