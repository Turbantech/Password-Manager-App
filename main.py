from random import randint, choice, shuffle
from tkinter import *
from tkinter import messagebox
import json
from cryptography.fernet import Fernet
import os


# Generate a key for encryption/decryption
def generate_key():
    """Generate a new key and save it to a file."""
    return Fernet.generate_key()


# Load the key from a file
def load_key():
    """Load the key from the current directory named 'secret.key'."""
    return open("secret.key", "rb").read()

# Save the key to a file
def save_key(key):
    """Save the key to a file named 'secret.key'."""
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


# Initialize or load key
if not os.path.isfile("secret.key"):
    key = generate_key()
    save_key(key)
else:
    key = load_key()

cipher_suite = Fernet(key)


def generate_password():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    password_list = [choice(letters) for _ in range(randint(6, 8))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 3))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 3))]

    password = password_list + password_symbols + password_numbers
    shuffle(password)

    password_real = "".join(password)
    pwd_entry.delete(0, END)
    pwd_entry.insert(0, password_real)


def encrypt_password(password):
    """Encrypt the password using Fernet symmetric encryption."""
    return cipher_suite.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password):
    """Decrypt the password using Fernet symmetric decryption."""
    return cipher_suite.decrypt(encrypted_password.encode()).decode()


def create_json_file_if_not_exists():
    """Create a JSON file if it does not exist."""
    if not os.path.isfile("data.json"):
        with open("data.json", "w") as data_file:
            json.dump({}, data_file)


def save():
    """Save the website, email, and encrypted password to the JSON file."""
    website = website_entry.get()
    email = email_entry.get()
    password = pwd_entry.get()

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")
        return

    encrypted_password = encrypt_password(password)

    new_data = {
        website: {
            "email": email,
            "password": encrypted_password,  # Store the encrypted password
        }
    }

    create_json_file_if_not_exists()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except json.JSONDecodeError:
        data = {}

    data.update(new_data)

    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)

    website_entry.delete(0, END)
    pwd_entry.delete(0, END)
    messagebox.showinfo(title="Success", message="Details saved successfully!")


def find_password():
    """Find and display the details for the given website."""
    website = website_to_retrieve_entry.get()
    if len(website) == 0:
        messagebox.showinfo(title="Oops", message="Please enter a website to retrieve")
        return

    create_json_file_if_not_exists()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except json.JSONDecodeError:
        data = {}

    if website in data:
        email = data[website]["email"]
        encrypted_password = data[website]["password"]
        decrypted_password = decrypt_password(encrypted_password)
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {decrypted_password}")
    else:
        messagebox.showinfo(title="Not Found", message="No details for this website exist")


window = Tk()
window.title("Password Manager")
window.config(padx=60, pady=60)

canvas = Canvas(width=200, height=200)
lock_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_image)
canvas.grid(column=1, row=0)

# Labels
my_website = Label(text="Website: ")
my_website.grid(column=0, row=1)

my_email = Label(text="Email/Username: ")
my_email.grid(column=0, row=2)

my_pwd = Label(text="Password: ")
my_pwd.grid(column=0, row=3)

# Entry Fields
website_entry = Entry(width=34)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=53)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "angela@gmail.com")

pwd_entry = Entry(width=34)
pwd_entry.grid(column=1, row=3)

# Buttons
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=45, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

# New Entry and Button for Retrieve
website_to_retrieve_label = Label(text="Website to Retrieve: ")
website_to_retrieve_label.grid(column=0, row=5)

website_to_retrieve_entry = Entry(width=34)
website_to_retrieve_entry.grid(column=1, row=5)

retrieve_button = Button(text="Retrieve", width=45, command=find_password)
retrieve_button.grid(column=1, row=6, columnspan=2)

create_json_file_if_not_exists()

window.mainloop()



