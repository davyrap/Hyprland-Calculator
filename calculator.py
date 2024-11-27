from customtkinter import CTk, CTkLabel, CTkFont, CTkFrame
from os import system

FONTSIZE = 50

OPERATIONS = ["plus", "minus", "asterisk", "slash", "parenleft", "parenright", "period", "comma"]
OPERATIONS_SYMBOLS = ["+", "-", "*", "/", "(", ")", ".", "."]

def Calculate(e):
    global equation
    global root
    global entryL
    global cursorIndex
    global entryR
    global label

    if e.keysym in ["c", "C"]:
        CopyToClipBoard(0)
        return

    if e.keysym not in ["BackSpace", "Left", "Right", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"] and e.keysym not in OPERATIONS:
        return

    if e.keysym == "Left":
        if cursorIndex < len(equation):
            cursorIndex += 1
    elif e.keysym == "Right":
        if cursorIndex > 0:
            cursorIndex -= 1
    
    elif e.keysym == "BackSpace":
        equation = equation[:len(equation) - cursorIndex - 1] + equation[len(equation) - cursorIndex:]

    elif e.keysym in OPERATIONS:
        equation = equation[:len(equation) - cursorIndex] + OPERATIONS_SYMBOLS[OPERATIONS.index(e.keysym)] + equation[len(equation) - cursorIndex:]

    else: 
        equation = equation[:len(equation) - cursorIndex] + e.keysym + equation[len(equation) - cursorIndex:]

    SetText(entryL, equation[:len(equation) - cursorIndex])
    SetText(entryR, equation[len(equation) - cursorIndex:])
    SetText(label, str(eval(equation)))

    rootWidth = max(300, entryL.winfo_reqwidth() + entryR.winfo_reqwidth() + label.winfo_reqwidth() + 120)
    SetRootPos(root, rootWidth)

def SetText(lbl:CTkLabel, t:str):
    lbl.configure(text=t)
    lbl.update_idletasks()

def SetRootPos(root:CTk, width:int):
    screenWidth = root.winfo_screenwidth() # width of the screen
    x = (screenWidth / 2) - (width / 2)
    Resize(root, width)

def CopyToClipBoard(e):
    root.clipboard_clear()  # Pulisce gli appunti
    root.clipboard_append(str(label.cget("text")))  # Aggiunge il testo della Label
    root.update()  # Aggiorna gli appunti
    system(f"notify-send '{label.cget("text")}' 'Testo copiato negli appunti\nNon chiudere la calcolatrice prima di incollare'")

def Resize(root, target_width, step=2, interval=2):
    current_width = root.winfo_width()
    if abs(current_width - target_width) <= step:
        # Fine animazione: imposta la dimensione finale
        root.geometry(f"{target_width}x80")
        return

    # Calcola la nuova larghezza in base alla direzione del cambiamento
    new_width = current_width + step if current_width < target_width else current_width - step
    screen_width = root.winfo_screenwidth()
    x = int((screen_width / 2) - (new_width / 2))

    # Applica la nuova dimensione
    root.geometry(f"{new_width}x80+{x}+800")

    # Pianifica il prossimo passo dell'animazione
    root.after(interval, Resize, root, target_width, step, interval)

# root
root = CTk()
root.title("DavyrapCalculator")
root.geometry("50x80")
root.after(50, lambda : SetRootPos(root, 300))

# variables
myFont = CTkFont("FiraCode", FONTSIZE)
cursorIndex = 0
equation = ""

# mainFrame
mainFrame = CTkFrame(root, height=100, fg_color="transparent")
mainFrame.grid_columnconfigure(5, weight=1)
mainFrame.grid_rowconfigure(1, weight=1)

# entry (input)
entryL = CTkLabel(mainFrame, text="", font=myFont, justify="right", fg_color="transparent", height=80, text_color="grey")
entryL.grid(row=1, column=1, padx=0, pady=0)

cursor = CTkLabel(mainFrame, text="|", font=("Calibri", FONTSIZE), justify="center", fg_color="transparent")
cursor.grid(row=1, column=2, padx=0, pady=25)

entryR = CTkLabel(mainFrame, text="", font=myFont, justify="left", fg_color="transparent", height=80, text_color="grey")
entryR.grid(row=1, column=3, padx=0, pady=0)

equals = CTkLabel(mainFrame, text="=", font=myFont, justify="center", fg_color="transparent", height=80, text_color="gray")
equals.grid(row=1, column=4, padx=0, pady=0)

# result (output)
label = CTkLabel(mainFrame, text="", font=myFont, justify="left", fg_color="transparent", height=80)
label.grid(row=1, column=5, padx=0, pady=0)

root.bind("<KeyPress>", Calculate)
root.bind("<Button-1>", CopyToClipBoard)

mainFrame.pack(padx=0, pady=0)
root.mainloop()
