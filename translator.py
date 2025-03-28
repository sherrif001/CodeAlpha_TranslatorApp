import tkinter as tk
from tkinter import ttk
from googletrans import Translator, LANGUAGES

translator = Translator()

def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    target_lang = lang_entry.get().strip()

    if not text:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Please enter text to translate.")
        return
    
    try:
        translated = translator.translate(text, dest=target_lang)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated.text)
    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: {str(e)}")

def clear_text():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

def open_language_window():
    """ Opens a window with supported languages and selects one on click. """
    lang_window = tk.Toplevel(root)
    lang_window.title("Select a Language")
    lang_window.geometry("300x400")
    lang_window.configure(bg="#1E1E1E")

    tk.Label(lang_window, text="Select a Language:", fg="white", bg="#1E1E1E", font=("Arial", 12, "bold")).pack(pady=5)

    lang_listbox = tk.Listbox(lang_window, bg="#2E2E2E", fg="white", font=("Arial", 12), width=40)
    lang_listbox.pack(padx=10, pady=5, fill="both", expand=True)

    for code, name in LANGUAGES.items():
        lang_listbox.insert(tk.END, f"{name} ({code})")

    def set_language(event):
        """ Set the selected language as the target language. """
        selection = lang_listbox.get(lang_listbox.curselection())
        selected_code = selection.split("(")[-1][:-1]  

        if "lang_entry" not in globals():
            switch_page("translate")

        lang_entry.delete(0, tk.END)
        lang_entry.insert(0, selected_code)
        lang_window.destroy()

    lang_listbox.bind("<Double-Button-1>", set_language)

def switch_page(page):
    """ Switch between Home and Translate pages. """
    global lang_entry, input_text, output_text  

    for widget in main_frame.winfo_children():
        widget.destroy()

    if page == "home":
        tk.Label(main_frame, text="Welcome to Translator 1.0!", fg="white", bg="#121212", font=("Arial", 18, "bold")).pack(pady=10)
        tk.Label(main_frame, text="Made by Sherif Tamer", fg="white", bg="#121212", font=("Arial", 14)).pack(pady=5)
        tk.Label(main_frame, text="Uses Googletrans", fg="gray", bg="#121212", font=("Arial", 12)).pack(pady=10)
    elif page == "translate":
        input_text = tk.Text(main_frame, height=5, width=80, bg="#2E2E2E", fg="white", font=("Arial", 12))
        input_text.pack(pady=10, padx=20)

        tk.Label(main_frame, text="Translated Text", fg="white", bg="#121212", font=("Arial", 16, "bold")).pack()

        output_text = tk.Text(main_frame, height=5, width=80, bg="#2E2E2E", fg="white", font=("Arial", 12))
        output_text.pack(pady=10, padx=20)

        tk.Label(main_frame, text="Target Language Code:", fg="white", bg="#121212").pack()
        lang_entry = tk.Entry(main_frame, width=10, bg="#2E2E2E", fg="white", font=("Arial", 12))
        lang_entry.pack(pady=5)

        button_frame = tk.Frame(main_frame, bg="#121212")
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Translate", command=translate_text).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Clear", command=clear_text).grid(row=0, column=1, padx=10)

root = tk.Tk()
root.title("Translator 1.0")
root.geometry("800x500")
root.configure(bg="#121212")

nav_frame = tk.Frame(root, bg="#1E1E1E", height=40)
nav_frame.pack(fill="x")

def on_hover(widget, color):
    widget.bind("<Enter>", lambda e: widget.config(fg=color))
    widget.bind("<Leave>", lambda e: widget.config(fg="white"))

tk.Label(nav_frame, text="  TranslatorPro  ", fg="white", bg="#1E1E1E", font=("Arial", 14, "bold")).pack(side="left", padx=10)

home_label = tk.Label(nav_frame, text="Home", fg="white", bg="#1E1E1E", font=("Arial", 12), cursor="hand2")
home_label.pack(side="left", padx=15)
home_label.bind("<Button-1>", lambda e: switch_page("home"))
on_hover(home_label, "#3A68D0")

translate_label = tk.Label(nav_frame, text="Translate", fg="white", bg="#1E1E1E", font=("Arial", 12), cursor="hand2")
translate_label.pack(side="left", padx=15)
translate_label.bind("<Button-1>", lambda e: switch_page("translate"))
on_hover(translate_label, "#3A68D0")

languages_label = tk.Label(nav_frame, text="Languages", fg="white", bg="#1E1E1E", font=("Arial", 12), cursor="hand2")
languages_label.pack(side="left", padx=15)
languages_label.bind("<Button-1>", lambda e: open_language_window())
on_hover(languages_label, "#3A68D0")

main_frame = tk.Frame(root, bg="#121212")
main_frame.pack(fill="both", expand=True)

switch_page("home")

root.mainloop()