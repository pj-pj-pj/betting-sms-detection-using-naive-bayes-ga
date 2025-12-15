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
    prediction = model.predict(text_vec)[0]

    if prediction == 1:
        result = "BETTING-RELATED SMS (SPAM)"
        color = "#d32f2f"
    else:
        result = "NON-BETTING SMS"
        color = "#388e3c"

    result_label.config(text=f"Prediction: {result}", fg=color)

def insert_suggestion(text):
    entry.delete("1.0", tk.END)
    entry.insert(tk.END, text)


window = tk.Tk()
window.title("Betting SMS Classifier")
window.geometry("820x900")
window.configure(bg="#f5f7fa")


TITLE_FONT = ("Segoe UI", 16, "bold")
TEXT_FONT = ("Segoe UI", 11)
BTN_FONT = ("Segoe UI", 11, "bold")

PRIMARY_COLOR = "#1976d2"
CARD_BG = "#ffffff"


main_frame = tk.Frame(window, bg="#f5f7fa")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)


title_label = tk.Label(
    main_frame,
    text="📩 Betting SMS Detection",
    font=TITLE_FONT,
    bg="#f5f7fa",
    fg="#263238"
)
title_label.pack(anchor="w", pady=(0, 10))

subtitle = tk.Label(
    main_frame,
    text="Paste an SMS message or choose a sample below",
    font=("Segoe UI", 10),
    bg="#f5f7fa",
    fg="#607d8b"
)
subtitle.pack(anchor="w", pady=(0, 15))


input_card = tk.Frame(main_frame, bg=CARD_BG, bd=1, relief="solid")
input_card.pack(fill="x", pady=10)

entry = tk.Text(
    input_card,
    height=6,
    font=TEXT_FONT,
    wrap="word",
    bd=0
)
entry.pack(fill="x", padx=12, pady=12)


btn = tk.Button(
    main_frame,
    text="Classify Message",
    font=BTN_FONT,
    bg=PRIMARY_COLOR,
    fg="white",
    activebackground="#1565c0",
    activeforeground="white",
    bd=0,
    padx=20,
    pady=8,
    command=classify_message
)
btn.pack(pady=10)

window.bind('<Return>', lambda event: classify_message())

result_label = tk.Label(
    main_frame,
    text="",
    font=("Segoe UI", 12, "bold"),
    bg="#f5f7fa"
)
result_label.pack(pady=10)


suggestions_frame = tk.LabelFrame(
    main_frame,
    text="Sample SMS Suggestions",
    font=("Segoe UI", 11, "bold"),
    bg="#f5f7fa",
    fg="#37474f",
    padx=10,
    pady=10
)
suggestions_frame.pack(fill="both", expand=True, pady=10)

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
        suggestions_frame,
        text=msg[:80] + "..." if len(msg) > 80 else msg,
        anchor="w",
        justify="left",
        wraplength=720,
        font=("Segoe UI", 10),
        bg=CARD_BG,
        fg="#263238",
        bd=1,
        relief="solid",
        padx=10,
        pady=10,
        command=lambda m=msg: insert_suggestion(m)
    )
    btn.pack(fill="x", pady=4)

window.mainloop()
