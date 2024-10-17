import tkinter as tk
from tkinter import messagebox
import random

class MatchGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Kelime Eşleştirme Oyunu")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="white")

        self.title_label = tk.Label(self.root, text="Fill in the blanks below with “was” or “were”.", bg="white", fg="black", font=("Arial", 24, "bold"))
        self.title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.canvas_frame = tk.Frame(self.root, width=800, height=600, bg="lightblue")
        self.canvas_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.was_labels = []
        self.were_labels = []

        for i in range(6):
         was_label = tk.Label(self.canvas_frame, text="was", bg="lightgray", padx=25, pady=12, relief="solid", bd=2, font=("Arial", 18))
         was_label.place(x=1150 + i*2, y=200 + i*10)
         self.was_labels.append(was_label)

        for i in range(6):
          were_label = tk.Label(self.canvas_frame, text="were", bg="lightgray", padx=25, pady=12, relief="solid", bd=2, font=("Arial", 18))
          were_label.place(x=1150 + i*2, y=350 + i*10)
          self.were_labels.append(were_label)


        self.paragraphs = [
            "The weather ____ nice yesterday.",
            "They ____ at the party last night.",
            "She ____ very happy with her exam results.",
            "We ____ all tired after the long trip.",
            "My brother ____ a great soccer player when he was younger.",
            "The students ____ excited about the field trip.",
            "It ____ a difficult exam for everyone.",
            "There ____ many people at the concert.",
            "I ____ late to the meeting yesterday.",
            "The books ____ on the table."
        ]

        self.drag_data = {"word": None, "start_x": 0, "start_y": 0, "offset_x": 0, "offset_y": 0}

        self.correct_matches = {
            "was": [0, 2, 4, 6, 8],
            "were": [1, 3, 5, 7, 9]
        }

        for label in self.was_labels:
         label.bind("<Button-1>", self.start_drag)
         label.bind("<B1-Motion>", self.on_drag)
         label.bind("<ButtonRelease-1>", self.stop_drag)

        for label in self.were_labels:
         label.bind("<Button-1>", self.start_drag)
         label.bind("<B1-Motion>", self.on_drag)
         label.bind("<ButtonRelease-1>", self.stop_drag)



        self.drop_labels = []
        for i, paragraph in enumerate(self.paragraphs):
            label1 = tk.Label(self.canvas_frame, text=paragraph.split("____")[0], bg="white", padx=20, pady=12, font=("Arial", 18))
            label1.grid(row=i, column=0, sticky="e", padx=(100, 2))

            drop_label = tk.Label(self.canvas_frame, text="____", bg="lightblue", width=12, padx=20, pady=12, relief="solid", bd=2, font=("Arial", 18))
            drop_label.grid(row=i, column=1, padx=20, pady=2)
            self.drop_labels.append(drop_label)

            label2 = tk.Label(self.canvas_frame, text=paragraph.split("____")[1], bg="white", padx=25, pady=12, font=("Arial", 18))
            label2.grid(row=i, column=2, sticky="w", padx=(2, 200))

        button_width = 20

        check_button = tk.Button(self.canvas_frame, text="Check The Answers ", command=self.check_answers, width=button_width, padx=10, pady=5)
        check_button.grid(row=len(self.paragraphs), column=0, pady=(20, 10))

        reset_button = tk.Button(self.canvas_frame, text="Reset", command=self.reset_game, width=button_width, padx=10, pady=5)
        reset_button.grid(row=len(self.paragraphs), column=1, pady=(20, 10))

        exit_button = tk.Button(self.canvas_frame, text="Exit", command=self.exit_game, width=button_width, padx=10, pady=5)
        exit_button.grid(row=len(self.paragraphs), column=2, pady=(20, 10))

    def check_answers(self):
        correct_count = 0
        for i, drop_label in enumerate(self.drop_labels):
            word = drop_label.cget("text")
            if i in self.correct_matches.get(word, []):
                correct_count += 1

        messagebox.showinfo("Result", f"Correct Answers: {correct_count}/{len(self.paragraphs)}")

    def is_overlapping(self, widget1, widget2):
          x1, y1, x2, y2 = widget1.winfo_rootx(), widget1.winfo_rooty(), widget1.winfo_rootx() + widget1.winfo_width(), widget1.winfo_rooty() + widget1.winfo_height()
          x1_d, y1_d, x2_d, y2_d = widget2.winfo_rootx(), widget2.winfo_rooty(), widget2.winfo_rootx() + widget2.winfo_width(), widget2.winfo_rooty() + widget2.winfo_height()

          return x1 < x2_d and x2 > x1_d and y1 < y2_d and y2 > y1_d

    def stop_drag(self, event):
      label = self.drag_data["word"]
      placed = False

      for drop_label in self.drop_labels:
        if self.is_overlapping(label, drop_label):
            drop_label.config(text=label.cget("text"), bg="lightblue")
            placed = True
            label.place_forget()
            break

      if not placed:
        if label in self.was_labels:
            label.place(x=1150, y=200 + self.was_labels.index(label)*10)
        elif label in self.were_labels:
             label.place(x=1150, y=350 + self.were_labels.index(label)*10)

      self.drag_data["word"] = None

    def start_drag(self, event):
     label = event.widget
     self.drag_data["word"] = label
     self.drag_data["offset_x"] = event.x_root - label.winfo_x()
     self.drag_data["offset_y"] = event.y_root - label.winfo_y()

     label.lift()

    def on_drag(self, event):
     label = self.drag_data["word"]
     x = event.x_root - self.drag_data["offset_x"]
     y = event.y_root - self.drag_data["offset_y"]
     label.place(x=x, y=y)

    def reset_game(self):
     for drop_label in self.drop_labels:
        drop_label.config(text="____", bg="lightblue")
     for i, label in enumerate(self.was_labels):
        label.place(x=1150, y=200 + i*10)

     for i, label in enumerate(self.were_labels):
        label.place(x=1150, y=350 + i*10)


    def exit_game(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = MatchGame(root)
    root.mainloop()