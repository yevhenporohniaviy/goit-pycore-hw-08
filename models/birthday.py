from datetime import datetime
from models.field import Field

class Birthday(Field):
    def __init__(self, value):
        try:
            # Convert string to datetime object and validate format
            if isinstance(value, str):
                self.date = datetime.strptime(value, "%d.%m.%Y")
                # Validate year is not in future
                if self.date > datetime.now():
                    raise ValueError("Birthday cannot be in the future")
                super().__init__(value)
            else:
                raise ValueError("Birthday must be a string")
        except ValueError as e:
            if str(e) == "Birthday must be a string" or str(e) == "Birthday cannot be in the future":
                raise e
            raise ValueError("Invalid date format. Use DD.MM.YYYY")