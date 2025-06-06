import tkinter as tk
from tkinter import messagebox, simpledialog
import os, json, base64
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend

DATA_FILE = "vault.dat"
SALT_FILE = "salt.bin"
backend = default_backend()

def get_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=backend
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def init_vault_ui():
    pw = simpledialog.askstring("Setup", "Create a master password", show="*")
    confirm = simpledialog.askstring("Setup", "Confirm master password", show="*")
    if not pw or pw != confirm:
        messagebox.showerror("Error", "Passwords do not match.")
        return False
    salt = os.urandom(16)
    key = get_key(pw, salt)
    fernet = Fernet(key)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    with open(DATA_FILE, "wb") as f:
        f.write(fernet.encrypt(json.dumps({}).encode()))
    return True

def load_vault_ui(master_pw):
    try:
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
        key = get_key(master_pw, salt)
        fernet = Fernet(key)
        with open(DATA_FILE, "rb") as f:
            data = f.read()
        return fernet, json.loads(fernet.decrypt(data))
    except Exception as e:
        messagebox.showerror("Error", "Wrong password or corrupted vault.")
        return None, None

def save_vault(fernet, data):
    with open(DATA_FILE, "wb") as f:
        f.write(fernet.encrypt(json.dumps(data).encode()))

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Charlot Password Manager 🔐")
        self.vault = {}
        self.fernet = None

        self.site_listbox = tk.Listbox(root, width=40)
        self.site_listbox.pack(padx=10, pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Add", width=10, command=self.add_entry).grid(row=0, column=0)
        tk.Button(btn_frame, text="View", width=10, command=self.view_entry).grid(row=0, column=1)
        tk.Button(btn_frame, text="Delete", width=10, command=self.delete_entry).grid(row=0, column=2)

        if not os.path.exists(DATA_FILE):
            if not init_vault_ui():
                root.destroy()
                return

        self.unlock_vault()

    def unlock_vault(self):
        pw = simpledialog.askstring("Login", "Enter master password", show="*")
        self.fernet, self.vault = load_vault_ui(pw)
        if self.vault is not None:
            self.refresh_list()
        else:
            self.root.destroy()

    def refresh_list(self):
        self.site_listbox.delete(0, tk.END)
        for site in self.vault:
            self.site_listbox.insert(tk.END, site)

    def add_entry(self):
        site = simpledialog.askstring("Add Site", "Site Name:")
        if not site:
            return
        user = simpledialog.askstring("Username", f"Username for {site}:")
        pwd = simpledialog.askstring("Password", f"Password for {site}:", show="*")
        if user and pwd:
            self.vault[site] = {"username": user, "password": pwd}
            save_vault(self.fernet, self.vault)
            self.refresh_list()

    def view_entry(self):
        selected = self.site_listbox.curselection()
        if not selected:
            return
        site = self.site_listbox.get(selected)
        creds = self.vault.get(site, {})
        messagebox.showinfo(f"{site}", f"Username: {creds['username']}\nPassword: {creds['password']}")

    def delete_entry(self):
        selected = self.site_listbox.curselection()
        if not selected:
            return
        site = self.site_listbox.get(selected)
        if messagebox.askyesno("Confirm", f"Delete {site}?"):
            del self.vault[site]
            save_vault(self.fernet, self.vault)
            self.refresh_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
