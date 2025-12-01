import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# ------------------------------------------------------
# Helper functions to load/save JSON data
# ------------------------------------------------------

def load_json(path):
    """Safely load JSON from a file. If file missing or invalid, return empty list."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return []


def save_json(path, data):
    """Safely save list data to JSON."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error writing {path}: {e}")
        messagebox.showerror("Error", f"Failed to save data:\n{e}")


# ------------------------------------------------------
# Main Admin Dashboard App
# ------------------------------------------------------

class AdminDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window basic setup
        self.title("Navya Jewels - Admin Dashboard")
        self.geometry("1000x640")
        self.minsize(950, 580)
        self.configure(bg="#050509")

        # Find data folder (same folder as this script)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(base_dir, "data")

        self.users_file = os.path.join(self.data_dir, "users.json")
        self.orders_file = os.path.join(self.data_dir, "orders.json")
        self.contacts_file = os.path.join(self.data_dir, "contacts.json")

        # Data containers
        self.users = []
        self.orders = []
        self.contacts = []

        # Selected items cache
        self.selected_order_id = None
        self.selected_contact_id = None

        # For title animation
        self._title_colors = ["#f5f5f5", "#f8d489"]
        self._title_color_index = 0

        # Build UI
        self.build_ui()

        # Start small animations
        self.animate_title()
        self.update_datetime()

        # Load data at start
        self.refresh_data()

    # ---------------- Small UI helpers ---------------- #

    def add_hover_effect(self, button, normal_bg, hover_bg):
        """Simple hover animation for buttons."""
        button.configure(bg=normal_bg, activebackground=hover_bg)

        def on_enter(_):
            button.configure(bg=hover_bg)

        def on_leave(_):
            button.configure(bg=normal_bg)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def animate_title(self):
        """Pulse the title label text color for a soft animated feel."""
        if hasattr(self, "title_lbl"):
            color = self._title_colors[self._title_color_index]
            self.title_lbl.configure(fg=color)
            self._title_color_index = 1 - self._title_color_index
        # Call again after 700ms
        self.after(700, self.animate_title)

    def update_datetime(self):
        """Update the small date/time label in the top bar every second."""
        if hasattr(self, "datetime_lbl"):
            now = datetime.now()
            # Example format: 01 Dec 2025  |  11:23:45 AM
            text = now.strftime("%d %b %Y  |  %I:%M:%S %p")
            self.datetime_lbl.config(text=text)
        self.after(1000, self.update_datetime)

    # ---------------- UI Layout ---------------- #

    def build_ui(self):
        # Top gradient-like bar (using two shades)
        top_bar = tk.Frame(self, bg="#080814")
        top_bar.pack(fill="x", padx=10, pady=10)

        self.title_lbl = tk.Label(
            top_bar,
            text="Navya Jewels - Admin Dashboard",
            font=("Segoe UI Semibold", 13),
            fg="#f5f5f5",
            bg="#080814",
        )
        self.title_lbl.pack(side="left", padx=(10, 20), pady=8)

        # Summary badges
        badge_bg = "#151524"

        self.users_count_label = tk.Label(
            top_bar,
            text="Users: 0",
            font=("Segoe UI", 10, "bold"),
            fg="#f8d489",
            bg=badge_bg,
            padx=10,
            pady=4,
        )
        self.users_count_label.pack(side="left", padx=5)

        self.orders_count_label = tk.Label(
            top_bar,
            text="Orders: 0",
            font=("Segoe UI", 10, "bold"),
            fg="#a0e9a5",
            bg=badge_bg,
            padx=10,
            pady=4,
        )
        self.orders_count_label.pack(side="left", padx=5)

        self.contacts_count_label = tk.Label(
            top_bar,
            text="Enquiries: 0",
            font=("Segoe UI", 10, "bold"),
            fg="#9bc7ff",
            bg=badge_bg,
            padx=10,
            pady=4,
        )
        self.contacts_count_label.pack(side="left", padx=5)

        # Date / Time label (right side)
        self.datetime_lbl = tk.Label(
            top_bar,
            text="-- --- ----  |  --:--:-- --",
            font=("Segoe UI", 9),
            fg="#c0c0d8",
            bg="#080814",
        )
        self.datetime_lbl.pack(side="right", padx=(10, 5), pady=8)

        refresh_btn = tk.Button(
            top_bar,
            text="⟳ Refresh",
            command=self.refresh_data,
            fg="#000000",
            relief="flat",
            padx=12,
            pady=4,
        )
        refresh_btn.pack(side="right", padx=10)
        self.add_hover_effect(refresh_btn, "#f8d489", "#f9e3aa")

        # Notebook (tabs)
        notebook_frame = tk.Frame(self, bg="#050509")
        notebook_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        style = ttk.Style()
        style.theme_use("default")

        # Notebook styling
        style.configure(
            "TNotebook",
            background="#050509",
            borderwidth=0,
        )
        style.configure(
            "TNotebook.Tab",
            background="#131323",
            foreground="#f5f5f5",
            padding=(12, 6),
            font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#1f1f3a")],
            foreground=[("selected", "#f8d489")],
        )

        # Treeview styling
        style.configure(
            "Treeview",
            background="#0f0f16",
            foreground="#f5f5f5",
            fieldbackground="#0f0f16",
            rowheight=24,
            bordercolor="#222230",
            borderwidth=0,
        )
        style.map("Treeview", background=[("selected", "#2e2e4a")])
        style.configure(
            "Treeview.Heading",
            background="#151524",
            foreground="#f5f5f5",
            font=("Segoe UI", 9, "bold"),
            bordercolor="#151524",
            borderwidth=1,
        )

        notebook = ttk.Notebook(notebook_frame)
        notebook.pack(fill="both", expand=True)

        # ---- Users tab ----
        self.users_frame = tk.Frame(notebook, bg="#050509")
        notebook.add(self.users_frame, text="Users")

        self.build_users_tab(self.users_frame)

        # ---- Orders tab ----
        self.orders_frame = tk.Frame(notebook, bg="#050509")
        notebook.add(self.orders_frame, text="Orders")

        self.build_orders_tab(self.orders_frame)

        # ---- Enquiries tab ----
        self.contacts_frame = tk.Frame(notebook, bg="#050509")
        notebook.add(self.contacts_frame, text="Enquiries")

        self.build_contacts_tab(self.contacts_frame)

    # ------------ Tab builders ------------ #

    def build_users_tab(self, parent):
        # Main layout: table + details
        top = tk.Frame(parent, bg="#050509")
        top.pack(fill="both", expand=True, padx=6, pady=(6, 4))

        bottom = tk.Frame(parent, bg="#050509")
        # Fill BOTH to make bottom "square" bigger & visible
        bottom.pack(fill="x", padx=6, pady=(0, 8))

        # Tree + scrollbar
        tree_frame = tk.Frame(top, bg="#050509")
        tree_frame.pack(fill="both", expand=True)

        self.users_tree = ttk.Treeview(
            tree_frame,
            columns=("id", "name", "email", "phone"),
            show="headings",
            selectmode="browse",
        )
        self.users_tree.heading("id", text="ID")
        self.users_tree.heading("name", text="Name")
        self.users_tree.heading("email", text="Email")
        self.users_tree.heading("phone", text="Phone")

        self.users_tree.column("id", width=120, anchor="w")
        self.users_tree.column("name", width=180, anchor="w")
        self.users_tree.column("email", width=250, anchor="w")
        self.users_tree.column("phone", width=140, anchor="w")

        # Zebra row colors
        self.users_tree.tag_configure("evenrow", background="#0f0f16")
        self.users_tree.tag_configure("oddrow", background="#151524")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=vsb.set)

        self.users_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Bigger detail box (Text) at bottom
        self.user_detail_text = tk.Text(
            bottom,
            height=5,
            bg="#0f0f16",
            fg="#f5f5f5",
            insertbackground="#f5f5f5",
            relief="flat",
            padx=8,
            pady=6,
            font=("Consolas", 9),
        )
        self.user_detail_text.pack(fill="x", pady=(4, 0))
        self.user_detail_text.config(state="disabled")
        self.clear_user_detail()

        # Bind selection
        self.users_tree.bind("<<TreeviewSelect>>", self.show_user_detail)

    def build_orders_tab(self, parent):
        top = tk.Frame(parent, bg="#050509")
        top.pack(fill="both", expand=True, padx=6, pady=(6, 4))

        bottom = tk.Frame(parent, bg="#050509")
        bottom.pack(fill="x", padx=6, pady=(0, 8))

        # Tree + scrollbar
        tree_frame = tk.Frame(top, bg="#050509")
        tree_frame.pack(fill="both", expand=True)

        self.orders_tree = ttk.Treeview(
            tree_frame,
            columns=("id", "userId", "customerName", "total", "status", "createdAt"),
            show="headings",
            selectmode="browse",
        )
        self.orders_tree.heading("id", text="Order ID")
        self.orders_tree.heading("userId", text="User ID")
        self.orders_tree.heading("customerName", text="Customer")
        self.orders_tree.heading("total", text="Total (₹)")
        self.orders_tree.heading("status", text="Status")
        self.orders_tree.heading("createdAt", text="Date")

        self.orders_tree.column("id", width=120, anchor="w")
        self.orders_tree.column("userId", width=80, anchor="w")
        self.orders_tree.column("customerName", width=160, anchor="w")
        self.orders_tree.column("total", width=90, anchor="e")
        self.orders_tree.column("status", width=90, anchor="center")
        self.orders_tree.column("createdAt", width=170, anchor="w")

        # Zebra rows
        self.orders_tree.tag_configure("evenrow", background="#0f0f16")
        self.orders_tree.tag_configure("oddrow", background="#151524")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=vsb.set)

        self.orders_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Detail box + actions
        detail_frame = tk.Frame(bottom, bg="#050509")
        detail_frame.pack(fill="x")

        self.order_detail_text = tk.Text(
            detail_frame,
            height=6,
            bg="#0f0f16",
            fg="#f5f5f5",
            insertbackground="#f5f5f5",
            relief="flat",
            padx=8,
            pady=6,
            font=("Consolas", 9),
        )
        self.order_detail_text.pack(side="left", fill="both", expand=True, pady=(4, 0))
        self.order_detail_text.config(state="disabled")

        btn_frame = tk.Frame(detail_frame, bg="#050509")
        btn_frame.pack(side="right", fill="y", padx=(8, 0))

        confirm_btn = tk.Button(
            btn_frame,
            text="✓ Confirm",
            command=self.confirm_order,
            fg="#ffffff",
            relief="flat",
            padx=10,
            pady=4,
        )
        confirm_btn.pack(fill="x", pady=2)
        self.add_hover_effect(confirm_btn, "#2f9e44", "#38b249")

        deliver_btn = tk.Button(
            btn_frame,
            text="✓ Delivered",
            command=self.mark_order_delivered,
            fg="#ffffff",
            relief="flat",
            padx=10,
            pady=4,
        )
        deliver_btn.pack(fill="x", pady=2)
        self.add_hover_effect(deliver_btn, "#228be6", "#339af0")

        delete_btn = tk.Button(
            btn_frame,
            text="🗑 Remove",
            command=self.delete_order,
            fg="#ffffff",
            relief="flat",
            padx=10,
            pady=4,
        )
        delete_btn.pack(fill="x", pady=2)
        self.add_hover_effect(delete_btn, "#e03131", "#fa5252")

        self.orders_tree.bind("<<TreeviewSelect>>", self.on_order_select)

    def build_contacts_tab(self, parent):
        top = tk.Frame(parent, bg="#050509")
        top.pack(fill="both", expand=True, padx=6, pady=(6, 4))

        bottom = tk.Frame(parent, bg="#050509")
        bottom.pack(fill="x", padx=6, pady=(0, 8))

        # Tree + scrollbar
        tree_frame = tk.Frame(top, bg="#050509")
        tree_frame.pack(fill="both", expand=True)

        self.contacts_tree = ttk.Treeview(
            tree_frame,
            columns=("id", "name", "email", "phone", "status", "createdAt"),
            show="headings",
            selectmode="browse",
        )
        self.contacts_tree.heading("id", text="ID")
        self.contacts_tree.heading("name", text="Name")
        self.contacts_tree.heading("email", text="Email")
        self.contacts_tree.heading("phone", text="Phone")
        self.contacts_tree.heading("status", text="Status")
        self.contacts_tree.heading("createdAt", text="Date")

        self.contacts_tree.column("id", width=90, anchor="w")
        self.contacts_tree.column("name", width=140, anchor="w")
        self.contacts_tree.column("email", width=190, anchor="w")
        self.contacts_tree.column("phone", width=120, anchor="w")
        self.contacts_tree.column("status", width=80, anchor="center")
        self.contacts_tree.column("createdAt", width=150, anchor="w")

        # Zebra rows
        self.contacts_tree.tag_configure("evenrow", background="#0f0f16")
        self.contacts_tree.tag_configure("oddrow", background="#151524")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.contacts_tree.yview)
        self.contacts_tree.configure(yscrollcommand=vsb.set)

        self.contacts_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Detail box + actions
        detail_frame = tk.Frame(bottom, bg="#050509")
        detail_frame.pack(fill="x")

        self.contact_detail_text = tk.Text(
            detail_frame,
            height=6,
            bg="#0f0f16",
            fg="#f5f5f5",
            insertbackground="#f5f5f5",
            relief="flat",
            padx=8,
            pady=6,
            font=("Consolas", 9),
        )
        self.contact_detail_text.pack(side="left", fill="both", expand=True, pady=(4, 0))
        self.contact_detail_text.config(state="disabled")

        btn_frame = tk.Frame(detail_frame, bg="#050509")
        btn_frame.pack(side="right", fill="y", padx=(8, 0))

        done_btn = tk.Button(
            btn_frame,
            text="✓ Mark Done",
            command=self.mark_contact_done,
            fg="#ffffff",
            relief="flat",
            padx=10,
            pady=4,
        )
        done_btn.pack(fill="x", pady=2)
        self.add_hover_effect(done_btn, "#2f9e44", "#38b249")

        delete_btn = tk.Button(
            btn_frame,
            text="🗑 Remove",
            command=self.delete_contact,
            fg="#ffffff",
            relief="flat",
            padx=10,
            pady=4,
        )
        delete_btn.pack(fill="x", pady=2)
        self.add_hover_effect(delete_btn, "#e03131", "#fa5252")

        self.contacts_tree.bind("<<TreeviewSelect>>", self.on_contact_select)

    # ---------------- Data handling ---------------- #

    def refresh_data(self):
        """Reload JSON data and refresh UI tables + counters."""
        try:
            self.users = load_json(self.users_file)
            self.orders = load_json(self.orders_file)
            self.contacts = load_json(self.contacts_file)

            # Update top counts
            self.users_count_label.config(text=f"Users: {len(self.users)}")
            self.orders_count_label.config(text=f"Orders: {len(self.orders)}")
            self.contacts_count_label.config(text=f"Enquiries: {len(self.contacts)}")

            # Fill tables
            self.populate_users_table()
            self.populate_orders_table()
            self.populate_contacts_table()

            # Clear detail panes
            self.clear_user_detail()
            self.clear_order_detail()
            self.clear_contact_detail()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data:\n{e}")

    def populate_users_table(self):
        for row in self.users_tree.get_children():
            self.users_tree.delete(row)

        for index, u in enumerate(self.users):
            tag = "oddrow" if index % 2 else "evenrow"
            self.users_tree.insert(
                "",
                "end",
                values=(
                    u.get("id", ""),
                    u.get("name", ""),
                    u.get("email", ""),
                    u.get("phone", ""),
                ),
                tags=(tag,),
            )

    def populate_orders_table(self):
        for row in self.orders_tree.get_children():
            self.orders_tree.delete(row)

        for index, o in enumerate(self.orders):
            tag = "oddrow" if index % 2 else "evenrow"
            self.orders_tree.insert(
                "",
                "end",
                values=(
                    o.get("id", ""),
                    o.get("userId", ""),
                    o.get("customerName", ""),
                    o.get("total", 0),
                    o.get("status", "Pending"),
                    o.get("createdAt", ""),
                ),
                tags=(tag,),
            )

    def populate_contacts_table(self):
        for row in self.contacts_tree.get_children():
            self.contacts_tree.delete(row)

        for index, c in enumerate(self.contacts):
            status = c.get("status") or "Pending"
            tag = "oddrow" if index % 2 else "evenrow"
            self.contacts_tree.insert(
                "",
                "end",
                values=(
                    c.get("id", ""),
                    c.get("name", ""),
                    c.get("email", ""),
                    c.get("phone", ""),
                    status,
                    c.get("createdAt", ""),
                ),
                tags=(tag,),
            )

    # ---------------- Detail handlers ---------------- #

    def show_user_detail(self, event=None):
        selected = self.users_tree.focus()
        if not selected:
            self.clear_user_detail()
            return
        values = self.users_tree.item(selected, "values")
        if not values:
            self.clear_user_detail()
            return

        uid, name, email, phone = values
        lines = []
        lines.append(f"ID:      {uid}")
        lines.append(f"Name:    {name}")
        lines.append(f"Email:   {email}")
        lines.append(f"Phone:   {phone}")

        self.user_detail_text.config(state="normal")
        self.user_detail_text.delete("1.0", "end")
        self.user_detail_text.insert("1.0", "\n".join(lines))
        self.user_detail_text.config(state="disabled")

    def clear_user_detail(self):
        self.user_detail_text.config(state="normal")
        self.user_detail_text.delete("1.0", "end")
        self.user_detail_text.insert("1.0", "Select a user to see full details here.")
        self.user_detail_text.config(state="disabled")

    def on_order_select(self, event=None):
        selected = self.orders_tree.focus()
        if not selected:
            self.selected_order_id = None
            self.clear_order_detail()
            return

        values = self.orders_tree.item(selected, "values")
        if not values:
            self.selected_order_id = None
            self.clear_order_detail()
            return

        order_id = values[0]
        self.selected_order_id = order_id

        order = next((o for o in self.orders if o.get("id") == order_id), None)
        if not order:
            self.clear_order_detail()
            return

        # Build detail text
        lines = []
        lines.append(f"Order ID:  {order.get('id', '')}")
        lines.append(f"User ID:   {order.get('userId', '')}")
        lines.append(f"Customer:  {order.get('customerName', '')}")
        lines.append(f"Phone:     {order.get('phone', '')}")
        lines.append(
            "Address:   "
            f"{order.get('address', '')}, "
            f"{order.get('city', '')} - {order.get('pincode', '')}"
        )
        lines.append(f"Payment:   {order.get('paymentMethod', '')}")
        lines.append(f"Status:    {order.get('status', 'Pending')}")
        lines.append(f"Date:      {order.get('createdAt', '')}")
        lines.append("")
        lines.append("Items:")
        items = order.get("items", [])
        for item in items:
            name = item.get("name", "")
            qty = item.get("quantity", 0)
            price = item.get("price", 0)
            lines.append(f"  • {name}  x{qty}  (₹{price} each, ₹{price * qty} total)")
        lines.append("")
        lines.append(f"Order Total: ₹{order.get('total', 0)}")

        self.order_detail_text.config(state="normal")
        self.order_detail_text.delete("1.0", "end")
        self.order_detail_text.insert("1.0", "\n".join(lines))
        self.order_detail_text.config(state="disabled")

    def clear_order_detail(self):
        self.order_detail_text.config(state="normal")
        self.order_detail_text.delete("1.0", "end")
        self.order_detail_text.insert("1.0", "Select an order to see full details here.")
        self.order_detail_text.config(state="disabled")

    def on_contact_select(self, event=None):
        selected = self.contacts_tree.focus()
        if not selected:
            self.selected_contact_id = None
            self.clear_contact_detail()
            return

        values = self.contacts_tree.item(selected, "values")
        if not values:
            self.selected_contact_id = None
            self.clear_contact_detail()
            return

        contact_id = values[0]
        self.selected_contact_id = contact_id

        contact = next((c for c in self.contacts if c.get("id") == contact_id), None)
        if not contact:
            self.clear_contact_detail()
            return

        lines = []
        lines.append(f"ID:     {contact.get('id', '')}")
        lines.append(f"Name:   {contact.get('name', '')}")
        lines.append(f"Email:  {contact.get('email', '')}")
        lines.append(f"Phone:  {contact.get('phone', '')}")
        lines.append(f"Status: {contact.get('status', 'Pending')}")
        lines.append(f"Date:   {contact.get('createdAt', '')}")
        lines.append("")
        lines.append("Message:")
        lines.append(contact.get("message", ""))

        self.contact_detail_text.config(state="normal")
        self.contact_detail_text.delete("1.0", "end")
        self.contact_detail_text.insert("1.0", "\n".join(lines))
        self.contact_detail_text.config(state="disabled")

    def clear_contact_detail(self):
        self.contact_detail_text.config(state="normal")
        self.contact_detail_text.delete("1.0", "end")
        self.contact_detail_text.insert("1.0", "Select an enquiry to see full details here.")
        self.contact_detail_text.config(state="disabled")

    # ---------------- Actions: Orders ---------------- #

    def _get_selected_order(self):
        if not self.selected_order_id:
            messagebox.showinfo("Orders", "Please select an order first.")
            return None, None

        index = None
        for i, o in enumerate(self.orders):
            if o.get("id") == self.selected_order_id:
                index = i
                break

        if index is None:
            messagebox.showerror("Orders", "Selected order not found in data.")
            return None, None

        return index, self.orders[index]

    def confirm_order(self):
        idx, order = self._get_selected_order()
        if order is None:
            return
        order["status"] = "Confirmed"
        self.orders[idx] = order
        save_json(self.orders_file, self.orders)
        self.refresh_data()

    def mark_order_delivered(self):
        idx, order = self._get_selected_order()
        if order is None:
            return
        order["status"] = "Delivered"
        self.orders[idx] = order
        save_json(self.orders_file, self.orders)
        self.refresh_data()

    def delete_order(self):
        idx, order = self._get_selected_order()
        if order is None:
            return
        if not messagebox.askyesno("Remove Order", f"Remove order {order.get('id')}?"):
            return
        self.orders.pop(idx)
        save_json(self.orders_file, self.orders)
        self.refresh_data()

    # ---------------- Actions: Contacts ---------------- #

    def _get_selected_contact(self):
        if not self.selected_contact_id:
            messagebox.showinfo("Enquiries", "Please select an enquiry first.")
            return None, None

        index = None
        for i, c in enumerate(self.contacts):
            if c.get("id") == self.selected_contact_id:
                index = i
                break

        if index is None:
            messagebox.showerror("Enquiries", "Selected enquiry not found in data.")
            return None, None

        return index, self.contacts[index]

    def mark_contact_done(self):
        idx, contact = self._get_selected_contact()
        if contact is None:
            return
        contact["status"] = "Done"
        self.contacts[idx] = contact
        save_json(self.contacts_file, self.contacts)
        self.refresh_data()

    def delete_contact(self):
        idx, contact = self._get_selected_contact()
        if contact is None:
            return
        if not messagebox.askyesno("Remove Enquiry", f"Remove enquiry {contact.get('id')}?"):
            return
        self.contacts.pop(idx)
        save_json(self.contacts_file, self.contacts)
        self.refresh_data()


# ------------------------------------------------------
# Entry point
# ------------------------------------------------------

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
