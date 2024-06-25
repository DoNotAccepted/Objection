import tkinter as tk
import time
import random
from PIL import Image, ImageTk
import pygame
import threading
import keyboard

pygame.mixer.init()

def play_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def show_image_and_play_sound(window, label, image_file, sound_file, toggle_button_widget):
    toggle_button_widget.pack_forget()
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    img = Image.open(image_file)
    img_ratio = img.width / img.height
    new_height = window_height
    new_width = int(new_height * img_ratio)
    if new_width > window_width:
        new_width = window_width
        new_height = int(new_width / img_ratio)
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo
    x_center = (window_width - new_width) // 2
    y_center = (window_height - new_height) // 2
    label.place(x=x_center, y=y_center)
    play_sound(sound_file)
    for _ in range(5):
        x_move = random.randint(-20, 20)
        y_move = random.randint(-20, 20)
        label.place(x=x_center + x_move, y=y_center + y_move)
        window.update()
        time.sleep(0.1)
    label.place(x=x_center, y=y_center)
    window.update()
    time.sleep(0.5)
    label.config(image='')
    label.image = None
    toggle_button_widget.pack()

def on_key_press(window, label, button_state, toggle_button_widget, key):
    if button_state.get() == 'OFF':
        return
    window.attributes('-topmost', True)
    window.deiconify()
    window.focus_force()
    if key == 'a':
        window.state('zoomed')
        show_image_and_play_sound(window, label, 'Objection.png', 'Objection.mp3', toggle_button_widget)
        time.sleep(1)
        window.state('normal')
    elif key == 's':
        window.state('zoomed')
        show_image_and_play_sound(window, label, 'Holdit.png', 'Holdit.mp3', toggle_button_widget)
        time.sleep(1)
        window.state('normal')
    elif key == 'd':
        window.state('zoomed')
        show_image_and_play_sound(window, label, 'Takethat.png', 'Takethat.mp3', toggle_button_widget)
        time.sleep(1)
        window.state('normal')
    window.after(500, lambda: window.attributes('-topmost', False))
    window.state('iconic')

def toggle_button(button, button_state):
    if button_state.get() == 'ON':
        button_state.set('OFF')
        button.config(text='休庭')
    else:
        button_state.set('ON')
        button.config(text='开庭')

def main():
    window = tk.Tk()
    window.geometry('300x100')
    window.title('異議あり！')
    label = tk.Label(window)
    label.pack(fill=tk.BOTH, expand=True)
    button_state = tk.StringVar(value='ON')
    toggle_button_widget = tk.Button(window, text='开庭', command=lambda: toggle_button(toggle_button_widget, button_state))
    toggle_button_widget.pack()
    def key_listener():
        while True:
            if keyboard.is_pressed('a'):
                on_key_press(window, label, button_state, toggle_button_widget, 'a')
            elif keyboard.is_pressed('s'):
                on_key_press(window, label, button_state, toggle_button_widget, 's')
            elif keyboard.is_pressed('d'):
                on_key_press(window, label, button_state, toggle_button_widget, 'd')

    listener_thread = threading.Thread(target=key_listener, daemon=True)
    listener_thread.start()
    def on_minimize(event):
        window.attributes('-topmost', False)
    window.bind("<Unmap>", on_minimize)
    window.mainloop()

if __name__ == '__main__':
    main()
