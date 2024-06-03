import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
import random
from sympy import isprime, primitive_root

def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if isprime(num):
            return num

def generate_primitive_root(q):
    return primitive_root(q)

class ImageTreeview(ttk.Treeview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.image_column = None
        self.image_renderer = None
        self.images = {} 

    def set_image_column(self, column_index, renderer):
        self.image_column = column_index
        self.image_renderer = renderer


def calculate_keys():
    global private_keys, public_keys, table, q, alpha
    num_parties = int(num_parties_entry.get())
    num_bits = int(num_bits_entry.get())

    q = generate_prime(num_bits) 
    alpha = generate_primitive_root(q)

    input_window = tk.Toplevel(root)
    input_window.title("Keys List")
    
    private_keys = []
    public_keys = []
    user_photos = []  

    table_frame = ttk.Frame(input_window)
    table_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.8, relheight=0.8)

    table = ImageTreeview(table_frame)
    table["columns"] = ("private_key", "public_key", "shared_key", "common_key", "q","alpha")
    table.heading("#0", text="Party")
    table.heading("image", text="Image")
    table.heading("private_key", text="Private Key")
    table.heading("public_key", text="Public Key")
    table.heading("shared_key", text="Shared Key")
    table.heading("common_key", text="Common Key")
    table.heading("q", text="q")
    table.heading("alpha", text="ALPHA")
    table.column("image", anchor="center")


    for i in range(num_parties):
    
        private_key = random.randint(1, q - 1)  
        private_keys.append(private_key)
        public_key = pow(alpha, private_key, q) 
        public_keys.append(public_key)

        table.insert("", tk.END, iid=f"Party {i+1}", text=f"Party {i+1}",values=(private_key, public_key, "", "", q, alpha))
        
    table.pack(expand=True, fill="both")

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 14))

    def retrieve_private_keys():
        private_keys.clear()
        public_keys.clear()

        for i in range(num_parties):
            private_key = random.randint(1, q - 1)  
            private_keys.append(private_key)
            public_key = pow(alpha, private_key, q)  
            public_keys.append(public_key)
            table.item(f"Party {i+1}", values=(private_key, public_key, "", "", q, alpha))

    confirm_button = ttk.Button(input_window, text="Randomize Private Keys", command=retrieve_private_keys)
    confirm_button.pack()

    calculate_button = ttk.Button(input_window, text="Calculate Shared Keys", command=calculate_shared_keys)
    calculate_button.pack()

def calculate_shared_keys():
    global private_keys, public_keys, table, q, alpha
    num_parties = int(num_parties_entry.get())

    shared_keys = []

    for i in range(num_parties):
        next_party_index = (i + 1) % num_parties
        shared_key = pow(public_keys[next_party_index], private_keys[i], q) 
        shared_keys.append(shared_key)

        table.set(f"Party {i+1}", "shared_key", shared_key)

    common_key = pow(shared_keys[-1], private_keys[0], q)  
    for i in range(num_parties):
        table.set(f"Party {i+1}", "common_key", common_key)

root = tk.Tk()
root.title("Diffie-Hellman Key Exchange")
num_parties_label = ttk.Label(root, text="Number of Parties:", font=("Arial", 14))  
num_parties_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
num_parties_entry = ttk.Entry(root, font=("Arial", 14))  
num_parties_entry.grid(row=0, column=1, padx=5, pady=5)

num_bits_label = ttk.Label(root, text="Number of Bits for Prime Number:", font=("Arial", 14))
num_bits_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
num_bits_entry = ttk.Entry(root, font=("Arial", 14))
num_bits_entry.grid(row=1, column=1, padx=5, pady=5)

calculate_button = ttk.Button(root, text="Calculate Keys", command=calculate_keys, style="TButton")  
calculate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

















