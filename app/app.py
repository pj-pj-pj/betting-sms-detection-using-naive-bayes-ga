import tkinter as tk
from tkinter import messagebox
import pickle


with open("vectorizer.pkl", "rb") as f:
    cv = pickle.load(f)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Classification logic
def classify_message():
    text = entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Please enter a message.")
        return

    text_vec = cv.transform([text])
    prediction = new_func(text_vec)

    if prediction == 1:
        result = "BETTING-RELATED SMS (SPAM)"
        color = "#d32f2f"
    else:
        result = "NON-BETTING SMS"
        color = "#388e3c"

    result_label.config(text=f"Prediction: {result}", fg=color)

def new_func(text_vec):
    prediction = model.predict(text_vec)[0]
    return prediction

def insert_suggestion(text):
    entry.delete("1.0", tk.END)
    entry.insert(tk.END, text)


window = tk.Tk()
window.title("Betting SMS Classifier")
window.geometry("820x850")
window.configure(bg="#f7f9fc")


def _center_window(win, width=820, height=900):
    try:
        win.eval('tk::PlaceWindow . center')
    except tk.TclError:
        win.update_idletasks()
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        win.geometry(f"{width}x{height}+{x}+{y}")


_center_window(window, 820, 850)


TITLE_FONT = ("Segoe UI", 16, "bold")
TEXT_FONT = ("Segoe UI", 11)
BTN_FONT = ("Segoe UI", 11, "bold")

PRIMARY_COLOR = "#2563eb"
PRIMARY_ACTIVE = "#1d4ed8"
TEXT_COLOR = "#0f172a"
MUTED_COLOR = "#475569"
CARD_BG = "#ffffff"


main_frame = tk.Frame(window, bg="#f7f9fc")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)


title_label = tk.Label(
    main_frame,
    text="📩 Betting SMS Detection",
    font=TITLE_FONT,
    bg="#f7f9fc",
    fg=TEXT_COLOR
)
title_label.pack(anchor="w", pady=(0, 10))

subtitle = tk.Label(
    main_frame,
    text="Paste an SMS message or choose a sample below",
    font=("Segoe UI", 10),
    bg="#f7f9fc",
    fg=MUTED_COLOR
)
subtitle.pack(anchor="w", pady=(0, 15))

input_container = tk.Frame(main_frame, bg="#414141")  # subtle shadow layer
input_container.pack(fill="x", pady=10)

input_card = tk.Frame(input_container, bg=CARD_BG, bd=0, relief="flat")
input_card.pack(fill="x")


entry = tk.Text(
    input_card,
    height=5,
    font=TEXT_FONT,
    wrap="word",
    bd=0,
    relief="flat",
    highlightthickness=1,
    highlightbackground="#272727",  
    highlightcolor="#2f2f2f",       
    background=CARD_BG,
    fg=TEXT_COLOR
)
entry.pack(fill="x", padx=12, pady=12)


btn = tk.Button(
    main_frame,
    text="Classify Message",
    font=BTN_FONT,
    bg=PRIMARY_COLOR,
    fg="#272727",
    activebackground="#2466a9",
    activeforeground="#2466a9",
    bd=0,
    relief="flat",
    padx=20,
    pady=10,
    command=classify_message
)
btn.pack(pady=10)

window.bind('<Return>', lambda event: classify_message())

result_label = tk.Label(
    main_frame,
    text="",
    font=("Segoe UI", 12, "bold"),
    bg="#f7f9fc",
    fg=TEXT_COLOR
)
result_label.pack(pady=10)

suggestions_frame = tk.LabelFrame(
    main_frame,
    text="Sample SMS Suggestions",
    font=("Segoe UI", 11, "bold"),
    bg="#f7f9fc",
    fg=TEXT_COLOR,
    bd=0,
    relief="flat",
    padx=10,
    pady=10,
    highlightthickness=0
)
suggestions_frame.pack(fill="both", expand=True, pady=10)

# Scrollable area for suggestions so they remain visible when the window is resized
y_scrollbar = tk.Scrollbar(
    suggestions_frame,
    orient="vertical"
)
x_scrollbar = tk.Scrollbar(
    suggestions_frame,
    orient="horizontal"
)
canvas = tk.Canvas(
    suggestions_frame,
    bg="#f7f9fc",
    highlightthickness=0,
    bd=0,
    yscrollcommand=y_scrollbar.set,
    xscrollcommand=x_scrollbar.set
)
y_scrollbar.config(command=canvas.yview)
x_scrollbar.config(command=canvas.xview)
y_scrollbar.pack(side="right", fill="y")
x_scrollbar.pack(side="bottom", fill="x")
canvas.pack(side="left", fill="both", expand=True)

inner_frame = tk.Frame(canvas, bg="#f7f9fc")
inner_window = canvas.create_window((0, 0), window=inner_frame, anchor="nw")


def _update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


inner_frame.bind("<Configure>", _update_scroll_region)

suggestions = [
    "get 12% or up to p1,500 off on klook w/ bdo credit cards! "
    "use code bdoweekend until 7/27/25 (fri-sun). search klook at deals.bdo.com.ph for t&c. dti221074",
    "chill out with big wins! get 7,777p free bonus at panaloka.de "
    "coolly navigate the mystery ampao to win 500,000p! start your cool adventure!",
    "magdeposito ng 100p, makakuha ng 100p na libre 1q2w3e8.ca",
    "sorry, postpaid subscribers are not allowed to use this service. "
    "please call customer care hotline at *888 for assistance.",
    "don't miss payday bonanza at winpnow.eu! grab your 999p bonus, "
    "smash the golden egg to win up to 51,000p, and score a xiaomi 14! play now for big wins",
    "stay always connected! check your balance regularly and stay up-to-date "
    "with the latest offers via the smart app!",
    "your payment of p249.00 to netflix has been successfully processed on "
    "07-25-24 07:27:18 am. ref. no. 067918304",
    "<real name>, join the fun! welcome bonus up to p2,000 at sugarplay + "
    "baccarat giveaways up to p2,500. daily rebate up to p58,888. join now. sgbett2.com"
]

for msg in suggestions:
    btn = tk.Button(
        inner_frame,
        text=msg,
        anchor="w",
        justify="left",
        wraplength=0,
        font=("Segoe UI", 10),
        bg=CARD_BG,
        fg=TEXT_COLOR,
        bd=0,
        relief="flat",
        highlightthickness=1,
        highlightbackground="#e2e8f0",
        activebackground="#eef2f7",
        padx=10,
        pady=10,
        command=lambda m=msg: insert_suggestion(m)
    )
    btn.pack(fill="x", pady=4)

window.mainloop()
