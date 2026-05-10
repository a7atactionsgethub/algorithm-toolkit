#!/usr/bin/env python3
"""
WebOptimizer — Premium Image Optimizer for Web
Beautiful UI built with CustomTkinter + Pillow
"""

import os, sys, threading
from pathlib import Path

# ── Auto-install deps ──────────────────────────────────────────────────────────
def _install(pkg):
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

try:
    import customtkinter as ctk
except ImportError:
    print("Installing customtkinter..."); _install("customtkinter")
    import customtkinter as ctk

try:
    from PIL import Image, ImageOps
except ImportError:
    print("Installing Pillow..."); _install("Pillow")
    from PIL import Image, ImageOps

from tkinter import filedialog, messagebox

# ── Constants ──────────────────────────────────────────────────────────────────

SUPPORTED = {
    ".jpg",".jpeg",".png",".gif",".bmp",
    ".tiff",".tif",".webp",".ico",".heic",
    ".heif",".avif",".ppm",".pgm"
}

FMT_OPTIONS   = ["WebP  (best for web)", "JPEG", "PNG"]
FMT_EXT_MAP   = {"WebP  (best for web)": ".webp", "JPEG": ".jpg", "PNG": ".png"}
FMT_PIL_MAP   = {"WebP  (best for web)": "WEBP",  "JPEG": "JPEG", "PNG": "PNG"}

WIDTH_OPTIONS = ["Original size", "3840 px  — 4K", "1920 px  — Full HD",
                 "1280 px  — HD", "800 px   — Tablet", "480 px   — Mobile"]
WIDTH_MAP     = {
    "Original size": None, "3840 px  — 4K": 3840,
    "1920 px  — Full HD": 1920, "1280 px  — HD": 1280,
    "800 px   — Tablet": 800,  "480 px   — Mobile": 480,
}

# Palette
C_BG      = "#0a0a0f"
C_PANEL   = "#12121a"
C_CARD    = "#1a1a26"
C_BORDER  = "#252535"
C_ACCENT  = "#6c63ff"
C_CYAN    = "#00d4ff"
C_GREEN   = "#00e676"
C_RED     = "#ff4f4f"
C_TEXT    = "#e8e8f0"
C_MUTED   = "#55556a"
C_HOV     = "#7c74ff"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# ── Core optimizer ─────────────────────────────────────────────────────────────

def optimize_image(path: Path, out_dir: Path, fmt: str, quality: int, max_w):
    try:
        out_ext = FMT_EXT_MAP[fmt]
        pil_fmt = FMT_PIL_MAP[fmt]
        with Image.open(path) as img:
            img = ImageOps.exif_transpose(img)
            if pil_fmt == "JPEG":
                if img.mode in ("RGBA","LA","P"):
                    bg = Image.new("RGB", img.size, (255,255,255))
                    if img.mode == "P": img = img.convert("RGBA")
                    bg.paste(img, mask=img.split()[-1] if img.mode in ("RGBA","LA") else None)
                    img = bg
                elif img.mode != "RGB":
                    img = img.convert("RGB")
            elif pil_fmt == "WEBP":
                if img.mode not in ("RGB","RGBA"): img = img.convert("RGBA")
            elif pil_fmt == "PNG":
                if img.mode not in ("RGB","RGBA","L","P"): img = img.convert("RGBA")
            orig = path.stat().st_size
            if max_w and img.width > max_w:
                img = img.resize((max_w, int(img.height * max_w / img.width)), Image.LANCZOS)
            out = out_dir / (path.stem + out_ext)
            kw = {}
            if pil_fmt == "JPEG":  kw = {"quality": quality, "optimize": True, "progressive": True}
            elif pil_fmt == "WEBP": kw = {"quality": quality, "method": 6}
            elif pil_fmt == "PNG":  kw = {"optimize": True, "compress_level": min(9, int((100-quality)/11))}
            img.save(out, pil_fmt, **kw)
            new = out.stat().st_size
            saved = (orig - new) / orig * 100 if orig else 0
        return {"ok": True, "name": path.name, "out": out.name,
                "orig": orig, "new": new, "saved": saved}
    except Exception as e:
        return {"ok": False, "name": path.name, "error": str(e)}

def collect(paths):
    result = []
    for p in paths:
        pp = Path(p)
        if pp.is_dir():
            for f in pp.rglob("*"):
                if f.suffix.lower() in SUPPORTED and f.is_file():
                    result.append(f)
        elif pp.is_file() and pp.suffix.lower() in SUPPORTED:
            result.append(pp)
    return sorted(set(result))

def fmt_size(b):
    if b < 1024: return f"{b} B"
    if b < 1024**2: return f"{b/1024:.1f} KB"
    return f"{b/1024**2:.2f} MB"


# ── App ────────────────────────────────────────────────────────────────────────

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WebOptimizer")
        self.geometry("960x720")
        self.minsize(860, 640)
        self.configure(fg_color=C_BG)

        self._input_paths: list[str] = []
        self._output_dir: str = ""
        self._running = False

        self._build()

    # ── Build ──────────────────────────────────────────────────────────────────

    def _build(self):
        # ── Title bar ──────────────────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color=C_PANEL, corner_radius=0, height=64)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        ctk.CTkLabel(
            hdr, text="⚡  WebOptimizer",
            font=ctk.CTkFont("Segoe UI", 22, "bold"),
            text_color=C_ACCENT
        ).pack(side="left", padx=28, pady=18)

        ctk.CTkLabel(
            hdr, text="batch image optimizer for the web",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=C_MUTED
        ).pack(side="left", pady=18)

        self._stats_label = ctk.CTkLabel(
            hdr, text="",
            font=ctk.CTkFont("Segoe UI", 12, "bold"),
            text_color=C_GREEN
        )
        self._stats_label.pack(side="right", padx=28)

        # ── Body ───────────────────────────────────────────────────────────────
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=16)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        self._build_left(body)
        self._build_right(body)

        # ── Bottom bar ─────────────────────────────────────────────────────────
        bottom = ctk.CTkFrame(self, fg_color=C_PANEL, corner_radius=0, height=80)
        bottom.pack(fill="x", side="bottom")
        bottom.pack_propagate(False)

        inner = ctk.CTkFrame(bottom, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=24, pady=16)

        self._progress = ctk.CTkProgressBar(inner, height=6,
                                             progress_color=C_ACCENT,
                                             fg_color=C_BORDER)
        self._progress.set(0)
        self._progress.pack(fill="x", pady=(0, 10))

        row = ctk.CTkFrame(inner, fg_color="transparent")
        row.pack(fill="x")

        self._status = ctk.CTkLabel(row, text="Ready — add images and choose output folder",
                                    font=ctk.CTkFont("Segoe UI", 11),
                                    text_color=C_MUTED, anchor="w")
        self._status.pack(side="left")

        self._run_btn = ctk.CTkButton(
            row, text="⚡  Optimize Images",
            font=ctk.CTkFont("Segoe UI", 13, "bold"),
            fg_color=C_ACCENT, hover_color=C_HOV,
            text_color="white", corner_radius=10,
            width=200, height=38,
            command=self._run
        )
        self._run_btn.pack(side="right")

    def _build_left(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(3, weight=1)
        frame.columnconfigure(0, weight=1)

        # ── Input section ──────────────────────────────────────────────────────
        self._section(frame, "INPUT FILES").grid(row=0, column=0, sticky="w", pady=(0, 6))

        inp_card = ctk.CTkFrame(frame, fg_color=C_CARD, corner_radius=12,
                                border_width=1, border_color=C_BORDER)
        inp_card.grid(row=1, column=0, sticky="nsew")
        inp_card.rowconfigure(0, weight=1)
        inp_card.columnconfigure(0, weight=1)

        self._file_list = ctk.CTkScrollableFrame(inp_card, fg_color="transparent",
                                                  scrollbar_button_color=C_BORDER,
                                                  scrollbar_button_hover_color=C_ACCENT)
        self._file_list.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self._file_list.columnconfigure(0, weight=1)

        self._show_empty()

        btn_row = ctk.CTkFrame(inp_card, fg_color="transparent")
        btn_row.grid(row=1, column=0, sticky="ew", padx=14, pady=10)

        ctk.CTkButton(btn_row, text="＋  Add Images",
                       font=ctk.CTkFont("Segoe UI", 12),
                       fg_color=C_ACCENT, hover_color=C_HOV,
                       corner_radius=8, height=34,
                       command=self._add_files).pack(side="left", padx=(0, 8))

        ctk.CTkButton(btn_row, text="📁  Add Folder",
                       font=ctk.CTkFont("Segoe UI", 12),
                       fg_color=C_CARD, hover_color=C_BORDER,
                       border_width=1, border_color=C_BORDER,
                       corner_radius=8, height=34,
                       command=self._add_folder).pack(side="left")

        ctk.CTkButton(btn_row, text="✕  Clear",
                       font=ctk.CTkFont("Segoe UI", 11),
                       fg_color="transparent", hover_color=C_BORDER,
                       text_color=C_MUTED, corner_radius=8, height=34,
                       command=self._clear).pack(side="right")

        self._count_label = ctk.CTkLabel(inp_card, text="0 files selected",
                                          font=ctk.CTkFont("Segoe UI", 10),
                                          text_color=C_MUTED)
        self._count_label.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 10))

        # ── Log section ────────────────────────────────────────────────────────
        self._section(frame, "ACTIVITY LOG").grid(row=2, column=0, sticky="w", pady=(16, 6))

        log_card = ctk.CTkFrame(frame, fg_color=C_CARD, corner_radius=12,
                                 border_width=1, border_color=C_BORDER)
        log_card.grid(row=3, column=0, sticky="nsew")
        log_card.rowconfigure(0, weight=1)
        log_card.columnconfigure(0, weight=1)

        self._log_box = ctk.CTkTextbox(
            log_card, fg_color="transparent",
            font=ctk.CTkFont("Cascadia Code", 10),
            text_color=C_TEXT, wrap="word",
            scrollbar_button_color=C_BORDER,
            scrollbar_button_hover_color=C_ACCENT,
            state="disabled"
        )
        self._log_box.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self._log_box.tag_config("ok",   foreground=C_GREEN)
        self._log_box.tag_config("err",  foreground=C_RED)
        self._log_box.tag_config("info", foreground=C_CYAN)
        self._log_box.tag_config("dim",  foreground=C_MUTED)

    def _build_right(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=1, sticky="nsew")
        frame.columnconfigure(0, weight=1)

        # ── Settings ───────────────────────────────────────────────────────────
        self._section(frame, "SETTINGS").grid(row=0, column=0, sticky="w", pady=(0, 6))

        settings = ctk.CTkFrame(frame, fg_color=C_CARD, corner_radius=12,
                                 border_width=1, border_color=C_BORDER)
        settings.grid(row=1, column=0, sticky="ew")
        settings.columnconfigure(0, weight=1)

        pad = {"padx": 20, "pady": (14, 0)}

        # Format
        ctk.CTkLabel(settings, text="Output Format",
                     font=ctk.CTkFont("Segoe UI", 11, "bold"),
                     text_color=C_TEXT).grid(row=0, column=0, sticky="w", **pad)
        self._fmt_var = ctk.StringVar(value=FMT_OPTIONS[0])
        ctk.CTkSegmentedButton(
            settings, values=FMT_OPTIONS,
            variable=self._fmt_var,
            font=ctk.CTkFont("Segoe UI", 10),
            fg_color=C_BORDER, selected_color=C_ACCENT,
            selected_hover_color=C_HOV,
            unselected_color=C_BORDER,
            unselected_hover_color="#2a2a3a",
            text_color=C_TEXT, corner_radius=8,
        ).grid(row=1, column=0, sticky="ew", padx=20, pady=(6, 0))

        # Quality
        ctk.CTkLabel(settings, text="Quality",
                     font=ctk.CTkFont("Segoe UI", 11, "bold"),
                     text_color=C_TEXT).grid(row=2, column=0, sticky="w", **pad)

        q_row = ctk.CTkFrame(settings, fg_color="transparent")
        q_row.grid(row=3, column=0, sticky="ew", padx=20, pady=(4, 0))
        q_row.columnconfigure(0, weight=1)

        self._quality_var = ctk.IntVar(value=82)
        self._q_val_label = ctk.CTkLabel(q_row, text="82",
                                          font=ctk.CTkFont("Segoe UI", 16, "bold"),
                                          text_color=C_ACCENT, width=40)
        self._q_val_label.grid(row=0, column=1, padx=(10, 0))

        ctk.CTkSlider(q_row, from_=10, to=100,
                       variable=self._quality_var,
                       command=lambda v: self._q_val_label.configure(text=str(int(v))),
                       progress_color=C_ACCENT, button_color=C_ACCENT,
                       button_hover_color=C_HOV, fg_color=C_BORDER,
                       height=16).grid(row=0, column=0, sticky="ew")

        # Quality hints
        hint = ctk.CTkFrame(settings, fg_color="transparent")
        hint.grid(row=4, column=0, sticky="ew", padx=20, pady=(2, 0))
        ctk.CTkLabel(hint, text="10  smaller →",
                     font=ctk.CTkFont("Segoe UI", 9),
                     text_color=C_MUTED).pack(side="left")
        ctk.CTkLabel(hint, text="← larger  100",
                     font=ctk.CTkFont("Segoe UI", 9),
                     text_color=C_MUTED).pack(side="right")

        # Max width
        ctk.CTkLabel(settings, text="Max Width",
                     font=ctk.CTkFont("Segoe UI", 11, "bold"),
                     text_color=C_TEXT).grid(row=5, column=0, sticky="w", **pad)
        self._width_var = ctk.StringVar(value=WIDTH_OPTIONS[0])
        ctk.CTkComboBox(
            settings, values=WIDTH_OPTIONS, variable=self._width_var,
            font=ctk.CTkFont("Segoe UI", 11),
            fg_color=C_BORDER, border_color=C_BORDER,
            button_color=C_ACCENT, button_hover_color=C_HOV,
            dropdown_fg_color=C_CARD, dropdown_hover_color=C_BORDER,
            text_color=C_TEXT, state="readonly"
        ).grid(row=6, column=0, sticky="ew", padx=20, pady=(6, 16))

        # ── Output folder ──────────────────────────────────────────────────────
        self._section(frame, "OUTPUT FOLDER").grid(row=2, column=0, sticky="w", pady=(20, 6))

        out_card = ctk.CTkFrame(frame, fg_color=C_CARD, corner_radius=12,
                                 border_width=1, border_color=C_BORDER)
        out_card.grid(row=3, column=0, sticky="ew")
        out_card.columnconfigure(0, weight=1)

        self._out_path_label = ctk.CTkLabel(
            out_card, text="No folder selected",
            font=ctk.CTkFont("Segoe UI", 10),
            text_color=C_MUTED, anchor="w", wraplength=280
        )
        self._out_path_label.grid(row=0, column=0, sticky="w", padx=16, pady=(14, 6))

        ctk.CTkButton(
            out_card, text="📂  Choose Output Folder",
            font=ctk.CTkFont("Segoe UI", 12),
            fg_color=C_ACCENT, hover_color=C_HOV,
            corner_radius=8, height=34,
            command=self._choose_out
        ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 14))

        # ── Stats cards ────────────────────────────────────────────────────────
        self._section(frame, "SESSION STATS").grid(row=4, column=0, sticky="w", pady=(20, 6))

        stats_row = ctk.CTkFrame(frame, fg_color="transparent")
        stats_row.grid(row=5, column=0, sticky="ew")
        stats_row.columnconfigure((0, 1, 2), weight=1)

        self._stat_processed = self._stat_card(stats_row, "Processed", "0", 0)
        self._stat_saved     = self._stat_card(stats_row, "Saved",     "0 KB", 1)
        self._stat_pct       = self._stat_card(stats_row, "Reduction", "0%", 2)

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _section(self, parent, text):
        return ctk.CTkLabel(parent, text=text,
                            font=ctk.CTkFont("Segoe UI", 9, "bold"),
                            text_color=C_MUTED)

    def _stat_card(self, parent, label, value, col):
        card = ctk.CTkFrame(parent, fg_color=C_CARD, corner_radius=10,
                             border_width=1, border_color=C_BORDER)
        card.grid(row=0, column=col, sticky="ew",
                  padx=(0 if col == 0 else 6, 0))
        val_lbl = ctk.CTkLabel(card, text=value,
                                font=ctk.CTkFont("Segoe UI", 18, "bold"),
                                text_color=C_ACCENT)
        val_lbl.pack(pady=(12, 2))
        ctk.CTkLabel(card, text=label,
                     font=ctk.CTkFont("Segoe UI", 10),
                     text_color=C_MUTED).pack(pady=(0, 10))
        return val_lbl

    def _show_empty(self):
        for w in self._file_list.winfo_children():
            w.destroy()
        ctk.CTkLabel(
            self._file_list,
            text="No images selected\n\nClick  ＋ Add Images  or  📁 Add Folder",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=C_MUTED, justify="center"
        ).grid(row=0, column=0, pady=40)

    def _log(self, msg, tag=""):
        self._log_box.configure(state="normal")
        self._log_box.insert("end", msg + "\n", tag)
        self._log_box.see("end")
        self._log_box.configure(state="disabled")

    def _set_status(self, msg, color=None):
        self._status.configure(text=msg, text_color=color or C_MUTED)
        self.update_idletasks()

    # ── Actions ────────────────────────────────────────────────────────────────

    def _add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Images", " ".join(f"*{e}" for e in SUPPORTED)),
                       ("All files", "*.*")]
        )
        for f in files:
            if f not in self._input_paths:
                self._input_paths.append(f)
        self._refresh_list()

    def _add_folder(self):
        d = filedialog.askdirectory(title="Select Image Folder")
        if d and d not in self._input_paths:
            self._input_paths.append(d)
        self._refresh_list()

    def _clear(self):
        self._input_paths.clear()
        self._refresh_list()

    def _refresh_list(self):
        imgs = collect(self._input_paths)
        for w in self._file_list.winfo_children():
            w.destroy()

        if not imgs:
            self._show_empty()
        else:
            for i, img in enumerate(imgs):
                row = ctk.CTkFrame(self._file_list, fg_color="transparent")
                row.grid(row=i, column=0, sticky="ew", pady=1)
                row.columnconfigure(1, weight=1)

                ctk.CTkLabel(row, text="●", font=ctk.CTkFont("Segoe UI", 8),
                              text_color=C_ACCENT, width=16).grid(row=0, column=0, padx=(4, 6))

                ext = img.suffix.lower()
                color = C_CYAN if ext in (".png",".gif",".ico") else \
                        C_GREEN if ext in (".webp",) else C_TEXT

                ctk.CTkLabel(row, text=img.name,
                              font=ctk.CTkFont("Segoe UI", 11),
                              text_color=color, anchor="w").grid(row=0, column=1, sticky="w")

                size_str = fmt_size(img.stat().st_size) if img.exists() else ""
                ctk.CTkLabel(row, text=size_str,
                              font=ctk.CTkFont("Segoe UI", 9),
                              text_color=C_MUTED).grid(row=0, column=2, padx=8)

        self._count_label.configure(
            text=f"{len(imgs)} file{'s' if len(imgs)!=1 else ''} selected"
        )

    def _choose_out(self):
        d = filedialog.askdirectory(title="Choose Output Folder")
        if d:
            self._output_dir = d
            short = d if len(d) <= 42 else "…" + d[-40:]
            self._out_path_label.configure(text=short, text_color=C_TEXT)

    # ── Run ────────────────────────────────────────────────────────────────────

    def _run(self):
        if self._running: return
        imgs = collect(self._input_paths)
        if not imgs:
            messagebox.showwarning("No Images", "Add at least one image or folder.")
            return
        if not self._output_dir:
            messagebox.showwarning("No Output", "Choose an output folder first.")
            return

        self._running = True
        self._run_btn.configure(state="disabled", text="⏳  Working…")
        self._progress.set(0)
        self._stats_label.configure(text="")
        self._log_box.configure(state="normal")
        self._log_box.delete("1.0", "end")
        self._log_box.configure(state="disabled")
        self._stat_processed.configure(text="0")
        self._stat_saved.configure(text="0 KB")
        self._stat_pct.configure(text="0%")

        threading.Thread(target=self._worker, args=(imgs,), daemon=True).start()

    def _worker(self, imgs):
        fmt    = self._fmt_var.get()
        quality = self._quality_var.get()
        max_w  = WIDTH_MAP[self._width_var.get()]
        out_dir = Path(self._output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        ok_n = err_n = 0
        total_orig = total_new = 0

        self._log(f"Starting {len(imgs)} image(s)", "info")
        self._log(f"Format: {fmt.strip()}  |  Quality: {quality}  |  Max Width: {max_w or 'none'}", "dim")
        self._log("─" * 50, "dim")

        for i, img in enumerate(imgs, 1):
            self._set_status(f"Processing {i}/{len(imgs)}  —  {img.name}")
            r = optimize_image(img, out_dir, fmt, quality, max_w)

            if r["ok"]:
                ok_n += 1
                total_orig += r["orig"]
                total_new  += r["new"]
                self._log(
                    f"✓  {r['name']}\n"
                    f"   {fmt_size(r['orig'])} → {fmt_size(r['new'])}  ({r['saved']:.1f}% saved)",
                    "ok"
                )
            else:
                err_n += 1
                self._log(f"✗  {r['name']}\n   {r['error']}", "err")

            self._progress.set(i / len(imgs))
            saved_bytes = total_orig - total_new
            self._stat_processed.configure(text=str(ok_n + err_n))
            self._stat_saved.configure(text=fmt_size(max(0, saved_bytes)))
            pct = saved_bytes / total_orig * 100 if total_orig else 0
            self._stat_pct.configure(text=f"{pct:.1f}%")
            self.update_idletasks()

        self._log("─" * 50, "dim")
        self._log(f"Done  —  {ok_n} optimized  |  {err_n} failed", "info")
        pct = (total_orig - total_new) / total_orig * 100 if total_orig else 0
        self._stats_label.configure(
            text=f"✓ {ok_n} done  ·  {fmt_size(max(0, total_orig - total_new))} saved  ·  {pct:.1f}% smaller"
        )
        self._set_status("All done!", C_GREEN)
        self._run_btn.configure(state="normal", text="⚡  Optimize Images")
        self._running = False


# ── Entry ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()