import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from cryptography.fernet import Fernet
import os

# ===== Fungsi Enkripsi & Dekripsi =====
def generate_key():
    return Fernet.generate_key()

def encrypt_message():
    message = message_entry.get("1.0", tk.END).strip()
    if not message:
        messagebox.showwarning("Peringatan", "Pesan kosong!")
        return
    key = generate_key()
    f = Fernet(key)
    encrypted = f.encrypt(message.encode())
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, encrypted.decode())
    key_entry.delete(0, tk.END)
    key_entry.insert(0, key.decode())

def decrypt_message():
    encrypted = result_box.get("1.0", tk.END).strip()
    key = key_entry.get().strip()
    if not encrypted or not key:
        messagebox.showwarning("Peringatan", "Pesan terenkripsi atau kunci kosong!")
        return
    try:
        f = Fernet(key.encode())
        decrypted = f.decrypt(encrypted.encode()).decode()
        message_entry.delete("1.0", tk.END)
        message_entry.insert(tk.END, decrypted)
    except Exception as e:
        messagebox.showerror("Error", f"Gagal dekripsi: {e}")

def encrypt_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    key = generate_key()
    f = Fernet(key)
    with open(file_path, 'rb') as f_in:
        data = f_in.read()
    encrypted_data = f.encrypt(data)
    encrypted_path = file_path + '.enc'
    with open(encrypted_path, 'wb') as f_out:
        f_out.write(encrypted_data)
    messagebox.showinfo("Sukses", f"File terenkripsi disimpan sebagai:\n{encrypted_path}\n\nKunci:\n{key.decode()}")

def decrypt_file():
    file_path = filedialog.askopenfilename(title="Pilih File .enc")
    if not file_path:
        return
    key = key_entry.get().strip()
    if not key:
        messagebox.showwarning("Peringatan", "Masukkan kunci dekripsi!")
        return
    try:
        f = Fernet(key.encode())
        with open(file_path, 'rb') as f_in:
            encrypted_data = f_in.read()
        decrypted_data = f.decrypt(encrypted_data)
        output_path = file_path.replace('.enc', '_decrypted')
        with open(output_path, 'wb') as f_out:
            f_out.write(decrypted_data)
        messagebox.showinfo("Sukses", f"File berhasil didekripsi dan disimpan sebagai:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal dekripsi: {e}")

# ===== Tampilan GUI Modern =====
root = tk.Tk()
root.title("Fixencriptor - Modern Enkripsi & Dekripsi")
root.geometry("800x600")
root.configure(bg="#1e1e1e")

font_title = ("Segoe UI", 18, "bold")
font_label = ("Segoe UI", 12)
font_entry = ("Consolas", 11)
accent_color = "#00b894"
bg_card = "#2d3436"

tk.Label(root, text="Fixencriptor", font=font_title, fg=accent_color, bg="#1e1e1e").pack(pady=10)

container = tk.Frame(root, bg=bg_card, padx=20, pady=20, bd=0)
container.pack(padx=20, pady=10, fill="both", expand=True)

tk.Label(container, text="Pesan", font=font_label, fg="white", bg=bg_card).pack(anchor="w")
message_entry = scrolledtext.ScrolledText(container, height=5, font=font_entry, bg="#dfe6e9", wrap=tk.WORD)
message_entry.pack(fill="x", pady=(0, 10))

tk.Label(container, text="Hasil Enkripsi / Dekripsi", font=font_label, fg="white", bg=bg_card).pack(anchor="w")
result_box = scrolledtext.ScrolledText(container, height=5, font=font_entry, bg="#dfe6e9", wrap=tk.WORD)
result_box.pack(fill="x", pady=(0, 10))

tk.Label(container, text="Kunci (untuk dekripsi)", font=font_label, fg="white", bg=bg_card).pack(anchor="w")
key_entry = tk.Entry(container, font=font_entry, bg="#dfe6e9")
key_entry.pack(fill="x", pady=(0, 15))

btn_frame = tk.Frame(container, bg=bg_card)
btn_frame.pack(pady=10)

btn_style = {"font": font_label, "bg": accent_color, "fg": "white", "bd": 0, "padx": 10, "pady": 5}

tk.Button(btn_frame, text="Enkripsi Pesan", command=encrypt_message, **btn_style).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Dekripsi Pesan", command=decrypt_message, **btn_style).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Enkripsi File", command=encrypt_file, **btn_style).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Dekripsi File", command=decrypt_file, **btn_style).grid(row=1, column=1, padx=5, pady=5)

root.mainloop()
