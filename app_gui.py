# app_gui.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from agent_backend import graph, builder

def run_agent(symptom_input):
    def get_symptom_ui(state):
        state["symptom"] = symptom_input
        return state

    builder.update_node("get_symptom", get_symptom_ui)
    graph_ui = builder.compile()
    result = graph_ui.invoke({})

    return result.get("category", "Unknown").capitalize(), result.get("answer", "No response.")

# Create the main window
window = tk.Tk()
window.title("🩺 Symptom Classifier")
window.geometry("500x350")
window.configure(bg="#f7f7f7")

# Header Label
header = tk.Label(window, text="Symptom Classifier", font=("Arial", 20, "bold"), bg="#f7f7f7", fg="#4a4a4a")
header.pack(pady=20)

# Entry field
symptom_label = tk.Label(window, text="Enter your symptom:", font=("Arial", 12), bg="#f7f7f7")
symptom_label.pack()
symptom_entry = tk.Entry(window, font=("Arial", 12), width=40)
symptom_entry.pack(pady=5)

# Output box
output_frame = tk.Frame(window, bg="#ffffff", bd=2, relief=tk.GROOVE)
output_frame.pack(pady=20, fill="both", expand=True, padx=20)

output_text = tk.Label(output_frame, text="Diagnosis will appear here...", font=("Arial", 12), bg="#ffffff", justify="left", wraplength=450)
output_text.pack(padx=10, pady=10)

# Button callback
def classify_symptom():
    symptom = symptom_entry.get().strip()
    if not symptom:
        messagebox.showwarning("Input Error", "Please enter a symptom.")
        return
    category, advice = run_agent(symptom)
    output_text.config(
        text=f"📝 Symptom: {symptom}\n📂 Category: {category}\n💡 Advice: {advice}",
        fg="#333333"
    )

# Submit Button
submit_btn = tk.Button(window, text="Classify", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=classify_symptom)
submit_btn.pack(pady=10)

# Run the app
window.mainloop()
