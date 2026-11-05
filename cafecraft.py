#  CafeCraft - Café Ordering and Management System

import tkinter as tk                 
from tkinter import ttk              
from tkinter import messagebox       

# COLOURS AND FONT 
BG_MAIN = "#241A16"      # dark coffee brown (window background)
BG_CARD = "#382820"      # brown (cards / panels)
CARAMEL = "#C58B55"      # primary button + headings
CREAM = "#F3E5D0"        # secondary button + input boxes
TEXT_MAIN = "#FFF7ED"    # main text
TEXT_SOFT = "#D8C3A5"    # light beige secondary text
RED = "#B5493B"          # remove / danger button
FONT_NAME = "Segoe UI"

MENU = {
    "Espresso":          {"category": "Coffee",      "price": 90},
    "Cappuccino":        {"category": "Coffee",      "price": 120},
    "Latte":             {"category": "Coffee",      "price": 140},
    "Mocha":             {"category": "Coffee",      "price": 150},
    "Cold Coffee":       {"category": "Cold Drinks", "price": 130},
    "Chocolate Shake":   {"category": "Cold Drinks", "price": 150},
    "Iced Tea":          {"category": "Cold Drinks", "price": 110},
    "Lemonade":          {"category": "Cold Drinks", "price": 80},
    "Veg Sandwich":      {"category": "Snacks",      "price": 100},
    "French Fries":      {"category": "Snacks",      "price": 90},
    "Veg Burger":        {"category": "Snacks",      "price": 130},
    "Garlic Bread":      {"category": "Snacks",      "price": 110},
    "Chocolate Brownie": {"category": "Desserts",    "price": 110},
    "Cheesecake":        {"category": "Desserts",    "price": 160},
    "Waffle":            {"category": "Desserts",    "price": 140},
}

CATEGORY_ICONS = {"Coffee": "☕", "Cold Drinks": "❄", "Snacks": "♨", "Desserts": "♥"}

# Registered accounts: username -> full name and password (one demo account included)
accounts = {"demo": {"full_name": "Demo User", "password": "demo123"}}

current_user_name = ""     
current_order = {}         
last_receipt = {}          
order_counter = 1000      

login_username_entry = None
login_password_entry = None
signup_entries = {}

# ---------------------- MAIN WINDOW SETUP ----------------------
root = tk.Tk()
root.title("CafeCraft - Café Ordering and Management System")
root.configure(bg=BG_MAIN)
root.minsize(1000, 650)
root.state("zoomed")               

menu_message = tk.StringVar()           
status_text = tk.StringVar()             
order_type = tk.StringVar(value="Dine-in")   
cutlery_needed = tk.IntVar(value=0)          

status_bar = tk.Label(root, textvariable=status_text, font=(FONT_NAME, 11),
                      bg=BG_CARD, fg=TEXT_SOFT, anchor="w", padx=15, pady=4)
status_bar.pack(side="bottom", fill="x")

page_frame = tk.Frame(root, bg=BG_MAIN)
page_frame.pack(fill="both", expand=True)


#  SMALL HELPER FUNCTIONS 
def update_status():
    """Refresh the status bar: who is logged in, items in the order and the total."""
    if current_user_name == "":
        status_text.set("Not logged in")
    else:
        status_text.set(f"Logged in as {current_user_name}   |   "
                        f"Items in order: {count_items(current_order)}   |   "
                        f"Total: ₹{calculate_total(current_order)}")


def clear_page():
    """Remove everything from the shared frame so a new page can be drawn."""
    for widget in page_frame.winfo_children():
        widget.destroy()
    update_status()


def make_button(parent, text, command, style="primary", width=16):
    """Create a button. Using one function keeps all buttons looking the same."""
    if style == "primary":
        bg_colour, text_colour = CARAMEL, BG_MAIN
    elif style == "secondary":
        bg_colour, text_colour = CREAM, BG_MAIN
    else:                                   
        bg_colour, text_colour = RED, "white"
    button = tk.Button(parent, text=text, command=command,
                       bg=bg_colour, fg=text_colour,
                       activebackground=TEXT_SOFT, activeforeground=BG_MAIN,
                       font=(FONT_NAME, 13, "bold"), relief="flat", bd=0,
                       width=width, pady=6, cursor="hand2")
    # Mouse events: change colour when the mouse enters and leaves the button
    button.bind("<Enter>", lambda event: button.config(bg=TEXT_SOFT))
    button.bind("<Leave>", lambda event: button.config(bg=bg_colour))
    return button


def make_entry(parent, show_char=""):
    """Create a text input box. show_char='*' hides what is typed (passwords)."""
    return tk.Entry(parent, font=(FONT_NAME, 14), width=28, bg=CREAM, fg=BG_MAIN,
                    insertbackground=BG_MAIN, relief="flat", show=show_char)


def make_label(parent, text, size=14, bold=False, colour=TEXT_MAIN, bg=BG_MAIN, **options):
    """Create a label with our font and colours."""
    weight = "bold" if bold else "normal"
    return tk.Label(parent, text=text, font=(FONT_NAME, size, weight),
                    fg=colour, bg=bg, **options)


#  ORDER AND BILLING FUNCTIONS 
def add_to_order(item_name):
    """Add one item. If it is already in the order, just increase its quantity."""
    if item_name in current_order:
        current_order[item_name] += 1
    else:
        current_order[item_name] = 1


def calculate_subtotal(item_name, quantity):
    """Item subtotal = unit price x quantity."""
    return MENU[item_name]["price"] * quantity


def calculate_total(order):
    """Total bill = sum of all item subtotals."""
    total = 0
    for item_name, quantity in order.items():
        total += calculate_subtotal(item_name, quantity)
    return total


def count_items(order):
    """Total number of items (counting quantities)."""
    return sum(order.values())


def change_quantity(item_name, change):
    """Increase (+1) or decrease (-1) quantity, then redraw the order page."""
    current_order[item_name] += change
    if current_order[item_name] <= 0:       # quantity reached zero -> remove the item
        del current_order[item_name]
    show_order_page()                        


def remove_item(item_name):
    """Delete an item from the order and redraw the order page."""
    del current_order[item_name]
    show_order_page()


def clear_order():
    """Empty the current order and reset the order options."""
    current_order.clear()
    order_type.set("Dine-in")
    cutlery_needed.set(0)


def generate_receipt_text():
    """Build the receipt text from the REAL order stored in last_receipt."""
    line = "-" * 40
    cutlery_text = "Yes" if last_receipt["cutlery"] == 1 else "No"
    lines = []
    lines.append("CAFECRAFT".center(40))
    lines.append("Café Ordering System".center(40))
    lines.append(line)
    lines.append(f"Order No : {last_receipt['order_number']}")
    lines.append(f"Customer : {current_user_name}")
    lines.append(f"Type     : {last_receipt['order_type']}")
    lines.append(f"Cutlery  : {cutlery_text}")
    lines.append(line)
    lines.append(f"{'Item':<24}{'Qty':>4}{'Amount':>12}")
    lines.append(line)
    for item_name, quantity in last_receipt["items"].items():
        subtotal = calculate_subtotal(item_name, quantity)
        amount_text = "₹" + str(subtotal)
        lines.append(f"{item_name:<24}{quantity:>4}{amount_text:>12}")
    lines.append(line)
    total_text = "₹" + str(last_receipt["total"])
    lines.append(f"{'TOTAL':<28}{total_text:>12}")
    lines.append(line)
    lines.append("Thank you for visiting CafeCraft!".center(40))
    return "\n".join(lines)


#  BUTTON ACTIONS (login, signup, logout, orders)
def handle_login(event=None):
    """Check the username and password typed on the login page."""
    global current_user_name
    username = login_username_entry.get().strip()
    password = login_password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Login Error", "Please enter both username and password.")
        return
    if username in accounts and accounts[username]["password"] == password:
        current_user_name = accounts[username]["full_name"]
        show_home_page()
    else:
        messagebox.showerror("Login Error", "Incorrect username or password.")


def handle_signup():
    """Validate the signup form and save the new account in the accounts dictionary."""
    full_name = signup_entries["full_name"].get().strip()
    username = signup_entries["username"].get().strip()
    password = signup_entries["password"].get()
    confirm = signup_entries["confirm"].get()

    if full_name == "" or username == "" or password == "" or confirm == "":
        messagebox.showerror("Signup Error", "Please fill in all the fields.")
        return
    if username in accounts:
        messagebox.showerror("Signup Error", "This username is already registered.")
        return
    if password != confirm:
        messagebox.showerror("Signup Error", "Passwords do not match.")
        return

    accounts[username] = {"full_name": full_name, "password": password}
    messagebox.showinfo("Success", "Account created! You can now log in.")
    show_login_page()


def logout():
    """Ask for confirmation, then forget the user and any unfinished order."""
    global current_user_name
    if not messagebox.askyesno("Logout", "Do you really want to log out?"):
        return                               
    current_user_name = ""
    clear_order()
    show_login_page()


def add_item_clicked(item_name):
    """Called when 'Add to Order' is pressed on the menu page."""
    add_to_order(item_name)
    menu_message.set(f"✔ {item_name} added!   Quantity: {current_order[item_name]}"
                     f"   |   Items in order: {count_items(current_order)}")
    update_status()


def place_order():
    """Called by the Place Order button on the order page."""
    global order_counter, last_receipt
    if len(current_order) == 0:
        messagebox.showwarning("Empty Order", "Your order is empty. Please add items first.")
        return
    if not messagebox.askyesno("Place Order",
                               f"Total bill is ₹{calculate_total(current_order)}.\n"
                               "Do you want to place this order?"):
        return
    order_counter += 1
    
    last_receipt = {"order_number": "CC-" + str(order_counter),
                    "items": current_order.copy(),
                    "total": calculate_total(current_order),
                    "order_type": order_type.get(),
                    "cutlery": cutlery_needed.get()}
    clear_order()
    show_receipt_page()


def start_new_order():
    """New Order button on the receipt page."""
    clear_order()
    show_menu_page()


#  PAGE 1 : LOGIN
def show_login_page():
    global login_username_entry, login_password_entry
    clear_page()

    make_label(page_frame, "☕ CafeCraft", 48, True, CARAMEL).pack(pady=(60, 0))
    make_label(page_frame, "Café Ordering and Management System", 16,
               colour=TEXT_SOFT).pack()

    card = tk.Frame(page_frame, bg=BG_CARD, padx=55, pady=30)
    card.pack(pady=30)
    make_label(card, "Welcome! Please log in to start ordering.", 14,
               colour=TEXT_SOFT, bg=BG_CARD).pack(pady=(0, 18))

    form = tk.Frame(card, bg=BG_CARD)
    form.pack()
    make_label(form, "Username", 13, True, bg=BG_CARD).grid(row=0, column=0, sticky="w")
    login_username_entry = make_entry(form)
    login_username_entry.grid(row=1, column=0, ipady=6, pady=(2, 14))
    make_label(form, "Password", 13, True, bg=BG_CARD).grid(row=2, column=0, sticky="w")
    login_password_entry = make_entry(form, "*")
    login_password_entry.grid(row=3, column=0, ipady=6, pady=(2, 0))
    login_password_entry.bind("<Return>", handle_login)    

    button_row = tk.Frame(card, bg=BG_CARD)
    button_row.pack(pady=(24, 0))
    make_button(button_row, "Login", handle_login, "primary", 12).pack(side="left", padx=6)
    make_button(button_row, "Sign Up", show_signup_page, "secondary", 12).pack(side="left", padx=6)

    make_label(card, "Demo account:  demo / demo123", 11, colour=TEXT_SOFT,
               bg=BG_CARD).pack(pady=(18, 0))
    login_username_entry.focus()             


#  PAGE 1 (continued) : SIGNUP
def show_signup_page():
    clear_page()
    signup_entries.clear()

    make_label(page_frame, "Create Your Account", 32, True, CARAMEL).pack(pady=(40, 5))
    make_label(page_frame, "Join CafeCraft in a few seconds", 14,
               colour=TEXT_SOFT).pack()

    card = tk.Frame(page_frame, bg=BG_CARD, padx=55, pady=22)
    card.pack(pady=22)

    form = tk.Frame(card, bg=BG_CARD)
    form.pack()

    fields = [("Full Name", "full_name", ""),
              ("Username", "username", ""),
              ("Password", "password", "*"),
              ("Confirm Password", "confirm", "*")]
    row_number = 0
    for label_text, key, show_char in fields:
        make_label(form, label_text, 13, True, bg=BG_CARD).grid(row=row_number, column=0, sticky="w")
        entry = make_entry(form, show_char)
        entry.grid(row=row_number + 1, column=0, ipady=5, pady=(2, 8))
        signup_entries[key] = entry
        row_number += 2

    button_row = tk.Frame(card, bg=BG_CARD)
    button_row.pack(pady=(10, 0))
    make_button(button_row, "Create Account", handle_signup, "primary", 16).pack(side="left", padx=6)
    make_button(button_row, "Back to Login", show_login_page, "secondary", 16).pack(side="left", padx=6)
    signup_entries["full_name"].focus()


#  PAGE 2 : HOME / DASHBOARD
def show_home_page():
    clear_page()

    make_label(page_frame, "☕ CafeCraft", 52, True, CARAMEL).pack(pady=(60, 0))
    make_label(page_frame, f"Welcome, {current_user_name}!", 26, True).pack(pady=(10, 5))
    make_label(page_frame,
               "Freshly brewed coffee, chilled drinks, tasty snacks and sweet desserts,\n"
               "made with love and served with a smile.",
               15, colour=TEXT_SOFT, justify="center").pack(pady=(0, 30))

    button_row = tk.Frame(page_frame, bg=BG_MAIN)
    button_row.pack()
    make_button(button_row, "Browse Menu", show_menu_page, "primary", 20).pack(side="left", padx=12)
    make_button(button_row, "My Order", show_order_page, "secondary", 20).pack(side="left", padx=12)

    about_card = tk.Frame(page_frame, bg=BG_CARD, padx=40, pady=18)
    about_card.pack(pady=35)
    make_label(about_card, "About Us", 17, True, CARAMEL, BG_CARD).pack()
    make_label(about_card,
               "CafeCraft is a cosy little café that serves handcrafted coffee and\n"
               "snacks. Order from your table in just a few clicks!",
               13, colour=TEXT_MAIN, bg=BG_CARD, justify="center").pack(pady=(6, 0))

    make_button(page_frame, "Logout", logout, "danger", 14).pack()


#  PAGE 3 : MENU
def show_menu_page():
    clear_page()
    menu_message.set("Click 'Add to Order' to add an item.")

    make_label(page_frame, "Our Menu", 32, True, CARAMEL).pack(pady=(20, 0))

    cards_frame = tk.Frame(page_frame, bg=BG_MAIN)
    cards_frame.pack(pady=10)

    position = 0
    for item_name, details in MENU.items():
        row_number = position // 5
        column_number = position % 5

        card = tk.Frame(cards_frame, bg=BG_CARD, padx=10, pady=12)
        card.grid(row=row_number, column=column_number, padx=6, pady=7)

        icon = CATEGORY_ICONS[details["category"]]
        make_label(card, icon + " " + item_name, 13, True, TEXT_MAIN, BG_CARD, width=17).pack()
        make_label(card, details["category"] + "  ·  ₹" + str(details["price"]),
                   13, True, CARAMEL, BG_CARD).pack(pady=6)
        
        make_button(card, "Add to Order", lambda n=item_name: add_item_clicked(n),
                    "primary", 13).pack()
        position += 1

    make_label(page_frame, "", 14, True, TEXT_SOFT, textvariable=menu_message).pack(pady=8)

    nav_row = tk.Frame(page_frame, bg=BG_MAIN)
    nav_row.pack()
    make_button(nav_row, "Home", show_home_page, "secondary", 18).pack(side="left", padx=10)
    make_button(nav_row, "View Order / Checkout", show_order_page, "primary", 24).pack(side="left", padx=10)


#  PAGE 4 : ORDER / CHECKOUT
def show_order_page():
    clear_page()

    make_label(page_frame, "Your Order", 32, True, CARAMEL).pack(pady=(18, 8))

    holder = tk.Frame(page_frame, bg=BG_CARD)
    holder.pack()
    canvas = tk.Canvas(holder, bg=BG_CARD, highlightthickness=0)
    table = tk.Frame(canvas, bg=BG_CARD, padx=20, pady=10)
    canvas.create_window((0, 0), window=table, anchor="nw")

    if len(current_order) == 0:
        make_label(table, "Your order is empty. Go back to the menu to add items.",
                   15, False, TEXT_SOFT, BG_CARD, width=50, pady=30).grid(row=0, column=0)
    else:
       
        headings = ["Item", "Price", "Quantity", "Subtotal", ""]
        for column_number, heading in enumerate(headings):
            make_label(table, heading, 13, True, CARAMEL, BG_CARD).grid(row=0, column=column_number, padx=8, pady=4)

        row_number = 1
        for item_name, quantity in current_order.items():
            unit_price = MENU[item_name]["price"]
            subtotal = calculate_subtotal(item_name, quantity)

            make_label(table, item_name, 14, False, TEXT_MAIN, BG_CARD, width=18, anchor="w").grid(row=row_number, column=0, padx=8, pady=3)
            make_label(table, "₹" + str(unit_price), 14, False, TEXT_MAIN, BG_CARD, width=7).grid(row=row_number, column=1, padx=8)

            quantity_cell = tk.Frame(table, bg=BG_CARD)
            quantity_cell.grid(row=row_number, column=2, padx=8)
            make_button(quantity_cell, "-", lambda n=item_name: change_quantity(n, -1), "secondary", 3).pack(side="left")
            make_label(quantity_cell, str(quantity), 14, True, TEXT_MAIN, BG_CARD, width=4).pack(side="left")
            make_button(quantity_cell, "+", lambda n=item_name: change_quantity(n, 1), "secondary", 3).pack(side="left")

            make_label(table, "₹" + str(subtotal), 14, True, TEXT_MAIN, BG_CARD, width=9).grid(row=row_number, column=3, padx=8)
            make_button(table, "Remove", lambda n=item_name: remove_item(n), "danger", 9).grid(row=row_number, column=4, padx=8)
            row_number += 1


    table.update_idletasks()
    canvas.config(width=table.winfo_reqwidth(), height=min(table.winfo_reqheight(), 330),
                  scrollregion=(0, 0, table.winfo_reqwidth(), table.winfo_reqheight()))
    canvas.pack(side="left")
    if table.winfo_reqheight() > 330:
        scrollbar = tk.Scrollbar(holder, command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    options = tk.Frame(page_frame, bg=BG_MAIN)
    options.pack(pady=(12, 0))
    make_label(options, "Order type:", 13, True, CARAMEL).pack(side="left", padx=(0, 8))
    for choice in ("Dine-in", "Takeaway"):
        tk.Radiobutton(options, text=choice, variable=order_type, value=choice,
                       font=(FONT_NAME, 13), bg=BG_MAIN, fg=TEXT_MAIN,
                       selectcolor=BG_CARD, activebackground=BG_MAIN,
                       activeforeground=TEXT_MAIN).pack(side="left", padx=6)
    tk.Checkbutton(options, text="Need cutlery", variable=cutlery_needed,
                   font=(FONT_NAME, 13), bg=BG_MAIN, fg=TEXT_MAIN,
                   selectcolor=BG_CARD, activebackground=BG_MAIN,
                   activeforeground=TEXT_MAIN).pack(side="left", padx=(25, 0))

    ttk.Separator(page_frame, orient="horizontal").pack(fill="x", padx=200, pady=10)
    make_label(page_frame, f"Total Bill:  ₹{calculate_total(current_order)}", 26, True, CARAMEL).pack()

    button_row = tk.Frame(page_frame, bg=BG_MAIN)
    button_row.pack(pady=12)
    make_button(button_row, "Back to Menu", show_menu_page, "secondary", 16).pack(side="left", padx=8)
    make_button(button_row, "Home", show_home_page, "secondary", 12).pack(side="left", padx=8)
    make_button(button_row, "Place Order", place_order, "primary", 16).pack(side="left", padx=8)


#  PAGE 5 : ORDER CONFIRMATION / RECEIPT
def show_receipt_page():
    clear_page()

    make_label(page_frame, "✔ Order Placed Successfully!", 28, True, CARAMEL).pack(pady=(8, 0))
    make_label(page_frame, "Your order is confirmed and is being prepared.", 13,
               colour=TEXT_SOFT).pack()

    receipt_card = tk.Frame(page_frame, bg=CREAM, padx=30, pady=6)
    receipt_card.pack(pady=6)
    
    font_size = 12 if len(last_receipt["items"]) <= 8 else 10
    tk.Label(receipt_card, text=generate_receipt_text(), font=("Courier New", font_size, "bold"),
             bg=CREAM, fg=BG_MAIN, justify="left").pack()

    button_row = tk.Frame(page_frame, bg=BG_MAIN)
    button_row.pack(pady=3)
    make_button(button_row, "New Order", start_new_order, "primary", 16).pack(side="left", padx=8)
    make_button(button_row, "Return to Home", show_home_page, "secondary", 16).pack(side="left", padx=8)
    make_button(button_row, "Logout", logout, "danger", 12).pack(side="left", padx=8)

#  START THE PROGRAM
if __name__ == "__main__":
    show_login_page()      # first page shown
    root.mainloop()        # keeps the window open and waits for clicks
