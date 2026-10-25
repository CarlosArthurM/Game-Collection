import customtkinter as ctk
from database.lists import get_all_lists, add_list, remove_list, rename_list

class ListManagerDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_close):
        super().__init__(parent)
        self.geometry("400x500")
        self.title("Manage Lists")
        self.resizable(False, False)
        self.grab_set()

        self.on_close = on_close

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._build_create_section()
        self._build_list_section()

        self.protocol("WM_DELETE_WINDOW", self._close)

    def _build_create_section(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="ew")
        frame.columnconfigure(0, weight=1)

        self.entry_new = ctk.CTkEntry(frame, placeholder_text="New list name...")
        self.entry_new.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        ctk.CTkButton(frame, text="Create", width=80,
            fg_color="#50007E", hover_color="#370057",
            command=self._create_list
        ).grid(row=0, column=1)

    def _build_list_section(self):
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(row=1, column=0, padx=16, pady=(0, 8), sticky="nsew")
        self.scroll.columnconfigure(0, weight=1)

        self._render_lists()

    def _render_lists(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        lists = get_all_lists()

        if not lists:
            ctk.CTkLabel(self.scroll, text="No lists yet",
                text_color="gray"
            ).pack(pady=20)
            return

        for list_id, list_name in lists:
            self._build_list_row(list_id, list_name)

    def _build_list_row(self, list_id, list_name):
        row = ctk.CTkFrame(self.scroll, fg_color="#1A1A2E", corner_radius=8)
        row.pack(fill="x", pady=4)
        row.columnconfigure(0, weight=1)

        entry = ctk.CTkEntry(row, placeholder_text=list_name)
        entry.insert(0, list_name)
        entry.grid(row=0, column=0, padx=(10, 8), pady=8, sticky="ew")

        ctk.CTkButton(row, text="Save", width=60,
            fg_color="#50007E", hover_color="#370057",
            command=lambda eid=list_id, e=entry: self._rename_list(eid, e)
        ).grid(row=0, column=1, padx=(0, 4), pady=8)

        ctk.CTkButton(row, text="✕", width=36,
            fg_color="#CA0000", hover_color="#A50000",
            command=lambda eid=list_id: self._remove_list(eid)
        ).grid(row=0, column=2, padx=(0, 8), pady=8)


    def _create_list(self):
        name = self.entry_new.get().strip()
        if not name:
            return
        add_list(name)
        self.entry_new.delete(0, "end")
        self._render_lists()

    def _rename_list(self, list_id, entry):
        name = entry.get().strip()
        if not name:
            return
        rename_list(list_id, name)
        self._render_lists()

    def _remove_list(self, list_id):
        remove_list(list_id)
        self._render_lists()

    def _close(self):
        self.on_close()
        self.destroy()