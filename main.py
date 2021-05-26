from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

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
    if image_path.get() == "" or watermark_path.get() == "":
        messagebox.showinfo(title="No file", message="There is an image file missing. Please add both images.")
        return
    image = Image.open(image_path.get())
    watermark = Image.open(watermark_path.get())
    watermark.save('watermark.png')
    if watermark_size.get() == "":
        width_scale_entry.config(state=NORMAL)
        width_scale_entry.insert(END, watermark.size[0])
    watermark_copy = watermark.copy()
    image_copy = image.copy()

    try:
        new_opacity = int(opacity.get())
        watermark_copy.putalpha(new_opacity)
        watermark.paste(watermark_copy, watermark)
        watermark.save('watermark.png')
        watermark_copy = watermark.copy()
    except ValueError:
        messagebox.showinfo(title="Invalid Input", message="Pick a number between 0 and 255.")

    try:
        new_width = int(width_scale_entry.get())
        new_height_factor = new_width / watermark_copy.size[0]
        new_height = int(round(watermark_copy.size[1] * new_height_factor))
        watermark_copy = watermark_copy.resize((new_width, new_height))
        watermark_copy.save('watermark.png')
    except ValueError:
        messagebox.showinfo(title="Invalid Input", message="Please insert a whole number into the form.")

    if alignment.get() == 1:
        position = ((int(round(image_copy.width - (int(round(watermark_copy.width)))))),
                    (int(round(image_copy.height - (int(round(watermark_copy.height)))))))
    else:
        position = (((int(round(image_copy.width / 2))) - (int(round(watermark_copy.width / 2)))),
                    ((int(round(image_copy.height / 2))) - (int(round(watermark_copy.height / 2)))))

    image_copy.paste(watermark_copy, position, watermark_copy)
    image_copy.save('output_img.jpg')
    save_button.config(state=NORMAL)
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


def save_image():
    try:
        output_image = Image.open('output_img.jpg')
    except FileNotFoundError:
        merge_images()
        output_image = Image.open('output_img.jpg')

    try:
        output_image.save(filedialog.asksaveasfile(
            mode='wb',
            filetypes=[('Image Files', '.jpeg .jpg .png .ppm .gif .tiff .bpm')],
            defaultextension=".jpg")
        )
        os.remove('output_img.jpg')
        os.remove('preview.jpg')
        os.remove('watermark.png')
    except ValueError:
        return


def clear():
    if toggle.get():
        toggle_options()
    image_path.set("")
    watermark_path.set("")
    alignment.set(1)
    watermark_size.set("")
    opacity.set(255)
    preview_canvas.delete("all")
    os.remove('output_img.jpg')
    os.remove('preview.jpg')
    os.remove('watermark.png')


# -------- UI Setup -------- #

window = Tk()
window.title("Watermark this!")
window.config(padx=70, pady=70, bg=WHITE)


# -------- Logo -------- #

logo_canvas = Canvas(width=650, height=220, highlightthickness=0, bg=WHITE)
logo_img = PhotoImage(file="watermark-this-final.png")
logo_canvas.create_image(325, 110, image=logo_img)
logo_canvas.grid(column=2, row=0)


# -------- Preview -------- #

preview_canvas = Canvas(width=600, height=400, bg=WHITE)
preview_canvas.grid(column=2, row=8)

save_button = Button(text="Save Image",
                     font=("Lucinda Grande", 14, "normal"),
                     command=lambda: save_image(),
                     state=DISABLED,
                     bg=WHITE)
save_button.grid(column=2, row=9)

clear_button = Button(text="Clear",
                      font=("Lucinda Grande", 12, "normal"),
                      command=lambda: clear(),
                      state=NORMAL,
                      bg=WHITE)
clear_button.grid(column=2, row=10)


# -------- Upload -------- #

image_path = StringVar()
watermark_path = StringVar()

filename1_entry = Entry(state=DISABLED, textvariable=image_path)
filename1_entry.grid(column=1, row=1, columnspan=2, sticky="EW")

upload_img_button = Button(text="Upload Image",
                           font=("Lucinda Grande", 12, "normal"),
                           command=lambda: browse_func(filename1_entry),
                           bg=WHITE)
upload_img_button.grid(column=3, row=1, sticky="EW")

filename2_entry = Entry(state=DISABLED, textvariable=watermark_path)
filename2_entry.grid(column=1, row=2, columnspan=2, sticky="EW")

upload_watermark_button = Button(text="Upload Watermark",
                                 font=("Lucinda Grande", 12, "normal"),
                                 command=lambda: browse_func(filename2_entry),
                                 bg=WHITE)
upload_watermark_button.grid(column=3, row=2, sticky="EW")

merge_button = Button(text="Watermark it!",
                      font=("Lucinda Grande", 14, "normal"),
                      command=lambda: merge_images(),
                      bg=WHITE)
merge_button.grid(column=2, row=7, sticky="EW")


# -------- Options Toggle -------- #

toggle = BooleanVar()
toggle.set(False)

options_frame = Frame(window, bg=WHITE)
options_frame.grid(column=2, row=4)

options_button = Button(text="+",
                        font=("Lucinda Grande", 12, "normal"), command=lambda: toggle_options(), bg=WHITE)
options_button.grid(column=0, row=3)

options_label = Label(text="Options", bg=WHITE)
options_label.grid(column=1, row=3)

if not toggle.get():
    options_frame.grid_remove()

# -------- Options Menu -------- #

align_labelframe = LabelFrame(options_frame, text="Watermark Alignment",
                              font=("Lucinda Grande", 12, "normal"), bg=WHITE)
align_labelframe.grid(column=0, row=0, sticky="EW")

alignment = IntVar()
alignment.set(1)
bottom_right_button = Radiobutton(align_labelframe, text="Bottom Right", variable=alignment, value=1, bg=WHITE)
bottom_right_button.grid(sticky="W")
center_button = Radiobutton(align_labelframe, text="Center", variable=alignment, value=2, bg=WHITE)
center_button.grid(sticky="W")

scale_labelframe = LabelFrame(options_frame, text="Resize Watermark",
                              font=("Lucinda Grande", 12, "normal"), bg=WHITE)
scale_labelframe.grid(column=1, row=0, sticky="EW")

watermark_size = StringVar()
width_scale_entry = Entry(scale_labelframe, bg=WHITE, textvariable=watermark_size, state=DISABLED)
width_scale_entry.grid(sticky="EW")

opacity_labelframe = LabelFrame(options_frame, text="Watermark Opacity",
                                font=("Lucinda Grande", 12, "normal"), bg=WHITE)
opacity_labelframe.grid(column=2, row=0, sticky="EW")

opacity = StringVar(window)
opacity.set("255")
opacity_spinbox = Spinbox(opacity_labelframe, from_=0, to=255, textvariable=opacity, bg=WHITE)
opacity_spinbox.grid(sticky="EW")


window.mainloop()
