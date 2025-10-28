
````markdown
# 🧠 Human-AutoTyper

**Human-AutoTyper** is a Python-based automation tool that simulates realistic human typing behavior on any active text field. It types out your text automatically, character by character, with customizable typing speed and random delays — just like a real person!

---

## 🚀 Features

- ⌨️ Simulates human-like typing with adjustable speed (WPM)
- 🕒 Adds random delays to mimic natural typing rhythm
- 📋 Supports text input directly or from clipboard
- 🧭 Simple Tkinter GUI for easy control
- 🧠 Failsafe — move your mouse to the top-left corner to instantly stop typing
- 🔒 Safe and lightweight — no external dependencies except standard Python libraries and `pyautogui`

---

## 🧩 Requirements

Make sure you have Python installed (≥ 3.8).  
Install the required dependencies using:

```bash
pip install pyautogui pyperclip
````

---

## 📜 Usage

1. Clone or download the project.
2. Open your terminal or IDE.
3. Run the app:

   ```bash
   python app.py
   ```
4. Enter your text or choose to paste from clipboard.
5. Set your typing speed (Words Per Minute).
6. Click **Start Typing** and place your cursor in any text field (e.g., Notepad, browser, IDE).
7. Watch your text being typed automatically!

---

## ⚙️ Configuration

You can modify or extend these options in `app.py`:

| Option               | Description                              | Default       |
| -------------------- | ---------------------------------------- | ------------- |
| `WPM`                | Words per minute typing speed            | 50            |
| `random_delay_range` | Range for random typing delay            | 0.02–0.25 sec |
| `failsafe`           | Move mouse to top-left to stop instantly | Enabled       |

---

## 🧠 Example

```python
# Example: Auto-type "Hello, world!" at 80 WPM
from app import type_text

type_text("Hello, world!", wpm=80)
```

---

## 🪶 Author

**Manish Kumar**
💻 Developer | Automation Enthusiast

📫 Connect with me on [LinkedIn](https://linkedin.com/in/)

---

## 🛡️ License

This project is licensed under the **MIT License** — feel free to use and modify it.

---

```

---

Would you like me to make it include an **animated GIF or screenshot section** (for the GUI or typing demo)? That makes the README look more engaging for GitHub.
```
