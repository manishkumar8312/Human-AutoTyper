import threading
import time
import random
import string
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import pyautogui

pyautogui.FAILSAFE = True  # Move mouse to top-left corner to stop instantly

# -------------------------
# Typing engine helpers
# -------------------------
def seconds_per_char_from_wpm(wpm):
    return 60.0 / max(1.0, (wpm * 5.0))  # average 5 chars per word

def random_delay(mean, jitter=0.15, minimum=0.002):
    sigma = mean * jitter
    return max(minimum, random.gauss(mean, sigma))

def pick_wrong_char(correct_char):
    neighbors = {
        'a': 'qs', 'b': 'vn', 'c': 'vx', 'd': 'sf', 'e': 'wr', 'f': 'dg',
        'g': 'fh', 'h': 'gj', 'i': 'uo', 'j': 'hk', 'k': 'jl', 'l': 'k;',
        'm': 'n,', 'n': 'bm', 'o': 'ip', 'p': 'o[', 'q': 'w', 'r': 'te',
        's': 'ad', 't': 'ry', 'u': 'yi', 'v': 'cb', 'w': 'qe', 'x': 'zc',
        'y': 'tu', 'z': 'x'
    }
    low = correct_char.lower()
    if low in neighbors and random.random() < 0.9:
        c = random.choice(neighbors[low])
        return c.upper() if correct_char.isupper() else c
    return random.choice(string.ascii_letters + string.digits + ",.;'")

# -------------------------
# Optimized human typing
# -------------------------
def human_type(text, wpm=250, mistake_rate=0.0, pre_delay=5.0, stop_flag=lambda: False):
    """Type text with slight human-like delay but optimized for speed."""
    base = seconds_per_char_from_wpm(wpm)
    print(f"Typing speed: {wpm} WPM")

    # Pre-delay so user can focus input box
    for i in range(int(pre_delay), 0, -1):
        if stop_flag():
            return
        print(f"Starting in {i}...")
        time.sleep(1)

    # Clean up tabs and trailing spaces before typing
    cleaned_lines = []
    for line in text.splitlines():
        # Remove leading/trailing tabs and spaces
        cleaned_lines.append(line.strip())

    # Type each line separately
    for idx, line in enumerate(cleaned_lines):
        if stop_flag():
            return

        for ch in line:
            if stop_flag():
                return

            if ch.isalnum() and random.random() < mistake_rate:
                wrong = pick_wrong_char(ch)
                pyautogui.write(wrong)
                time.sleep(random_delay(0.02))
                pyautogui.press('backspace')
                time.sleep(random_delay(0.02))

            pyautogui.write(ch)
            time.sleep(random_delay(base, 0.05))

        # Press Enter after each line (no extra spaces)
        if idx < len(cleaned_lines) - 1:
            pyautogui.press('enter')
            time.sleep(random_delay(base, 0.05))

# -------------------------
# GUI + threading
# -------------------------
class AutoTyperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Fast Auto Typer (Clipboard)")
        master.resizable(False, False)

        frm = ttk.Frame(master, padding=12)
        frm.grid(row=0, column=0)

        ttk.Label(frm, text="WPM:").grid(row=0, column=0, sticky="w")
        self.wpm_var = tk.IntVar(value=250)
        ttk.Spinbox(frm, from_=50, to=600, increment=10, textvariable=self.wpm_var, width=8).grid(row=0, column=1, padx=4)

        ttk.Label(frm, text="Pre-start delay (s):").grid(row=0, column=2, sticky="w")
        self.delay_var = tk.IntVar(value=5)
        ttk.Spinbox(frm, from_=0, to=60, textvariable=self.delay_var, width=8).grid(row=0, column=3, padx=4)

        ttk.Button(frm, text="Type Clipboard →", command=self.start_typing_from_clipboard).grid(row=1, column=0, columnspan=4, pady=8, sticky="we")

        ttk.Label(frm, text="Clipboard Preview:").grid(row=2, column=0, columnspan=4, sticky="w", pady=(8, 0))
        self.preview = tk.Text(frm, width=80, height=12, wrap="none")
        self.preview.grid(row=3, column=0, columnspan=4, pady=4)

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=4, column=0, columnspan=4, pady=8, sticky="e")
        self.stop_flag = threading.Event()
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_preview).grid(row=0, column=0, padx=4)
        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop_typing, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=4)

        ttk.Label(frm, text="Note: Move mouse to top-left to abort (failsafe). Use only for personal practice.").grid(row=5, column=0, columnspan=4, pady=(10, 0))

        self.refresh_preview()

    def refresh_preview(self):
        try:
            text = pyperclip.paste()
        except Exception:
            text = ""
        self.preview.delete("1.0", tk.END)
        self.preview.insert(tk.END, text)

    def start_typing_from_clipboard(self):
        text = pyperclip.paste()
        if not text.strip():
            messagebox.showwarning("Clipboard empty", "Copy some text first!")
            return

        wpm = int(self.wpm_var.get())
        pre_delay = int(self.delay_var.get())

        self.stop_flag.clear()
        self.stop_btn.config(state="normal")

        def worker():
            try:
                human_type(text, wpm=wpm, pre_delay=pre_delay, stop_flag=self.stop_flag.is_set)
            except Exception as e:
                print("Error:", e)
            finally:
                self.master.after(0, self._typing_done)

        threading.Thread(target=worker, daemon=True).start()

    def stop_typing(self):
        self.stop_flag.set()
        self.stop_btn.config(state="disabled")

    def _typing_done(self):
        self.stop_btn.config(state="disabled")
        messagebox.showinfo("Done", "Typing completed!")

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyperGUI(root)
    root.mainloop()
