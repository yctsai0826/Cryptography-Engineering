import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import font

class SecurePasswordManagerGUI:
    def __init__(self, root):
        self.manager = SecurePasswordManager()
        self.root = root
        self.root.title("Secure Password Manager")
        self.root.geometry("400x200")  # 设置窗口大小
        self.root.resizable(False, False)  # 禁止调整窗口大小
        
        # 设置字体
        self.font_style = font.Font(family="Helvetica", size=12)
        
        # Add credential button
        self.add_button = tk.Button(root, text="Add Credential", command=self.add_credential,
                                    font=self.font_style, bg="#4CAF50", fg="black")
        self.add_button.pack(pady=10, padx=20, fill=tk.X)
        
        # Autofill credential button
        self.autofill_button = tk.Button(root, text="Autofill Credential", command=self.autofill_credential,
                                         font=self.font_style, bg="#2196F3", fg="black")
        self.autofill_button.pack(pady=10, padx=20, fill=tk.X)

    def add_credential(self):
        protocol_domain = simpledialog.askstring("Input", "Enter the target website with protocol (http/https):", parent=self.root)
        username = simpledialog.askstring("Input", "Account name:", parent=self.root)
        encrypted_password = simpledialog.askstring("Input", "Password:", parent=self.root)
        self.manager.add_credential(protocol_domain, username, encrypted_password)
        messagebox.showinfo("Info", "Successfully added to password manager!")

    def autofill_credential(self):
        protocol_domain = simpledialog.askstring("Input", "Enter the target website with protocol (http/https):", parent=self.root)
        username, decrypted_password = self.manager.autofill_credential(protocol_domain)
        if username is None and decrypted_password.startswith("Autofill is disabled"):
            messagebox.showwarning("Warning", decrypted_password)
        elif username is None:
            messagebox.showerror("Error", "Different domain or using HTTP, cannot autofill.")
        else:
            messagebox.showinfo("Credential", f"Account: {username}\nPassword: {decrypted_password}")

class SecurePasswordManager:
    def __init__(self):
        self.credentials = {}
    
    def add_credential(self, protocol_domain, username, encrypted_password):
        self.credentials[protocol_domain] = (username, encrypted_password)
    
    def autofill_credential(self, protocol_domain):
        if protocol_domain.startswith("http://"):
            return None, "Autofill is disabled for HTTP sites for security reasons."
        elif protocol_domain in self.credentials:
            username, encrypted_password = self.credentials[protocol_domain]
            decrypted_password = encrypted_password  # Simulate decryption
            return username, decrypted_password
        else:
            return None, None

if __name__ == "__main__":
    root = tk.Tk()
    app = SecurePasswordManagerGUI(root)
    root.mainloop()
