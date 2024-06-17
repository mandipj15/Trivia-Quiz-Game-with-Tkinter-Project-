import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import random
from question_bank import question_bank

# Shuffle and select 5 questions from the question_bank
random.shuffle(question_bank)
selected_question = question_bank[:5]

# Initialize the current question index and selected choice index
current_question = 0
selected_choice_index = 0
answer_selected = False

# Function to display the current question
def show_question():
    global current_question, selected_choice_index, answer_selected
    # Get the current question from the question_bank
    question = selected_question[current_question]
    qus_label.config(text=question["question"])

    # Display the choice buttons
    choices = question["choices"]
    for i in range(len(choice_btn)):
        choice_btn[i].config(text=choices[i], state="normal", style="select.TButton")  # Reset button

    # Clear the feedback label and disable the next button
    feedback_label.config(text="")
    next_btn.config(state="disabled", style="elder.TButton")

    # Reset the selected choice index and answer selected flag
    selected_choice_index = 0
    answer_selected = False
    highlight_choice()

# Function to highlight the currently selected choice
def highlight_choice():
    for i, button in enumerate(choice_btn):
        if i == selected_choice_index:
            button.focus_set()
            button.config(style="highlight.TButton")
        else:
            button.config(style="select.TButton")

# Function to check the selected answer and provide feedback
def check_answer(choice):
    global answer_selected
    if answer_selected:
        return

    answer_selected = True

    # Get the current question from the question_bank
    question = selected_question[current_question]

    # Get the selected choice text from the corresponding button
    selected_choice = choice_btn[choice].cget("text")

    # Check if the selected choice matches the correct answer
    if selected_choice == question["correct_choice"]:
        # Update the score and display it
        global score
        score += 1
        score_label.config(text="Score: {}/{}".format(score, len(selected_question)))
        feedback_label.config(text="Correct!", foreground="green", bg="lightyellow")
        choice_btn[choice].config(style="Correct.TButton")
    else:
        feedback_label.config(text="Correct! The answer is {}".format(question["correct_choice"]), foreground="red", bg="lightyellow")
        choice_btn[choice].config(style="Incorrect.TButton")

    # Disable all choice buttons and enable the next button
    for button in choice_btn:
        button.config(state="disabled")
    next_btn.config(state="normal", style="elder.TButton")

# Function to move to the next question
def next_question(event=None):
    global current_question, answer_selected
    current_question += 1

    if current_question < len(selected_question):
        show_question()
    else:
        messagebox.showinfo("Quiz Completed", "Quiz Completed! Final score: {}/{}".format(score, len(selected_question)))
        next_btn.pack_forget()
        play_again_btn.pack(pady=10)

# Function to restart the game
def restart_game( event=None):
    global current_question, score, selected_question, answer_selected
    random.shuffle(question_bank)
    selected_question = question_bank[:5]
    current_question = 0
    score = 0
    score_label.config(text="Score: 0/{}".format(len(selected_question)))
    play_again_btn.pack_forget()
    next_btn.pack(pady=10)
    answer_selected = False
    show_question()

# Function to quit the game
def quit_game(event=None):
    root.destroy()

# Function to start the quiz
def start_quiz(event=None):
    start_frame.pack_forget()
    top_frame.pack(side="top", fill="x")
    quiz_frame.pack()

# Function to handle key presses
def handle_key_press(event):
    global selected_choice_index
    if not answer_selected:
        if event.keysym == "Up":
            selected_choice_index = (selected_choice_index - 1) % len(choice_btn)
            highlight_choice()
        elif event.keysym == "Down":
            selected_choice_index = (selected_choice_index + 1) % len(choice_btn)
            highlight_choice()
    if event.keysym == "Return":
        check_answer(selected_choice_index)

# Create the main window
root = tk.Tk()
root.title("Trivia Quiz Game")
root.geometry("900x570")

# Create a ttk Style object
style = ttk.Style()
style.theme_use("clam")

# Customize buttons
style.configure("elder.TButton", foreground="black", background="#F1B660", font=("comic sans ms", 12, "bold", "italic"), bordercolor="#1B1A27", borderwidth=2)
style.map("elder.TButton", background=[('active', '#00C3ED')])

style.configure("playAgain.TButton", foreground="darkorange", background="#E5E725", font=("comic sans ms", 12, "bold", "italic"), bordercolor="black", borderwidth=2)
style.map("PlayAgain.TButton", background=[('active', '#006C7E')])

style.configure("quit.TButton", foreground="white", background="#00909B", font=("comic sans ms", 10, "bold", "italic"), bordercolor="black", borderwidth=1, padding=[3, 3, 3, 3])
style.map("quit.TButton", background=[('active', 'red')])

style.configure("select.TButton", background="whitesmoke", foreground="Black", font=("comic sans ms", 11, "bold"), bordercolor="black", borderwidth=1)
style.map("select.TButton", background=[('active', "cornsilk")])

style.configure("highlight.TButton", background="lightblue", foreground="Black", font=("comic sans ms", 11, "bold"), bordercolor="black", borderwidth=1)
style.map("highlight.TButton", background=[('active', "cornsilk")])

style.configure("Correct.TButton", background="limegreen", foreground="white", font=("comic sans ms", 11, "bold"))
style.map("Correct.TButton", background=[('active', 'green')])

style.configure("Incorrect.TButton", background="red", foreground="white", font=("comic sans ms", 11, "bold"))
style.map("Incorrect.TButton", background=[('active', 'red')])

# Load the background image
start_bg_path = "quiz background.png"
start_bg_image = Image.open(start_bg_path)
background_image = ImageTk.PhotoImage(start_bg_image)

# Create start frame
start_frame = tk.Frame(root, bg="snow")
start_frame.pack(fill=tk.BOTH, expand=True)
start_frame.place(relwidth=1, relheight=1)

# Create background label to display the image
background_label = tk.Label(start_frame, image=background_image)
background_label.pack(padx=100, pady=70, fill=tk.BOTH, expand=True)
background_label.place(relwidth=1, relheight=1)

# Create other widgets in the start frame
start_label = ttk.Label(start_frame, background="khaki", text="Welcome to the Trivia Quiz Game!",
                        font=("elephant", 18), anchor="center", padding=10)
start_label.pack(pady=50)

# Load image
start_img = Image.open("play button.png")
start_img = start_img.resize((150, 60))
start_photo = ImageTk.PhotoImage(start_img)

start_button = tk.Button(start_frame, image=start_photo, command=start_quiz, cursor="hand2",
                         background="#FFFFFF", borderwidth=0, activeforeground="#FFFFFF", activebackground="#FFFFFF")
start_button.pack(pady=20)

# Load background image
quiz_bg_path = "db34d40b271fb59477621550bf73ea0b.jpg"
quiz_bg_img = Image.open(quiz_bg_path)
quiz_frame_bg = ImageTk.PhotoImage(quiz_bg_img)

# Create quiz frame
quiz_frame = tk.Frame(root, highlightbackground="black", highlightthickness=2, width=600)
quiz_frame.pack(fill=tk.BOTH, expand=True)

quiz_background_label = tk.Label(quiz_frame, image=quiz_frame_bg)
quiz_background_label.place(relheight=1, relwidth=1)

# Create the question label
qus_label = ttk.Label(quiz_frame, anchor="center", wraplength=500, padding=10,
                      font=('comic sans MS', 15, 'bold'), background="light sky blue")
qus_label.pack(pady=10)

# Create choice buttons
choice_btn = []
for i in range(4):
    button = ttk.Button(quiz_frame, command=lambda i=i: check_answer(i), width=20, padding=10, cursor="hand2", style="select.TButton")
    button.pack(fill="x", padx=10, pady=5)
    choice_btn.append(button)

# Create feedback label
feedback_label = tk.Label(quiz_frame, anchor="center", highlightbackground="black",
                          highlightthickness=1, background="mintcream", font=("comic sans ms", 9))
feedback_label.pack(pady=10)

# Initialize the score
score = 0

# Create the score label
score_label = tk.Label(quiz_frame, text="Score: 0/{}".format(len(selected_question)), font=("comic sans ms", 10, "bold"), anchor="center",
                       highlightbackground="darkslategray", highlightthickness=1, background="cornsilk")
score_label

score_label.pack(pady=10)

# Create next button
next_btn = ttk.Button(quiz_frame, text="Next", command=next_question, state="disabled", width=10, padding=8, cursor="hand2", style="elder.TButton")
next_btn.pack(pady=10)

# Create play again button, initially hidden
play_again_btn = ttk.Button(quiz_frame, text="Play Again", command=restart_game, padding=10, cursor="hand2", style="playAgain.TButton")

# Create a top frame for the quit button
top_frame = tk.Frame(root)

# Create quit button and pack it to the left corner of the top frame
quit_btn = ttk.Button(top_frame, text="Quit", command=quit_game, cursor="hand2", style="quit.TButton")
quit_btn.pack(side="left", padx=7, pady=6)

# Press Escape button on keyboard to quit the game
root.bind("<Escape>", quit_game)

# Press Enter key on keyboard to go on next question the game
root.bind("<Return>", handle_key_press)

# Press spacebar on keyboard to move to the next question
root.bind("<space>", next_question)

# Bind up and down arrow keys for navigation
root.bind("<Up>", handle_key_press)
root.bind("<Down>", handle_key_press)

# Press <p> on keyboard to move to the play again
root.bind("<p>", restart_game)

# press enter key on key board to go on next question the game 
root.bind("<w>", start_quiz)


# Pack the quiz frame into the root window, but it will be shown after starting the quiz
quiz_frame.pack_forget()

# Show the first question
show_question()

# Start the main event loop
root.mainloop()
