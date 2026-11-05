# Tkinter_Cafe_Management
# CafeCraft — Café Ordering and Management System

A desktop café ordering app built with **Python and Tkinter**. It runs as a single file, uses no database and needs no extra libraries.

**Submitted by:** Shreya Mandal (RA2511028010124)
**Course project:** Application Programming (APP) · B.Tech CSE- CC

## Features

- Login and signup with input validation (empty fields, duplicate username, password mismatch)
- Menu of 15 items in five columns, each with an **Add to Order** button
- Order page with + / − / Remove buttons and a live total bill
- Order type (Dine-in / Takeaway) and a cutlery option
- Confirmation pop-ups and a receipt with an order number (CC-1001, CC-1002, ...)
- Café-themed interface that opens maximised, with hover effects and a status bar

## Pages

Login / Signup → Home → Menu → Order → Receipt

## Screenshots

| Login | Signup | Home |
|---|---|---|
| ![Login](screenshots/login.png) | ![Signup](screenshots/signup.png) | ![Home](screenshots/home.png) |

| Menu | Order | Receipt |
|---|---|---|
| ![Menu](screenshots/menu.png) | ![Order](screenshots/order.png) | ![Receipt](screenshots/receipt.png) |

| Success pop-up | Place Order pop-up |
|---|---|
| ![Success](screenshots/popup-success.png) | ![Place order](screenshots/popup-place-order.png) |

## How to run

1. Install **Python 3.8 or newer**. Tkinter comes with the standard Windows and macOS installers. On Linux: `sudo apt install python3-tk`.
2. Download or clone this repository.
3. In a terminal, inside the project folder, run:

```bash
python cafecraft.py
```

Use `python3` instead of `python` on macOS or Linux.

**Demo account:** username `demo`, password `demo123` (or create your own on the Signup page).

## Tkinter concepts used

| Concept | Where |
|---|---|
| `Frame` with `pack()` and `grid()` | One shared page frame redrawn for every page |
| `Label`, `Entry`, `Button` | All pages (`show="*"` hides passwords) |
| `Radiobutton` + `StringVar` | Order type |
| `Checkbutton` + `IntVar` | Cutlery option |
| `Canvas` + `Scrollbar` | Scrollable order table |
| `messagebox` | `showerror`, `showinfo`, `showwarning`, `askyesno` |
| `bind()` events | Enter key to log in, hover colours |
| `lambda n=item_name` | Gives each menu button its own item |
| Dictionaries | `MENU`, `accounts`, `current_order` |

## Code structure

- **Data:** menu, accounts and the current order are kept in dictionaries
- **Helpers:** `make_button`, `make_label`, `make_entry` keep every page uniform
- **Pages:** `show_login_page`, `show_signup_page`, `show_home_page`, `show_menu_page`, `show_order_page`, `show_receipt_page`
- **Logic:** `handle_login`, `handle_signup`, `add_to_order`, `change_quantity`, `calculate_total`, `place_order`

## Limitations and future scope

- Data is lost when the program closes, because nothing is saved to disk
- Passwords are stored as plain text

Possible improvements: SQLite database, hashed passwords, an admin screen to edit the menu, order history and PDF receipts.
