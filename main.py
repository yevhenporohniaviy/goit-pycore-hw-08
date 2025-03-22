from models.address_book import AddressBook
from models.record import Record
from datetime import datetime

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Please provide all required arguments."
        except KeyError:
            return "Contact not found."
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    if not phone.isdigit() or len(phone) != 10:
        raise ValueError("Phone number must contain 10 digits.")
    
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    if not new_phone.isdigit() or len(new_phone) != 10:
        raise ValueError("New phone number must contain 10 digits.")
    
    record = book.find(name)
    if record is None:
        raise KeyError()
    record.edit_phone(old_phone, new_phone)
    return "Phone number updated."

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError()
    return "; ".join([phone.value for phone in record.phones])

def show_all(book: AddressBook):
    if not book.data:
        return "No contacts saved."
    return "\n".join(str(record) for record in book.data.values())

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    try:
        datetime.strptime(birthday, "%d.%m.%Y")
    except ValueError:
        raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
    record = book.find(name)
    if record is None:
        raise KeyError()
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError()
    if record.birthday is None:
        return "Birthday not set."
    return record.birthday.value

@input_error
def birthdays(_, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays next week."
    
    result = ["Upcoming birthdays:"]
    for birthday in upcoming:
        result.append(f"{birthday['name']}: {birthday['birthday']} (celebrate on {birthday['congratulation_date']})")
    return "\n".join(result)

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
