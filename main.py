from tkinter import *
from PIL import Image, ImageTk
import pandas
from randomdict import RandomDict

BACKGROUND_COLOR = "#B1DDC6"
ran_item = ()
pre_item = ()

ran_val = pandas.read_csv(r"C:\Users\karth\OneDrive\Documents\NITC\RIG\Python\flash card\data\french_words.csv")
new_dict = {row.French: row.English for (index, row) in ran_val.iterrows()}


# ------------------------------PROGRAM-----------------------------------#
def change_val():
    global ran_item, flip_timer, pre_item
    window.after_cancel(flip_timer)
    pre_item = ran_item
    r = RandomDict(new_dict)
    ran_item = r.random_item()
    card_front.itemconfig(big_image, image=card_front_img)
    card_front.itemconfig(title_front, text="French", fill="black")
    card_front.itemconfig(word_front, text=ran_item[0], fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    global ran_item, flip_timer
    card_front.itemconfig(big_image, image=card_back_img)
    card_front.itemconfig(title_front, fill="white", text="English")
    card_front.itemconfig(word_front, fill="white", text=ran_item[1])


def learn_word():
    global pre_item, new_dict
    new_dict.pop(pre_item[0])
    print(pre_item)
    df = pandas.Series(new_dict).to_frame()
    df.to_csv("words_to_learn.csv")


# --------------------------------UI--------------------------------------#


window = Tk()
window.title("Flash Card")
window.config(bg=BACKGROUND_COLOR, highlightthickness=0)
flip_timer = window.after(3000, flip_card)

# back card
card_back_img1 = (Image.open(r"images\card_back.png"))
card_back_img2 = card_back_img1.resize((400, 264), Image.LANCZOS)
card_back_img = ImageTk.PhotoImage(card_back_img2)

# front card
card_front = Canvas(width=400, height=264, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img1 = (Image.open(r"images\card_front.png"))
card_front_img2 = card_front_img1.resize((400, 264), Image.LANCZOS)
card_front_img = ImageTk.PhotoImage(card_front_img2)
big_image = card_front.create_image(200, 128, image=card_front_img)

title_front = card_front.create_text(200, 75, text="Title", font=("Ariel", 20, "italic"))
word_front = card_front.create_text(200, 128, text="Word", font=("Ariel", 30, "bold"))

card_front.grid(row=0, column=0, columnspan=2, pady=25, padx=25)

wrong_img1 = Image.open(r"images\wrong.png")
wrong_img2 = wrong_img1.resize((75, 75), Image.LANCZOS)
wrong_img = ImageTk.PhotoImage(wrong_img2)
wrong_val = Button(image=wrong_img, command=change_val)
wrong_val.grid(row=1, column=0, pady=50)

right_img1 = Image.open(r"images\right.png")
right_img2 = right_img1.resize((75, 75), Image.LANCZOS)
right_img = ImageTk.PhotoImage(right_img2)
right_val = Button(image=right_img, command=lambda: [change_val(), learn_word()])
right_val.grid(row=1, column=1, pady=50)

change_val()

window.mainloop()
