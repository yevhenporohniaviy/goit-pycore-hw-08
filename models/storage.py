import pickle
from models.address_book import AddressBook

def save_data(book, filename="addressbook.pkl"):
    """Save the address book to a file using pickle serialization"""
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    """Load the address book from a file using pickle deserialization"""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Return a new address book if file not found