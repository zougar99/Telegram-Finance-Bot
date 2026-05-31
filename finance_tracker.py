"""
Finance Tracker - Application Windows bach tjiri lflos
Revenus (salary, freelance) • Dépenses (asisiyn / ghyr asisiya) • Sold
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import csv
import os

SIDEBAR_BG = "#0f0f23"
SIDEBAR_HOVER = "#1a1a2e"
SIDEBAR_ACTIVE = "#16213e"
MAIN_BG = "#f8f9fa"
TEXT_DARK = "#2d3748"
TEXT_GRAY = "#718096"
ACCENT = "#2563eb"
SUCCESS = "#28a745"
WARNING = "#dc3545"

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finance_tracker.db")


class FinanceTrackerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Finance Tracker - Njiri lflos")
        self.root.geometry("1100x650")
        self.root.minsize(900, 550)
        self.root.configure(bg=MAIN_BG)

        self._init_db()
        self._editing_id = None
        self._editing_type = None
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                date TEXT,
                amount REAL,
                category TEXT,
                description TEXT,
                created_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    def _build_ui(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        sidebar = tk.Frame(self.root, bg=SIDEBAR_BG, width=200)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        tk.Label(sidebar, text="Finance", font=("Segoe UI", 18, "bold"), fg="white", bg=SIDEBAR_BG).pack(pady=(20, 5))
        tk.Label(sidebar, text="Tracker", font=("Segoe UI", 12), fg="#a0aec0", bg=SIDEBAR_BG).pack(pady=(0, 20))

        self._create_menu_btn(sidebar, "➕ Add", "add")
        self._create_menu_btn(sidebar, "📋 List", "list")
        self._create_menu_btn(sidebar, "📊 Sold", "stats")

        tk.Label(sidebar, text="Njiri lflos\nRevenus • Dépenses", font=("Segoe UI", 9), fg=TEXT_GRAY, bg=SIDEBAR_BG, justify="center").pack(side="bottom", pady=15)

        self.content = tk.Frame(self.root, bg=MAIN_BG, padx=25, pady=20)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)

        self.pages = {}
        self._build_add_page()
        self._build_list_page()
        self._build_stats_page()

        self._show_page("add")

    def _create_menu_btn(self, parent, text, page):
        btn = tk.Frame(parent, bg=SIDEBAR_BG, cursor="hand2")
        btn.pack(fill="x", padx=10, pady=2)
        lbl = tk.Label(btn, text=f"  {text}", font=("Segoe UI", 11), fg="white", bg=SIDEBAR_BG, anchor="w", cursor="hand2")
        lbl.pack(fill="x", pady=8, padx=5)

        def on_enter(e):
            btn.configure(bg=SIDEBAR_HOVER)
            lbl.configure(bg=SIDEBAR_HOVER)
        def on_leave(e):
            bg = SIDEBAR_ACTIVE if self.current_page == page else SIDEBAR_BG
            btn.configure(bg=bg)
            lbl.configure(bg=bg)
        def on_click(e):
            self._show_page(page)

        for w in [btn, lbl]:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)

    def _show_page(self, page):
        self.current_page = page
        for name, frame in self.pages.items():
            frame.grid_remove()
        self.pages[page].grid(row=1, column=0, sticky="nsew")
        if page == "list":
            self._refresh_list()
        elif page == "stats":
            self._refresh_stats()

    def _build_add_page(self):
        page = tk.Frame(self.content, bg=MAIN_BG)
        page.grid_columnconfigure(0, weight=1)

        tk.Label(page, text="Add Revenu / Dépense", font=("Segoe UI", 20, "bold"), fg=TEXT_DARK, bg=MAIN_BG).grid(row=0, column=0, sticky="w", pady=(0, 5))
        tk.Label(page, text="7ot revenu (salary, freelance) wla dépense (7ta, bouffe...)", font=("Segoe UI", 10), fg=TEXT_GRAY, bg=MAIN_BG).grid(row=1, column=0, sticky="w", pady=(0, 15))

        form = tk.Frame(page, bg=MAIN_BG)
        form.grid(row=2, column=0, sticky="ew", pady=10)
        form.grid_columnconfigure(1, weight=1)

        row = 0
        tk.Label(form, text="Type:", font=("Segoe UI", 10), bg=MAIN_BG).grid(row=row, column=0, sticky="w", padx=(0, 10), pady=5)
        self.entry_type = ttk.Combobox(form, values=["Revenu", "Dépense"], font=("Segoe UI", 11), width=20, state="readonly")
        self.entry_type.grid(row=row, column=1, sticky="w", padx=5, pady=5)
        self.entry_type.set("Revenu")
        self.entry_type.bind("<<ComboboxSelected>>", self._on_type_change)

        row += 1
        tk.Label(form, text="Date:", font=("Segoe UI", 10), bg=MAIN_BG).grid(row=row, column=0, sticky="w", padx=(0, 10), pady=5)
        self.entry_date = tk.Entry(form, font=("Segoe UI", 11), width=25)
        self.entry_date.grid(row=row, column=1, sticky="w", padx=5, pady=5)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        row += 1
        tk.Label(form, text="Montant (DH):", font=("Segoe UI", 10), bg=MAIN_BG).grid(row=row, column=0, sticky="w", padx=(0, 10), pady=5)
        self.entry_amount = tk.Entry(form, font=("Segoe UI", 11), width=25)
        self.entry_amount.grid(row=row, column=1, sticky="w", padx=5, pady=5)

        row += 1
        tk.Label(form, text="Catégorie:", font=("Segoe UI", 10), bg=MAIN_BG).grid(row=row, column=0, sticky="w", padx=(0, 10), pady=5)
        self.entry_category = ttk.Combobox(form, font=("Segoe UI", 11), width=25)
        self.entry_category.grid(row=row, column=1, sticky="w", padx=5, pady=5)
        self._update_categories()

        row += 1
        tk.Label(form, text="Description:", font=("Segoe UI", 10), bg=MAIN_BG).grid(row=row, column=0, sticky="nw", padx=(0, 10), pady=5)
        self.entry_desc = tk.Text(form, font=("Segoe UI", 11), height=3, width=40)
        self.entry_desc.grid(row=row, column=1, sticky="ew", padx=5, pady=5)

        row += 1
        btn_frame = tk.Frame(form, bg=MAIN_BG)
        btn_frame.grid(row=row, column=1, sticky="w", pady=15)
        tk.Button(btn_frame, text="Save", font=("Segoe UI", 11), bg=ACCENT, fg="white", relief="flat", padx=25, pady=8, cursor="hand2", command=self._save_entry).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Clear", font=("Segoe UI", 11), bg=TEXT_GRAY, fg="white", relief="flat", padx=25, pady=8, cursor="hand2", command=self._clear_form).pack(side="left")

        self.pages["add"] = page

    def _update_categories(self):
        if self.entry_type.get() == "Revenu":
            self.entry_category["values"] = ["Salary", "Freelance", "Autre"]
        else:
            self.entry_category["values"] = ["Loyer", "Bouffe", "Transport", "Santé", "Loisirs", "Autre"]
        if self.entry_category.get() not in self.entry_category["values"]:
            self.entry_category.set(self.entry_category["values"][0])

    def _on_type_change(self, e=None):
        self._update_categories()

    def _save_entry(self):
        ttype = self.entry_type.get()
        date = self.entry_date.get().strip()
        amount_str = self.entry_amount.get().strip()
        category = self.entry_category.get().strip()
        desc = self.entry_desc.get("1.0", "end").strip()

        if not amount_str:
            messagebox.showwarning("Warning", "7ot montant")
            return
        try:
            amount = float(amount_str.replace(",", "."))
        except ValueError:
            messagebox.showwarning("Warning", "Montant mzyan (ex: 1500)")
            return
        if ttype == "Dépense":
            amount = -abs(amount)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        if self._editing_id:
            c.execute("UPDATE transactions SET type=?, date=?, amount=?, category=?, description=? WHERE id=?",
                      (ttype, date or datetime.now().strftime("%Y-%m-%d"), amount, category, desc, self._editing_id))
            messagebox.showinfo("OK", "M7ayda!")
            self._editing_id = None
        else:
            c.execute("INSERT INTO transactions (type, date, amount, category, description, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                      (ttype, date or datetime.now().strftime("%Y-%m-%d"), amount, category, desc, datetime.now().isoformat()))
            messagebox.showinfo("OK", "M7fouz!")
        conn.commit()
        conn.close()

        self._clear_form()

    def _clear_form(self):
        self._editing_id = None
        self.entry_date.delete(0, "end")
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_amount.delete(0, "end")
        self.entry_category.set("")
        self._update_categories()
        self.entry_desc.delete("1.0", "end")

    def _build_list_page(self):
        page = tk.Frame(self.content, bg=MAIN_BG)
        page.grid_columnconfigure(0, weight=1)
        page.grid_rowconfigure(2, weight=1)

        tk.Label(page, text="List", font=("Segoe UI", 20, "bold"), fg=TEXT_DARK, bg=MAIN_BG).grid(row=0, column=0, sticky="w", pady=(0, 5))
        tk.Label(page, text="Kolchi - Revenus w Dépenses", font=("Segoe UI", 10), fg=TEXT_GRAY, bg=MAIN_BG).grid(row=1, column=0, sticky="w", pady=(0, 10))

        filter_frame = tk.Frame(page, bg=MAIN_BG)
        filter_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        filter_frame.grid_columnconfigure(3, weight=1)
        tk.Label(filter_frame, text="Filter:", font=("Segoe UI", 10), bg=MAIN_BG).grid(row=0, column=0, padx=(0, 5))
        self.filter_date = tk.Entry(filter_frame, font=("Segoe UI", 10), width=12)
        self.filter_date.grid(row=0, column=1, padx=5)
        tk.Label(filter_frame, text="Type:", font=("Segoe UI", 10), bg=MAIN_BG).grid(row=0, column=2, padx=(10, 5))
        self.filter_type = ttk.Combobox(filter_frame, values=["", "Revenu", "Dépense"], font=("Segoe UI", 10), width=12, state="readonly")
        self.filter_type.grid(row=0, column=3, padx=5)
        tk.Button(filter_frame, text="Filter", font=("Segoe UI", 10), bg=ACCENT, fg="white", relief="flat", padx=15, pady=5, cursor="hand2", command=self._refresh_list).grid(row=0, column=4, padx=10)
        tk.Button(filter_frame, text="Export CSV", font=("Segoe UI", 10), bg=SUCCESS, fg="white", relief="flat", padx=15, pady=5, cursor="hand2", command=self._export_csv).grid(row=0, column=5)
        tk.Button(filter_frame, text="Edit", font=("Segoe UI", 10), bg=ACCENT, fg="white", relief="flat", padx=15, pady=5, cursor="hand2", command=self._edit_entry).grid(row=0, column=6, padx=5)
        tk.Button(filter_frame, text="Delete", font=("Segoe UI", 10), bg=WARNING, fg="white", relief="flat", padx=15, pady=5, cursor="hand2", command=self._delete_entry).grid(row=0, column=7)

        tree_frame = tk.Frame(page, bg=MAIN_BG)
        tree_frame.grid(row=3, column=0, sticky="nsew", pady=5)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        columns = ("id", "date", "type", "amount", "category", "description")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15, displaycolumns=("date", "type", "amount", "category", "description"))
        self.tree.heading("date", text="Date")
        self.tree.heading("type", text="Type")
        self.tree.heading("amount", text="Montant (DH)")
        self.tree.heading("category", text="Catégorie")
        self.tree.heading("description", text="Description")
        self.tree.column("date", width=90)
        self.tree.column("type", width=80)
        self.tree.column("amount", width=100)
        self.tree.column("category", width=100)
        self.tree.column("description", width=250)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        page.grid_rowconfigure(3, weight=1)
        self.pages["list"] = page

    def _refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        date_filter = self.filter_date.get().strip()
        type_filter = self.filter_type.get().strip()

        if date_filter and type_filter:
            c.execute("SELECT id, date, type, amount, category, description FROM transactions WHERE date LIKE ? AND type=? ORDER BY date DESC",
                      (f"%{date_filter}%", type_filter))
        elif date_filter:
            c.execute("SELECT id, date, type, amount, category, description FROM transactions WHERE date LIKE ? ORDER BY date DESC",
                      (f"%{date_filter}%",))
        elif type_filter:
            c.execute("SELECT id, date, type, amount, category, description FROM transactions WHERE type=? ORDER BY date DESC",
                      (type_filter,))
        else:
            c.execute("SELECT id, date, type, amount, category, description FROM transactions ORDER BY date DESC")

        for row in c.fetchall():
            amt = row[3]
            amt_str = f"+{amt:.2f}" if amt >= 0 else f"{amt:.2f}"
            self.tree.insert("", "end", iid=str(row[0]), values=(row[0], row[1], row[2], amt_str, row[4], row[5] or ""))
        conn.close()

    def _edit_entry(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select entry bach t-edit")
            return
        entry_id = int(sel[0])
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT type, date, amount, category, description FROM transactions WHERE id=?", (entry_id,))
        row = c.fetchone()
        conn.close()
        if not row:
            return
        self.entry_type.set(row[0])
        self._update_categories()
        self.entry_date.delete(0, "end")
        self.entry_date.insert(0, row[1])
        self.entry_amount.delete(0, "end")
        self.entry_amount.insert(0, str(abs(row[2])))
        self.entry_category.set(row[3])
        self.entry_desc.delete("1.0", "end")
        self.entry_desc.insert("1.0", row[4] or "")
        self._editing_id = entry_id
        self._show_page("add")

    def _delete_entry(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select entry bach t-delete")
            return
        if not messagebox.askyesno("Confirm", "Wach bghiti t-delete?"):
            return
        entry_id = int(sel[0])
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM transactions WHERE id=?", (entry_id,))
        conn.commit()
        conn.close()
        self._refresh_list()

    def _export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT date, type, amount, category, description FROM transactions ORDER BY date DESC")
        rows = c.fetchall()
        conn.close()
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Date", "Type", "Montant (DH)", "Catégorie", "Description"])
            w.writerows(rows)
        messagebox.showinfo("OK", f"Export m7fouz: {path}")

    def _build_stats_page(self):
        page = tk.Frame(self.content, bg=MAIN_BG)
        page.grid_columnconfigure(0, weight=1)

        tk.Label(page, text="Sold", font=("Segoe UI", 20, "bold"), fg=TEXT_DARK, bg=MAIN_BG).grid(row=0, column=0, sticky="w", pady=(0, 5))
        tk.Label(page, text="Total Revenus - Total Dépenses = Sold", font=("Segoe UI", 10), fg=TEXT_GRAY, bg=MAIN_BG).grid(row=1, column=0, sticky="w", pady=(0, 15))

        self.stats_frame = tk.Frame(page, bg=MAIN_BG)
        self.stats_frame.grid(row=2, column=0, sticky="nsew")
        self.stats_frame.grid_columnconfigure(0, weight=1)

        self.pages["stats"] = page

    def _refresh_stats(self):
        for w in self.stats_frame.winfo_children():
            w.destroy()

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT SUM(amount) FROM transactions WHERE amount > 0")
        total_revenus = c.fetchone()[0] or 0
        c.execute("SELECT SUM(amount) FROM transactions WHERE amount < 0")
        total_depenses = abs(c.fetchone()[0] or 0)
        conn.close()

        sold = total_revenus - total_depenses

        tk.Label(self.stats_frame, text=f"Total Revenus: {total_revenus:,.2f} DH", font=("Segoe UI", 14, "bold"), fg=SUCCESS, bg=MAIN_BG).grid(row=0, column=0, sticky="w", pady=10)
        tk.Label(self.stats_frame, text=f"Total Dépenses: {total_depenses:,.2f} DH", font=("Segoe UI", 14, "bold"), fg=WARNING, bg=MAIN_BG).grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(self.stats_frame, text=f"Sold: {sold:,.2f} DH", font=("Segoe UI", 18, "bold"), fg=ACCENT, bg=MAIN_BG).grid(row=2, column=0, sticky="w", pady=15)

    def run(self):
        self.root.mainloop()


def main():
    try:
        app = FinanceTrackerApp()
        app.run()
    except Exception as e:
        import traceback
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "finance_error.txt"), "w", encoding="utf-8") as f:
            f.write(str(e) + "\n\n" + traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
