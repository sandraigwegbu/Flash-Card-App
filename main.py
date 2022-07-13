from tkinter import *
from tkinter import messagebox
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
STUDY_LANGUAGE = "French"
WORD_LIST_CSV = "./data/french_words.csv"
current_card = {}
to_learn = {}

try:
	data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
	original_data = pandas.read_csv(WORD_LIST_CSV)
	to_learn = original_data.to_dict(orient="records")
else:
	to_learn = data.to_dict(orient="records")


# ----------------------------- RANDOM WORD GENERATOR ------------------------------ #
def next_card():
	global current_card, flip_timer
	window.after_cancel(flip_timer)

	current_card = random.choice(to_learn)
	canvas.itemconfig(card_title, text=STUDY_LANGUAGE, fill="black")
	canvas.itemconfig(card_word, text=current_card[STUDY_LANGUAGE], fill="black")
	canvas.itemconfig(card_background_image, image=card_front_img)
	flip_timer = window.after(3000, func=flip_card)


# --------------------------------- FLIP THE CARD ---------------------------------- #
def flip_card():
	global current_card
	canvas.itemconfig(card_background_image, image=card_back_img)
	canvas.itemconfig(card_word, text=current_card["English"], fill="white")
	canvas.itemconfig(card_title, text="English", fill="white")


# --------------------------------- SAVING PROGRESS -------------------------------- #
def update_card_deck():
	if len(to_learn) > 1:
		to_learn.remove(current_card)

		updated_data = pandas.DataFrame(to_learn)
		updated_data.to_csv("./data/words_to_learn.csv", index=False)

		next_card()
	else:
		messagebox.showinfo(title="Congratulations!", message="There are no more cards remaining in the deck.")


# ----------------------------------- RESET DECK ----------------------------------- #
def reset():
	global to_learn
	reset_data = pandas.read_csv(WORD_LIST_CSV)
	to_learn = reset_data.to_dict(orient="records")


# ------------------------------------ UI SETUP ------------------------------------ #
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_background_image = canvas.create_image(400, 263, image=card_front_img)
card_word = canvas.create_text(400, 263, text="", font=(FONT_NAME, 60, "bold"))
card_title = canvas.create_text(400, 150, text="", font=(FONT_NAME, 40, "italic"))
canvas.grid(column=0, row=0, columnspan=3)

# Buttons
wrong_png = PhotoImage(file="./images/wrong.png")
wrong_button = Button(command=next_card, image=wrong_png, highlightthickness=0)
wrong_button.grid(column=0, row=1)

right_png = PhotoImage(file="./images/right.png")
right_button = Button(command=update_card_deck, image=right_png, highlightthickness=0)
right_button.grid(column=2, row=1)

reset_button = Button(command=reset, text="Reset", font=(FONT_NAME, 14, "normal"), bg="white")
reset_button.grid(column=1, row=1)

messagebox.showinfo(title="How to use this flash card app.", message="Click the the green 'tick' button if you know "
                                                                     "the correct translation. Click the red 'cross' "
                                                                     "button if you don\'t know the word.\n\nFor every "
                                                                     "word that is guessed correctly, the card will "
                                                                     "be removed from the deck until there are no "
                                                                     "cards remaining.\n\nThe reset button puts all"
                                                                     "cards back in the deck.")

flip_timer = window.after(3000, func=flip_card)
next_card()

window.mainloop()
