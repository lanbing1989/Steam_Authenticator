import os
import json
import time
import steam_totp
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

DEFAULT_MAFILES_DIR = "maFiles"

def load_mafiles(mafiles_dir):
    mafiles = []
    if not os.path.isdir(mafiles_dir):
        return mafiles
    for filename in os.listdir(mafiles_dir):
        if filename.endswith(".maFile"):
            path = os.path.join(mafiles_dir, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    account_name = data.get("account_name", filename)
                    shared_secret = data["shared_secret"]
                    mafiles.append({
                        "account": account_name,
                        "shared_secret": shared_secret,
                        "filename": filename
                    })
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return mafiles

class CodeWindow(tk.Toplevel):
    def __init__(self, master, mafile_info):
        super().__init__(master)
        self.title(f"验证码 - {mafile_info['account']}")
        self.geometry("350x240")
        self.configure(bg="#ffffff")
        self.resizable(False, False)
        self.shared_secret = mafile_info["shared_secret"]
        self.current_code = ""
        self.copied_label = None

        # 屏幕右侧居中显示
        self.set_right_side(350, 240)

        frame = ttk.Frame(self, padding=20, style="White.TFrame")
        frame.pack(fill=tk.BOTH, expand=True)

        account_str = f"账号: {mafile_info['account']}"
        self.label_account = ttk.Label(frame, text=account_str, font=("微软雅黑", 13), background="#ffffff")
        self.label_account.pack(pady=(0, 14))

        self.label_code = ttk.Label(frame, text="------", font=("Consolas", 36, "bold"), foreground="#1976d2", background="#ffffff")
        self.label_code.pack(pady=(0, 10))

        self.label_timer = ttk.Label(frame, text="倒计时: -- 秒", font=("微软雅黑", 13), background="#ffffff")
        self.label_timer.pack(pady=(0, 12))

        self.copy_btn = ttk.Button(frame, text="一键复制验证码", command=self.copy_code, style="Accent.TButton")
        self.copy_btn.pack(ipadx=10, ipady=2)

        self.update_code()

    def set_right_side(self, width=350, height=240):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = sw - width - 40
        y = int((sh - height) / 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def copy_code(self):
        code = self.current_code
        if code:
            self.clipboard_clear()
            self.clipboard_append(code)
            if self.copied_label:
                self.copied_label.destroy()
            self.copied_label = ttk.Label(self, text="已复制!", font=("微软雅黑", 11), foreground="green", background="#ffffff")
            self.copied_label.place(relx=0.5, rely=0.90, anchor="center")
            self.after(1200, lambda: self.copied_label.destroy())

    def update_code(self):
        try:
            now = int(time.time())
            code = steam_totp.generate_twofactor_code_for_time(self.shared_secret, now)
            seconds_left = 30 - (now % 30)
        except Exception:
            code = "ERROR"
            seconds_left = "--"
        self.current_code = code
        self.label_code.config(text=code)
        self.label_timer.config(text=f"倒计时: {seconds_left} 秒")
        self.after(1000, self.update_code)

class SteamCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steam maFile 多账号管理器 - 灯火通明")
        bg_color = "#ffffff"
        self.root.configure(bg=bg_color)
        self.set_right_side(420, 660)  # 略微增高

        self.mafiles_dir = DEFAULT_MAFILES_DIR  # 默认文件夹

        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure("Treeview", font=("微软雅黑", 12), rowheight=32, background=bg_color, fieldbackground=bg_color, foreground="#222")
        style.configure("Treeview.Heading", font=("微软雅黑", 13, "bold"), background=bg_color, foreground="#222")
        style.configure("Accent.TButton", foreground="white", background="#1976d2")
        style.configure("White.TFrame", background=bg_color)
        style.configure("White.TLabel", background=bg_color)

        frm_top = ttk.Frame(root, padding=(10, 10, 10, 0), style="White.TFrame")
        frm_top.pack(fill=tk.X)

        ttk.Label(frm_top, text="🔍", font=("微软雅黑", 14), background=bg_color).pack(side=tk.LEFT, padx=(0, 2))
        self.entry_search = ttk.Entry(frm_top, font=("微软雅黑", 12), width=24)
        self.entry_search.pack(side=tk.LEFT, padx=4)
        self.entry_search.bind("<KeyRelease>", self.search_accounts)

        btn_refresh = ttk.Button(frm_top, text="刷新账号列表", command=self.refresh_mafiles)
        btn_refresh.pack(side=tk.LEFT, padx=12)

        btn_choose = ttk.Button(frm_top, text="选择文件夹", command=self.choose_folder)
        btn_choose.pack(side=tk.LEFT, padx=12)

        # 单列Treeview，只显示账号
        frm_table = ttk.Frame(root, padding=(10, 4, 10, 4), style="White.TFrame")
        frm_table.pack(fill=tk.BOTH, expand=True)
        self.tree = ttk.Treeview(frm_table, columns=("account",), show="headings", height=12, style="Treeview")
        self.tree.heading("account", text="账号")
        self.tree.column("account", width=360, anchor="center")
        vsb = ttk.Scrollbar(frm_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        frm_table.rowconfigure(0, weight=1)
        frm_table.columnconfigure(0, weight=1)

        self.tree.bind("<Double-1>", self.show_code_window)

        self.mafiles = []
        self.filtered_mafiles = []
        self.tree_items = {}
        self.refresh_mafiles(first_time=True)

        self.show_footer(bg_color)

    def set_right_side(self, width=420, height=660):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = sw - width - 40
        y = int((sh - height) / 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def choose_folder(self):
        path = filedialog.askdirectory(title="请选择maFiles文件夹")
        if path:
            self.mafiles_dir = path
            self.refresh_mafiles()

    def refresh_mafiles(self, first_time=False):
        self.mafiles = load_mafiles(self.mafiles_dir)
        self.filtered_mafiles = self.mafiles.copy()
        self.reload_treeview()
        if not first_time:
            messagebox.showinfo("提示", f"账号列表已刷新\n当前文件夹: {self.mafiles_dir}")

    def reload_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree_items.clear()
        for ma in self.filtered_mafiles:
            item = self.tree.insert("", tk.END, values=(ma["account"],))
            self.tree_items[ma["account"]] = item

    def search_accounts(self, event=None):
        query = self.entry_search.get().strip().lower()
        if not query:
            self.filtered_mafiles = self.mafiles.copy()
        else:
            self.filtered_mafiles = [
                ma for ma in self.mafiles if query in ma["account"].lower() or query in ma["filename"].lower()
            ]
        self.reload_treeview()

    def show_code_window(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        values = self.tree.item(item, "values")
        account = values[0]
        for ma in self.filtered_mafiles:
            if ma["account"] == account:
                CodeWindow(self.root, ma)
                break

    def show_footer(self, bg_color):
        # 简易使用说明和版权
        frm_footer = ttk.Frame(self.root, padding=(12, 0, 12, 8), style="White.TFrame")
        frm_footer.pack(fill=tk.X, side=tk.BOTTOM)
        label1 = ttk.Label(frm_footer, text="【使用说明】", font=("微软雅黑", 10, "bold"), foreground="#222", style="White.TLabel")
        label1.pack(anchor="w", pady=(2, 0))
        desc = (
            "1. 将所有 Steam maFile 文件放入本程序同目录的 maFiles 文件夹内（或点击“选择文件夹”自定义目录）。\n"
            "2. 搜索或直接浏览账号列表，双击账号弹出验证码窗口。\n"
            "3. 验证码窗口可自动刷新，显示倒计时，并支持一键复制。\n"
            "4. 若新增/更换 maFile 文件，点击“刷新账号列表”按钮即可。"
        )
        label2 = ttk.Label(
            frm_footer,
            text=desc,
            font=("微软雅黑", 9),
            foreground="#222",
            justify="left",
            style="White.TLabel",
            anchor="w",
            wraplength=400,  # 自动换行，保证文字完整显示
            padding=(0, 0, 0, 1)
        )
        label2.pack(fill=tk.X, anchor="w")
        label_copyright = ttk.Label(
            frm_footer,
            text="© 2025 灯火通明（济宁）网络有限公司",
            font=("微软雅黑", 9),
            foreground="#1976d2",
            style="White.TLabel",
            anchor="e"
        )
        label_copyright.pack(anchor="e", pady=(0, 2), fill=tk.X)

if __name__ == "__main__":
    root = tk.Tk()
    app = SteamCodeApp(root)
    root.mainloop()
