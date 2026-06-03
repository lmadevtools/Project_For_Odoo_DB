"""
main_gui.py Tkinter GUI for the inventory management system
Run : python main_gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from Classes.inventory import Inventory

# ======================================================================
# Theme / Colors
# ======================================================================

BG_SIDEBAR   = "#2C3E50"
BG_MAIN      = "#F0F3F4"
BG_CARD      = "#FFFFFF"
BG_BTN       = "#2980B9"
BG_BTN_HOVER = "#1A6FA0"
BG_BTN_RED   = "#E74C3C"
BG_BTN_GREEN = "#27AE60"
FG_SIDEBAR   = "#ECF0F1"
FG_TITLE     = "#2C3E50"
FG_LABEL     = "#555555"
FONT_TITLE   = ("Helvetica", 16, "bold")
FONT_SUB     = ("Helvetica", 11, "bold")
FONT_BODY    = ("Helvetica", 10)
FONT_BTN     = ("Helvetica", 10, "bold")
FONT_NAV     = ("Helvetica", 11)


# ======================================================================
# Main App
# ======================================================================

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Inventory Management")
        self.geometry("1100x680")
        self.resizable(True, True)
        self.configure(bg=BG_MAIN)

        self.inv = Inventory()

        self._build_layout()
        self._show_frame("products")

    def _build_layout(self):
        # --- Sidebar ---
        self.sidebar = tk.Frame(self, bg=BG_SIDEBAR, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar, text="MANAGEMENT",
            bg=BG_SIDEBAR, fg=FG_SIDEBAR,
            font=("Helvetica", 13, "bold"), pady=20
        ).pack(fill="x")

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10)

        self._nav_buttons = {}
        nav_items = [
            ("📦  Products",  "products"),
            ("👤  Customers", "customers"),
            ("📋  Orders",    "orders"),
            ("📊  Reports",   "reports"),
        ]
        for label, key in nav_items:
            btn = tk.Button(
                self.sidebar, text=label,
                bg=BG_SIDEBAR, fg=FG_SIDEBAR,
                font=FONT_NAV, anchor="w", padx=20,
                relief="flat", cursor="hand2",
                command=lambda k=key: self._show_frame(k)
            )
            btn.pack(fill="x", pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#34495E"))
            btn.bind("<Leave>", lambda e, b=btn, k=key: b.config(
                bg="#1A6FA0" if self._current == k else BG_SIDEBAR
            ))
            self._nav_buttons[key] = btn

        # --- Main content area ---
        self.content = tk.Frame(self, bg=BG_MAIN)
        self.content.pack(side="left", fill="both", expand=True)

        self._frames = {}
        for FrameClass, key in [
            (ProductsFrame,  "products"),
            (CustomersFrame, "customers"),
            (OrdersFrame,    "orders"),
            (ReportsFrame,   "reports"),
        ]:
            frame = FrameClass(self.content, self)
            self._frames[key] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._current = None

    def _show_frame(self, key):
        self._current = key
        # Update nav highlight
        for k, btn in self._nav_buttons.items():
            btn.config(bg="#1A6FA0" if k == key else BG_SIDEBAR)
        # Refresh and raise frame
        frame = self._frames[key]
        frame.refresh()
        frame.lift()


# ======================================================================
# Helper widgets
# ======================================================================

def make_button(parent, text, command, color=BG_BTN, width=18):
    btn = tk.Button(
        parent, text=text, command=command,
        bg=color, fg="white", font=FONT_BTN,
        relief="flat", cursor="hand2", width=width, pady=4
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=_darken(color)))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn


def _darken(hex_color):
    mapping = {
        BG_BTN:       BG_BTN_HOVER,
        BG_BTN_RED:   "#C0392B",
        BG_BTN_GREEN: "#1E8449",
    }
    return mapping.get(hex_color, hex_color)


def make_table(parent, columns, height=15):
    frame = tk.Frame(parent, bg=BG_CARD)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
        background=BG_CARD, foreground=FG_LABEL,
        rowheight=26, fieldbackground=BG_CARD, font=FONT_BODY
    )
    style.configure("Treeview.Heading",
        background=BG_SIDEBAR, foreground="white",
        font=("Helvetica", 10, "bold")
    )
    style.map("Treeview", background=[("selected", "#2980B9")])

    tree = ttk.Treeview(frame, columns=columns, show="headings", height=height)
    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, anchor="w", width=120)

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")
    return frame, tree


def ask_str(title, prompt, required=True):
    while True:
        val = simpledialog.askstring(title, prompt)
        if val is None:
            return None   # cancelled
        val = val.strip()
        if required and not val:
            messagebox.showwarning("Required", "This field is required.")
            continue
        return val


def ask_float(title, prompt, min_val=None):
    while True:
        val = simpledialog.askfloat(title, prompt)
        if val is None:
            return None
        if min_val is not None and val < min_val:
            messagebox.showwarning("Invalid", f"Minimum value : {min_val}")
            continue
        return val


def ask_int(title, prompt, min_val=None):
    while True:
        val = simpledialog.askinteger(title, prompt)
        if val is None:
            return None
        if min_val is not None and val < min_val:
            messagebox.showwarning("Invalid", f"Minimum value : {min_val}")
            continue
        return val


# ======================================================================
# Products Frame
# ======================================================================

class ProductsFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app

        # Title
        tk.Label(self, text="Products", bg=BG_MAIN, fg=FG_TITLE,
                 font=FONT_TITLE, anchor="w", padx=20, pady=15).pack(fill="x")

        # Buttons
        btn_frame = tk.Frame(self, bg=BG_MAIN)
        btn_frame.pack(fill="x", padx=20, pady=(0, 10))
        make_button(btn_frame, "+ Add product",   self._add_product,   BG_BTN_GREEN).pack(side="left", padx=5)
        make_button(btn_frame, "▲ Add stock",      self._add_stock,     BG_BTN).pack(side="left", padx=5)
        make_button(btn_frame, "▼ Remove stock",   self._remove_stock,  BG_BTN).pack(side="left", padx=5)
        make_button(btn_frame, "Archive",          self._archive,       BG_BTN_RED).pack(side="left", padx=5)
        make_button(btn_frame, "Show archived",    self._show_archived, "#7F8C8D").pack(side="left", padx=5)

        # Table
        cols = ("ID", "Name", "Category", "Price (€)", "Stock", "Min. Stock", "Status")
        tbl_frame, self.tree = make_table(self, cols)
        tbl_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for p in self.app.inv.list_products(include_archived=True):
            status = "Active" if p.active else "Archived"
            low    = " ⚠" if p.is_low_stock() and p.active else ""
            self.tree.insert("", "end", values=(
                p.product_id, p.name, p.category,
                f"{p.price:.2f}", f"{p.quantity}{low}",
                p.minimum_stock, status
            ))

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selection", "Please select a product.")
            return None
        return self.tree.item(sel[0])["values"][0]

    def _add_product(self):
        name  = ask_str("New product", "Name")
        if name is None: return
        price = ask_float("New product", "Price (€)", min_val=0)
        if price is None: return
        qty   = ask_int("New product", "Initial quantity", min_val=0)
        if qty is None: return
        mstock = ask_int("New product", "Minimum stock", min_val=0)
        if mstock is None: return
        cat = ask_str("New product", "Category (default: General)", required=False) or "General"
        try:
            self.app.inv.add_product(name, price, qty, mstock, cat)
            self.refresh()
            messagebox.showinfo("Success", f"Product '{name}' created.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _add_stock(self):
        pid = self._selected_id()
        if pid is None: return
        amount = ask_int("Add stock", "Quantity to add", min_val=1)
        if amount is None: return
        reason = ask_str("Add stock", "Reason (optional)", required=False) or ""
        try:
            self.app.inv.add_stock_to_product(str(pid), amount, reason)
            self.refresh()
            messagebox.showinfo("Success", f"{amount} units added.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _remove_stock(self):
        pid = self._selected_id()
        if pid is None: return
        amount = ask_int("Remove stock", "Quantity to remove", min_val=1)
        if amount is None: return
        reason = ask_str("Remove stock", "Reason (optional)", required=False) or ""
        try:
            self.app.inv.remove_stock_from_product(str(pid), amount, reason)
            self.refresh()
            messagebox.showinfo("Success", f"{amount} units removed.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _archive(self):
        pid = self._selected_id()
        if pid is None: return
        if not messagebox.askyesno("Confirm", f"Archive product {pid}?"):
            return
        try:
            self.app.inv.archive_product(str(pid))
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _show_archived(self):
        self.refresh()


# ======================================================================
# Customers Frame
# ======================================================================

class CustomersFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app

        tk.Label(self, text="Customers", bg=BG_MAIN, fg=FG_TITLE,
                 font=FONT_TITLE, anchor="w", padx=20, pady=15).pack(fill="x")

        btn_frame = tk.Frame(self, bg=BG_MAIN)
        btn_frame.pack(fill="x", padx=20, pady=(0, 10))
        make_button(btn_frame, "+ Add customer", self._add_customer, BG_BTN_GREEN).pack(side="left", padx=5)
        make_button(btn_frame, "Archive",        self._archive,      BG_BTN_RED).pack(side="left", padx=5)

        cols = ("ID", "Name", "Email", "Phone", "Status")
        tbl_frame, self.tree = make_table(self, cols)
        tbl_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for c in self.app.inv.list_customers(include_archived=True):
            status = "Active" if c.active else "Archived"
            self.tree.insert("", "end", values=(
                c.customer_id, c.name, c.email, c.phone or "-", status
            ))

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selection", "Please select a customer.")
            return None
        return self.tree.item(sel[0])["values"][0]

    def _add_customer(self):
        name  = ask_str("New customer", "Name")
        if name is None: return
        email = ask_str("New customer", "Email")
        if email is None: return
        phone = ask_str("New customer", "Phone (optional)", required=False) or ""
        try:
            self.app.inv.add_customer(name, email, phone)
            self.refresh()
            messagebox.showinfo("Success", f"Customer '{name}' created.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _archive(self):
        cid = self._selected_id()
        if cid is None: return
        if not messagebox.askyesno("Confirm", f"Archive customer {cid}?"):
            return
        try:
            c = self.app.inv.get_customer(str(cid))
            c.archive()
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ======================================================================
# Orders Frame
# ======================================================================

class OrdersFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app

        tk.Label(self, text="Orders", bg=BG_MAIN, fg=FG_TITLE,
                 font=FONT_TITLE, anchor="w", padx=20, pady=15).pack(fill="x")

        btn_frame = tk.Frame(self, bg=BG_MAIN)
        btn_frame.pack(fill="x", padx=20, pady=(0, 10))
        make_button(btn_frame, "+ New order",   self._create_order,  BG_BTN_GREEN).pack(side="left", padx=5)
        make_button(btn_frame, "+ Add line",    self._add_line,      BG_BTN).pack(side="left", padx=5)
        make_button(btn_frame, "✔ Confirm",     self._confirm,       BG_BTN_GREEN).pack(side="left", padx=5)
        make_button(btn_frame, "✔ Mark done",   self._mark_done,     BG_BTN).pack(side="left", padx=5)
        make_button(btn_frame, "✘ Cancel",      self._cancel,        BG_BTN_RED).pack(side="left", padx=5)

        # Order list (top)
        tk.Label(self, text="Orders", bg=BG_MAIN, fg=FG_LABEL,
                 font=FONT_SUB, anchor="w", padx=20).pack(fill="x")
        cols_o = ("Order ID", "Customer", "Status", "Date", "Total (€)")
        tbl_o, self.tree_orders = make_table(self, cols_o, height=8)
        tbl_o.pack(fill="x", padx=20, pady=(0, 10))
        self.tree_orders.bind("<<TreeviewSelect>>", self._on_order_select)

        # Lines (bottom)
        tk.Label(self, text="Order lines", bg=BG_MAIN, fg=FG_LABEL,
                 font=FONT_SUB, anchor="w", padx=20).pack(fill="x")
        cols_l = ("Product ID", "Product", "Qty", "Unit price (€)", "Subtotal (€)")
        tbl_l, self.tree_lines = make_table(self, cols_l, height=6)
        tbl_l.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def refresh(self):
        self.tree_orders.delete(*self.tree_orders.get_children())
        self.tree_lines.delete(*self.tree_lines.get_children())
        for o in self.app.inv.list_orders():
            self.tree_orders.insert("", "end", values=(
                o.order_id, o.customer.name,
                o.status.upper(), o.created_at[:10],
                f"{o.total:.2f}"
            ))

    def _on_order_select(self, event):
        self.tree_lines.delete(*self.tree_lines.get_children())
        sel = self.tree_orders.selection()
        if not sel: return
        oid = self.tree_orders.item(sel[0])["values"][0]
        try:
            order = self.app.inv.get_order(str(oid))
            for line in order.lines:
                self.tree_lines.insert("", "end", values=(
                    line.product.product_id,
                    line.product.name,
                    line.quantity,
                    f"{line.unit_price:.2f}",
                    f"{line.subtotal:.2f}"
                ))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _selected_order_id(self):
        sel = self.tree_orders.selection()
        if not sel:
            messagebox.showwarning("Selection", "Please select an order.")
            return None
        return str(self.tree_orders.item(sel[0])["values"][0])

    def _create_order(self):
        customers = self.app.inv.list_customers()
        if not customers:
            messagebox.showwarning("No customers", "Please create a customer first.")
            return
        options = [f"{c.customer_id} — {c.name}" for c in customers]
        win = _PickerDialog(self, "New order", "Select a customer :", options)
        self.wait_window(win)
        if win.result is None: return
        cid = customers[win.result].customer_id
        try:
            order = self.app.inv.create_order(cid)
            self.refresh()
            messagebox.showinfo("Success", f"Order {order.order_id} created.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _add_line(self):
        oid = self._selected_order_id()
        if oid is None: return
        products = self.app.inv.list_products()
        if not products:
            messagebox.showwarning("No products", "No products available.")
            return
        options = [f"{p.product_id} — {p.name} (stock: {p.quantity})" for p in products]
        win = _PickerDialog(self, "Add line", "Select a product :", options)
        self.wait_window(win)
        if win.result is None: return
        product = products[win.result]
        qty = ask_int("Add line", "Quantity", min_val=1)
        if qty is None: return
        try:
            order = self.app.inv.get_order(oid)
            order.add_line(product, qty)
            self.app.inv.db.commit()
            self.refresh()
            # Re-select the order to refresh lines
            for item in self.tree_orders.get_children():
                if self.tree_orders.item(item)["values"][0] == oid:
                    self.tree_orders.selection_set(item)
                    self._on_order_select(None)
                    break
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _confirm(self):
        oid = self._selected_order_id()
        if oid is None: return
        try:
            self.app.inv.confirm_order(oid)
            self.refresh()
            messagebox.showinfo("Success", f"Order {oid} confirmed.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _mark_done(self):
        oid = self._selected_order_id()
        if oid is None: return
        try:
            self.app.inv.mark_order_done(oid)
            self.refresh()
            messagebox.showinfo("Success", f"Order {oid} marked as done.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _cancel(self):
        oid = self._selected_order_id()
        if oid is None: return
        if not messagebox.askyesno("Confirm", f"Cancel order {oid}?"):
            return
        try:
            self.app.inv.cancel_order(oid)
            self.refresh()
            messagebox.showinfo("Success", f"Order {oid} cancelled.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ======================================================================
# Reports Frame
# ======================================================================

class ReportsFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app

        tk.Label(self, text="Reports", bg=BG_MAIN, fg=FG_TITLE,
                 font=FONT_TITLE, anchor="w", padx=20, pady=15).pack(fill="x")

        btn_frame = tk.Frame(self, bg=BG_MAIN)
        btn_frame.pack(fill="x", padx=20, pady=(0, 10))
        make_button(btn_frame, "Low stock",     self._show_low_stock,  BG_BTN_RED).pack(side="left", padx=5)
        make_button(btn_frame, "Stock moves",   self._show_moves,      BG_BTN).pack(side="left", padx=5)
        make_button(btn_frame, "Export CSV",    self._export_csv,      "#7F8C8D").pack(side="left", padx=5)

        # Summary cards
        self.card_frame = tk.Frame(self, bg=BG_MAIN)
        self.card_frame.pack(fill="x", padx=20, pady=(0, 15))
        self.lbl_products  = self._make_card(self.card_frame, "Products",    "0")
        self.lbl_customers = self._make_card(self.card_frame, "Customers",   "0")
        self.lbl_orders    = self._make_card(self.card_frame, "Orders",      "0")
        self.lbl_moves     = self._make_card(self.card_frame, "Stock moves", "0")

        # Table
        cols = ("Date", "Product ID", "Product", "Direction", "Qty", "Reason")
        tbl_frame, self.tree = make_table(self, cols)
        tbl_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _make_card(self, parent, label, value):
        card = tk.Frame(parent, bg=BG_CARD, relief="flat", bd=0)
        card.pack(side="left", padx=8, pady=5, ipadx=15, ipady=10)
        tk.Label(card, text=label, bg=BG_CARD, fg=FG_LABEL, font=FONT_BODY).pack()
        lbl = tk.Label(card, text=value, bg=BG_CARD, fg=FG_TITLE,
                       font=("Helvetica", 18, "bold"))
        lbl.pack()
        return lbl

    def refresh(self):
        inv = self.app.inv
        self.lbl_products.config(text=str(len(inv.list_products())))
        self.lbl_customers.config(text=str(len(inv.list_customers())))
        self.lbl_orders.config(text=str(len(inv.list_orders())))
        self.lbl_moves.config(text=str(len(inv.stock_moves)))
        self._show_moves()

    def _show_moves(self):
        self.tree.delete(*self.tree.get_children())
        for m in self.app.inv.stock_moves:
            self.tree.insert("", "end", values=(
                m.created_at[:10], m.product_id, m.product_name,
                m.direction.upper(), m.quantity, m.reason or "-"
            ))

    def _show_low_stock(self):
        self.tree.delete(*self.tree.get_children())
        for p in self.app.inv.list_low_stock():
            self.tree.insert("", "end", values=(
                "-", p.product_id, p.name,
                "LOW STOCK", p.quantity, f"min: {p.minimum_stock}"
            ))

    def _export_csv(self):
        filepath = ask_str("Export CSV", "Filename (default: export.csv)", required=False) or "export.csv"
        try:
            self.app.inv.export_csv(filepath)
            messagebox.showinfo("Export", f"File exported : {filepath}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ======================================================================
# Helper — Picker dialog (list selection)
# ======================================================================

class _PickerDialog(tk.Toplevel):

    def __init__(self, parent, title, prompt, options):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.grab_set()
        self.result = None

        tk.Label(self, text=prompt, font=FONT_SUB, pady=10, padx=15).pack()

        self.listbox = tk.Listbox(self, font=FONT_BODY, width=55, height=10,
                                  selectbackground=BG_BTN)
        for opt in options:
            self.listbox.insert("end", opt)
        self.listbox.pack(padx=15, pady=(0, 10))

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=(0, 10))
        tk.Button(btn_frame, text="Select", command=self._select,
                  bg=BG_BTN_GREEN, fg="white", font=FONT_BTN,
                  relief="flat", padx=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.destroy,
                  bg=BG_BTN_RED, fg="white", font=FONT_BTN,
                  relief="flat", padx=15).pack(side="left", padx=5)

    def _select(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Selection", "Please select an item.", parent=self)
            return
        self.result = sel[0]
        self.destroy()


# ======================================================================

if __name__ == "__main__":
    app = App()
    app.mainloop()
    app.inv.db.disconnect()
