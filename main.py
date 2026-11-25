
import tkinter as tk
import math
import ast
import operator


# renkler ve ayarlar

themes = {
    "light": {
        "bg": "#F2F2F2",
        "white": "#FFFFFF",
        "orange": "#F4AD78",
        "orange_hover": "#E99A60",
        "gray": "#E8E8E8",
        "dark": "#333333",
        "text_gray": "#888888"
    },

    "dark": {
        "bg": "#242424",
        "white": "#303030",
        "orange": "#F4AD78",
        "orange_hover": "#E99A60",
        "gray": "#424242",
        "dark": "#F2F2F2",
        "text_gray": "#BBBBBB"
    }
}

current_theme = "light"
large_ui = False
show_history = True
advanced_mode = False

history_items = []

number_buttons = []
operator_buttons = []


# ana pencere

root = tk.Tk()

root.title("Modern Hesap Makinesi")
root.state("zoomed")
root.minsize(800, 600)

expression = tk.StringVar(value="0")


# ana yerleşim

main_frame = tk.Frame(root)

main_frame.pack(
    fill="both",
    expand=True,
    padx=40,
    pady=25
)

main_frame.columnconfigure(0, weight=3)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(1, weight=1)


# üst baslık

header = tk.Frame(main_frame)

header.grid(
    row=0,
    column=0,
    columnspan=2,
    sticky="ew",
    pady=(0, 20)
)

header.columnconfigure(0, weight=1)

title = tk.Label(
    header,
    text="Hesap Makinesi",
    font=("Arial", 25, "bold")
)

title.grid(row=0, column=0, sticky="w")


# hesaplama paneli

calculator = tk.Frame(main_frame)

calculator.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=(0, 20)
)

calculator.rowconfigure(1, weight=1)
calculator.columnconfigure(0, weight=1)


# ekran

display = tk.Entry(
    calculator,
    textvariable=expression,
    font=("Arial", 35),
    bd=0,
    justify="right",
    state="readonly"
)

display.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=25,
    pady=30,
    ipady=20
)


# butonların alanı

button_frame = tk.Frame(calculator)

button_frame.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=20,
    pady=10
)

button_frame.columnconfigure(
    (0, 1, 2, 3),
    weight=1
)


# normal hesap makinesi butonları

basic_buttons = [
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["(", "0", ",", "="]
]


# bilimsel hesap makinesi butonları

scientific_buttons = [
    ["sin", "cos", "tan", "√"],
    ["log", "ln", "π", "x²"]
]


# işlem geçmişi

history_frame = tk.Frame(
    main_frame,
    width=300
)

history_frame.grid(
    row=1,
    column=1,
    sticky="nsew"
)

history_frame.grid_propagate(False)

history_title = tk.Label(
    history_frame,
    text="İşlem Geçmişi",
    font=("Arial", 17, "bold")
)

history_title.pack(
    anchor="w",
    padx=20,
    pady=20
)

history_list = tk.Listbox(
    history_frame,
    font=("Arial", 12),
    bd=0,
    highlightthickness=0,
    selectbackground="#F4AD78"
)

history_list.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

history_clear_button = tk.Button(
    history_frame,
    text="Geçmişi Temizle",
    font=("Arial", 11),
    bd=0,
    cursor="hand2"
)

history_clear_button.pack(
    fill="x",
    padx=15,
    pady=15,
    ipady=8
)


# hesaplama ekranı fonksiyonları
def press(value):

    current = expression.get()

    if current in ["0", "Hata"]:
        if value in "+-×÷":
            if current == "Hata":
                expression.set("0")
                current = "0"
        else:
            current = ""

    expression.set(current + value)


def clear():

    expression.set("0")


def backspace():

    current = expression.get()

    if len(current) <= 1:
        expression.set("0")
    else:
        expression.set(current[:-1])


# guvenli matematilk motoru

binary_operations = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow
}

unary_operations = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg
}


def evaluate(node):

    if isinstance(node, ast.Expression):
        return evaluate(node.body)

    elif isinstance(node, ast.Constant):

        if type(node.value) not in (int, float):
            raise ValueError("Geçersiz sayı")

        return node.value

    elif isinstance(node, ast.BinOp):

        operation = binary_operations.get(type(node.op))

        if operation is None:
            raise ValueError("Geçersiz işlem")

        left = evaluate(node.left)
        right = evaluate(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("Üs çok büyük")

        result = operation(left, right)

        if isinstance(result, complex):
            raise ValueError("Geçersiz sonuç")

        if not math.isfinite(result):
            raise ValueError("Geçersiz sonuç")

        return result

    elif isinstance(node, ast.UnaryOp):

        operation = unary_operations.get(type(node.op))

        if operation is None:
            raise ValueError("Geçersiz işlem")

        return operation(evaluate(node.operand))

    elif isinstance(node, ast.Name):

        constants = {
            "pi": math.pi
        }

        if node.id not in constants:
            raise ValueError("Bilinmeyen ifade")

        return constants[node.id]

    elif isinstance(node, ast.Call):

        if not isinstance(node.func, ast.Name):
            raise ValueError("Geçersiz fonksiyon")

        functions = {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log
        }

        function_name = node.func.id

        if function_name not in functions:
            raise ValueError("Bilinmeyen fonksiyon")

        if len(node.args) != 1 or node.keywords:
            raise ValueError("Geçersiz fonksiyon kullanımı")

        value = evaluate(node.args[0])

        result = functions[function_name](value)

        if not math.isfinite(result):
            raise ValueError("Geçersiz sonuç")

        return result

    raise ValueError("Geçersiz matematik ifadesi")


def calculate():

    current = expression.get()

    try:

        safe_expression = current.replace("×", "*")
        safe_expression = safe_expression.replace("÷", "/")
        safe_expression = safe_expression.replace(",", ".")

        tree = ast.parse(
            safe_expression,
            mode="eval"
        )

        result = evaluate(tree)

        if isinstance(result, float):
            result = round(result, 10)

        if not math.isfinite(result):
            raise ValueError

        old_expression = current

        if isinstance(result, float):
            result_text = f"{result:.10f}".rstrip("0").rstrip(".")
        else:
            result_text = str(result)

        result_text = result_text.replace(".", ",")

        expression.set(result_text)

        add_history(
            f"{old_expression} = {result_text}"
        )

    except (
        ValueError,
        SyntaxError,
        ZeroDivisionError,
        TypeError,
        OverflowError
    ):

        expression.set("Hata")


# işlem geçmişi

def add_history(item):

    history_items.insert(0, item)

    history_list.insert(0, item)


def clear_history():

    history_items.clear()

    history_list.delete(0, tk.END)


def select_history(event):

    selection = history_list.curselection()

    if selection:

        item = history_items[selection[0]]

        if " = " in item:
            old_expression = item.rsplit(" = ", 1)[0]
            expression.set(old_expression)


history_list.bind(
    "<<ListboxSelect>>",
    select_history
)


# buton işlemleri

def button_action(value):

    if value == "C":
        clear()

    elif value == "⌫":
        backspace()

    elif value == "=":
        calculate()

    elif value == "sin":
        press("sin(")

    elif value == "cos":
        press("cos(")

    elif value == "tan":
        press("tan(")

    elif value == "√":
        press("sqrt(")

    elif value == "log":
        press("log(")

    elif value == "ln":
        press("ln(")

    elif value == "π":
        press("pi")

    elif value == "x²":
        press("**2")

    else:
        press(value)


# buton oluşturma

def create_button(text, row, col):

    button = tk.Button(
        button_frame,
        text=text,
        font=("Arial", 20, "bold"),
        bd=0,
        relief="flat",
        cursor="hand2",
        command=lambda: button_action(text)
    )

    button.grid(
        row=row,
        column=col,
        sticky="nsew",
        padx=6,
        pady=6
    )

    if text in [
        "÷", "×", "-", "+", "=",
        "sin", "cos", "tan", "√",
        "log", "ln", "π", "x²"
    ]:

        operator_buttons.append(button)

    else:

        number_buttons.append(button)


def render_buttons():

    for widget in button_frame.winfo_children():
        widget.destroy()

    number_buttons.clear()
    operator_buttons.clear()

    current_buttons = basic_buttons.copy()

    if advanced_mode:
        current_buttons += scientific_buttons

    for i in range(9):
        button_frame.rowconfigure(i, weight=0)

    for i in range(len(current_buttons)):
        button_frame.rowconfigure(i, weight=1)

    for row_index, row in enumerate(current_buttons):

        for col_index, value in enumerate(row):

            create_button(
                value,
                row_index,
                col_index
            )

    apply_theme(current_theme)


# tema degiştirme

def apply_theme(theme_name):

    global current_theme

    current_theme = theme_name

    c = themes[current_theme]

    root.configure(bg=c["bg"])
    main_frame.configure(bg=c["bg"])
    header.configure(bg=c["bg"])

    title.configure(
        bg=c["bg"],
        fg=c["dark"]
    )

    settings_button.configure(
        bg=c["orange"],
        fg="#FFFFFF",
        activebackground=c["orange_hover"],
        activeforeground="#FFFFFF"
    )

    calculator.configure(bg=c["white"])
    button_frame.configure(bg=c["white"])

    display.configure(
        bg=c["white"],
        fg=c["dark"],
        readonlybackground=c["white"]
    )

    history_frame.configure(bg=c["white"])

    history_title.configure(
        bg=c["white"],
        fg=c["dark"]
    )

    history_list.configure(
        bg=c["white"],
        fg=c["text_gray"],
        selectbackground=c["orange"],
        selectforeground="#FFFFFF"
    )

    history_clear_button.configure(
        bg=c["orange"],
        fg="#FFFFFF",
        activebackground=c["orange_hover"],
        activeforeground="#FFFFFF"
    )

    for button in number_buttons:

        button.configure(
            bg=c["gray"],
            fg=c["dark"],
            activebackground=c["orange"],
            activeforeground="#FFFFFF"
        )

    for button in operator_buttons:

        button.configure(
            bg=c["orange"],
            fg="#FFFFFF",
            activebackground=c["orange_hover"],
            activeforeground="#FFFFFF"
        )

    update_fonts()


# yazı boyutları

def update_fonts():

    if large_ui:

        title.configure(font=("Arial", 30, "bold"))
        display.configure(font=("Arial", 45))

        history_title.configure(
            font=("Arial", 21, "bold")
        )

        history_list.configure(font=("Arial", 16))

        history_clear_button.configure(
            font=("Arial", 15)
        )

        settings_button.configure(
            font=("Arial", 15)
        )

        for button in number_buttons + operator_buttons:
            button.configure(font=("Arial", 26, "bold"))

    else:

        title.configure(font=("Arial", 25, "bold"))
        display.configure(font=("Arial", 35))

        history_title.configure(
            font=("Arial", 17, "bold")
        )

        history_list.configure(font=("Arial", 12))

        history_clear_button.configure(
            font=("Arial", 11)
        )

        settings_button.configure(
            font=("Arial", 12)
        )

        for button in number_buttons + operator_buttons:
            button.configure(font=("Arial", 20, "bold"))


#arayuz iyileştirmesi yani yazı buyuklugu

def toggle_large_ui():

    global large_ui

    large_ui = large_var.get()

    update_fonts()


#bilimsel işlemlr

def toggle_advanced():

    global advanced_mode

    advanced_mode = advanced_var.get()

    render_buttons()


#işlem geçmişi acıp kapama

def toggle_history():

    global show_history

    show_history = history_var.get()

    if show_history:

        history_frame.grid()

        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)

        calculator.grid_configure(
            padx=(0, 20)
        )

    else:

        history_frame.grid_remove()

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=0)

        calculator.grid_configure(
            padx=(0, 0)
        )


# ayarlar penceresi

def open_settings():

    global large_var
    global history_var
    global advanced_var

    settings = tk.Toplevel(root)

    settings.title("Ayarlar")
    settings.geometry("430x470")
    settings.resizable(False, False)
    settings.transient(root)

    c = themes[current_theme]

    settings.configure(bg=c["bg"])

    heading = tk.Label(
        settings,
        text="Ayarlar",
        font=("Arial", 23, "bold"),
        bg=c["bg"],
        fg=c["dark"]
    )

    heading.pack(pady=25)

    # temanın baslığı

    theme_label = tk.Label(
        settings,
        text="Görünüm",
        font=("Arial", 14, "bold"),
        bg=c["bg"],
        fg=c["dark"]
    )

    theme_label.pack(pady=(5, 12))

    theme_frame = tk.Frame(
        settings,
        bg=c["bg"]
    )

    theme_frame.pack()

    # aydınlık tema

    light_button = tk.Button(
        theme_frame,
        text="Aydınlık Tema",
        font=("Arial", 11),
        bg=c["orange"],
        fg="white",
        activebackground=c["orange_hover"],
        bd=0,
        padx=15,
        pady=10,
        command=lambda: apply_theme("light")
    )

    light_button.pack(side="left", padx=5)

    # koyu tema

    dark_button = tk.Button(
        theme_frame,
        text="Koyu Tema",
        font=("Arial", 11),
        bg=c["orange"],
        fg="white",
        activebackground=c["orange_hover"],
        bd=0,
        padx=15,
        pady=10,
        command=lambda: apply_theme("dark")
    )

    dark_button.pack(side="left", padx=5)

    # ayarın degişkeni

    large_var = tk.BooleanVar(value=large_ui)
    history_var = tk.BooleanVar(value=show_history)
    advanced_var = tk.BooleanVar(value=advanced_mode)

    # daha buyuk yazı secenegi

    large_check = tk.Checkbutton(
        settings,
        text="Arayüz iyileştirmesi (Büyük yazılar)",
        variable=large_var,
        command=toggle_large_ui,
        font=("Arial", 12),
        bg=c["bg"],
        fg=c["dark"],
        activebackground=c["bg"],
        activeforeground=c["dark"],
        selectcolor=c["gray"]
    )

    large_check.pack(
        anchor="w",
        padx=30,
        pady=20
    )

    # islem gecmişi

    history_check = tk.Checkbutton(
        settings,
        text="İşlem geçmişini göster",
        variable=history_var,
        command=toggle_history,
        font=("Arial", 12),
        bg=c["bg"],
        fg=c["dark"],
        activebackground=c["bg"],
        activeforeground=c["dark"],
        selectcolor=c["gray"]
    )

    history_check.pack(
        anchor="w",
        padx=30,
        pady=10
    )

    # daha fazla tus

    advanced_check = tk.Checkbutton(
        settings,
        text="Ek işlemler (Bilimsel hesap makinesi)",
        variable=advanced_var,
        command=toggle_advanced,
        font=("Arial", 12),
        bg=c["bg"],
        fg=c["dark"],
        activebackground=c["bg"],
        activeforeground=c["dark"],
        selectcolor=c["gray"]
    )

    advanced_check.pack(
        anchor="w",
        padx=30,
        pady=15
    )

    # Kapat butonu

    close_button = tk.Button(
        settings,
        text="Kapat",
        font=("Arial", 12),
        bg=c["orange"],
        fg="white",
        activebackground=c["orange_hover"],
        bd=0,
        padx=30,
        pady=10,
        command=settings.destroy
    )

    close_button.pack(pady=20)



settings_button = tk.Button(
    header,
    text="Ayarlar",
    font=("Arial", 12),
    bd=0,
    padx=20,
    pady=10,
    cursor="hand2",
    command=open_settings
)

settings_button.grid(
    row=0,
    column=1,
    sticky="e"
)

history_clear_button.configure(
    command=clear_history
)




def keyboard_input(event):

    key = event.char

    if key in "0123456789().":
        press(key)

    elif key == ",":
        press(",")

    elif key == "+":
        press("+")

    elif key == "-":
        press("-")

    elif key == "*":
        press("×")

    elif key == "/":
        press("÷")

    elif key == "%":
        press("%")

    elif event.keysym == "Return":
        calculate()

    elif event.keysym == "BackSpace":
        backspace()

    elif event.keysym == "Escape":
        clear()


root.bind("<Key>", keyboard_input)




render_buttons()

root.mainloop()



