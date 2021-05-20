from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

WHITE = "#ffffff"


# -------- Functions -------- #

def browse_func(entry):
    entry.config(state=NORMAL)
    print(entry.get())
    if entry.get() != "":
        entry.delete(0, END)
    filename = filedialog.askopenfilename(filetypes=[('Image Files', '.jpeg .jpg .png .ppm .gif .tiff .bpm')])
    entry.insert(END, filename)
    entry.config(state=DISABLED)


def merge_images():
    image_path = filename1_entry.get()
    watermark_path = filename2_entry.get()
    if image_path == "" or watermark_path == "":
        messagebox.showinfo(title="No file", message="There is an image file missing. Please add both images.")
        return
    image = Image.open(image_path)
    watermark = Image.open(watermark_path)
    image_copy = image.copy()
    if v.get() == 1:
        position = ((int(round(image_copy.width - (int(round(watermark.width)))))),
                    (int(round(image_copy.height - (int(round(watermark.height)))))))
    else:
        position = (((int(round(image_copy.width / 2))) - (int(round(watermark.width / 2)))),
                    ((int(round(image_copy.height / 2))) - (int(round(watermark.height / 2)))))
    image_copy.paste(watermark, position, watermark)
    image_copy.save('output_img.jpg')
    image_copy.thumbnail((600, 400))
    image_copy.save('preview.jpg')
    thumbnail = ImageTk.PhotoImage(file='preview.jpg')
    window.thumbnail = thumbnail
    preview_canvas.config(width=thumbnail.width(), height=thumbnail.height())
    preview_canvas.create_image((thumbnail.width() / 2), (thumbnail.height() / 2), image=thumbnail)
    preview_canvas.grid(column=2, row=8)


def toggle_options():
    if toggle.get():
        options_button.config(text="+")
        options_frame.grid_remove()
        toggle.set(False)
    else:
        options_button.config(text="-")
        options_frame.grid()
        toggle.set(True)


def resize_watermark():
    pass


# -------- UI Setup -------- #

window = Tk()
window.title("Watermark this!")
window.config(padx=100, pady=100, bg=WHITE)


# -------- Logo -------- #

logo_canvas = Canvas(width=650, height=220, highlightthickness=0, bg=WHITE)
logo_img = PhotoImage(file="watermark-this-final.png")
logo_canvas.create_image(325, 110, image=logo_img)
logo_canvas.grid(column=2, row=0)


# -------- Preview -------- #

preview_canvas = Canvas(width=600, height=400, bg=WHITE)
preview_canvas.grid(column=2, row=8)


# -------- Upload -------- #

filename1_entry = Entry(state=DISABLED)
filename1_entry.grid(column=1, row=1, columnspan=2, sticky="EW")

upload_img_button = Button(text="Upload Image",
                           font=("Lucinda Grande", 12, "normal"), command=lambda: browse_func(filename1_entry),
                           bg=WHITE)
upload_img_button.grid(column=3, row=1, sticky="EW")

filename2_entry = Entry(state=DISABLED)
filename2_entry.grid(column=1, row=2, columnspan=2, sticky="EW")

upload_watermark_button = Button(text="Upload Watermark",
                                 font=("Lucinda Grande", 12, "normal"), command=lambda: browse_func(filename2_entry),
                                 bg=WHITE)
upload_watermark_button.grid(column=3, row=2, sticky="EW")

merge_button = Button(text="Watermark it!",
                      font=("Lucinda Grande", 14, "normal"), command=lambda: merge_images(), bg=WHITE)
merge_button.grid(column=2, row=7, sticky="EW")


# -------- Options -------- #

toggle = BooleanVar()
toggle.set(False)

options_frame = Frame(window)
options_frame.grid(column=2, row=4)

options_button = Button(text="+",
                        font=("Lucinda Grande", 12, "normal"), command=lambda: toggle_options(), bg=WHITE)
options_button.grid(column=0, row=3)

if not toggle.get():
    options_frame.grid_remove()

# -------- Checkbox -------- #

align_labelframe = LabelFrame(options_frame, text="Watermark Alignment",
                              font=("Lucinda Grande", 12, "normal"), bg=WHITE)
align_labelframe.grid(column=0, row=0, sticky="W")

v = IntVar()
v.set(1)
bottom_right_button = Radiobutton(align_labelframe, text="Bottom Right", variable=v, value=1, bg=WHITE)
bottom_right_button.grid(sticky="W")
center_button = Radiobutton(align_labelframe, text="Center", variable=v, value=2, bg=WHITE)
center_button.grid(sticky="W")

scale_labelframe = LabelFrame(options_frame, text="Resize Watermark",
                              font=("Lucinda Grande", 12, "normal"), bg=WHITE)
scale_labelframe.grid(column=1, row=0, sticky="E")

width_scale_entry = Entry(scale_labelframe, bg=WHITE)
width_scale_entry.grid(sticky="E")

height_scale_entry = Entry(scale_labelframe, bg=WHITE)
height_scale_entry.grid(sticky="E")

# -------- Entries -------- #


# -------- Labels -------- #

options_label = Label(text="Options", bg=WHITE)
options_label.grid(column=1, row=3)

window.mainloop()
