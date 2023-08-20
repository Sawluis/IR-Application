# Imports
from tkinter import messagebox, ttk
from customtkinter import CTk, CTkFrame, CTkEntry, CTkLabel, CTkButton
from tax_calculator_package import get_ir, TaxResult
import tkinter as tk

# Colors
black_color = '#1A1A1D'
light_gray_color = '#4c4f53'
light_gray_color2 = '#a0a6ad'
white_color = '#ffffff'
blue_color = '#067bd3'
light_blue_color = '#a09fd3'

# Background_Color
background_color = black_color

# Text_Color
text_color = white_color

# Title_Color
title_color = blue_color
title_two_color = light_blue_color

# Button
button_color = white_color
hover_color = light_gray_color2

# Paddings
##Labels
padding_labels_x = 5
padding_labels_y = 20

##Inputs
padding_inputs_x = 2
padding_inputs_y = 10

###Resolves
padding_resolves_x = 5
padding_resolves_y = 4

#Character_Limit
character_limit = 48


# Functions
def calculator():
    calculate = get_ir(float(salary_input.get()))

    result: list[TaxResult] = [calculate.inss, calculate.month_salary_without_inss,
                                calculate.annual_salary_without_inss, calculate.ir,
                                calculate.total_salary_with_deductions]

    count = 0
    for i in inputs:
        i.configure(text=f'C${result[count]}')
        count += 1

    resol = [f'Salario mensual*7% = {calculate.month_salary} * 0.07',
             f'Salario mensual - Inss = {calculate.month_salary} - {calculate.inss}', 
             f'(Salario mensual - Inss) * 12 = {calculate.month_salary - calculate.inss} * 12',
             f'(Salario anual-Sobreexceso)*Porcentaje aplicable+\nImpuesto base/12 meses\n= (({calculate.annual_salary_without_inss}) - '
             f'{calculate.parameter.remove_value}) * {calculate.parameter.percentage} + {calculate.parameter.base_tax}) / 12',
             f'Salario neto-IR = {calculate.month_salary_without_inss} - {calculate.ir}']

    count = 0
    for i in resolves:
        i.configure(text=resol[count])
        if count == 3:
            i.configure(height=110)
        count += 1


def validate_number():
    while True:
        try:
            float_number = salary_input.get()

            if float_number.startswith("C$"):
                salary_input.delete(0, tk.END)
                salary_input.insert(0, float_number[2:])

                float_number = float(salary_input.get())

                if float_number < 0.01:
                    salary_input.insert(0, "C$")
                    messagebox.showerror("Error", "Ingresa un valor válido")
                    break
                else:
                    calculator()
                    salary_input.insert(0, 'C$')
                    break
            else:
                salary_input.delete(0, tk.END)
                salary_input.insert(0, "C$")
        except ValueError:
            salary_input.delete(0, tk.END)
            salary_input.insert(0, "C$")
            messagebox.showerror("Error", "Ingresa un valor numérico válido")
            break


def on_entry_click(event):
    if salary_input.get() == "C$ - Ingrese su salario":
        salary_input.delete(0, tk.END)
        salary_input.insert(0, "C$")


def validate_length(P):
    if len(P) > character_limit:
        frame.bell()
        messagebox.showerror("Error", "Alcanzó el limite de carácteres válidos")
        return False
    return True


# Windows_Configurations
window = CTk()
window.geometry('500x650+750+10')
window.minsize(width=680, height=980)
window.maxsize(width=700, height=990)
window.config(bg='#2e1042')
window.title("Proyecto Final-Control")
#window.iconbitmap('images/IR.ico')

# Frame_Configuration
frame = CTkFrame(window, fg_color=background_color)
frame.grid(column=0, row=0, sticky='nsew', padx=1.5, pady=1.5)

for i in range(2):
    frame.columnconfigure(i, weight=1)
for i in range(20):
    frame.rowconfigure(i, weight=1)

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

# Components
# Labels
labels_text = ['Ingrese su salario mensual', 'Deducción INSS', 'Salario neto (luego de deducciones)',
               'Salario anual (luego de deducciones)',
               'Deducción Impuesto sobre la Renta (IR)', 'Salario total mensual con deducciones']
labels_count = 1
labels = []

for text in labels_text:
    lab = CTkLabel(frame, text=text, font=("Arial Bold", 16),
                   fg_color=background_color, width=400, height=75, anchor='w', text_color=title_two_color)
    lab.grid(columnspan=2, row=labels_count, padx=padding_labels_x, pady=(padding_labels_y, 0))
    labels.append(lab)
    if labels_count < 3:
        labels_count += 2
    else:
        labels_count += 3

# Inputs
inputs_text = ['C$0', 'C$0', 'C$0', 'C$0', 'C$0']
inputs_count = 5
inputs = []

for text in inputs_text:
    inp = CTkLabel(frame, text=text, font=("Arial", 16),
                   fg_color=background_color, padx=padding_inputs_x,
                   width=400, height=68, anchor='w', text_color=text_color, justify='left')
    inp.grid(columnspan=2, row=inputs_count, pady=(0, padding_inputs_y))
    inputs.append(inp)
    inputs_count += 3

# Resolves
resolves_text = ['Inss=Salario mensual * 7%',
                 'Salario neto=Salario mensual-Inss', 
                 'Salario anual=(Salario mensual-Inss) * 12',
                 'IR=((Salario anual - Sobreexceso) * Porcentaje aplicable + \n'
                 'Impuesto base) / 12 meses', 'Salario total=Salario neto - IR']

resolves_count = 4
resolves = []

for text in resolves_text:
    res = CTkLabel(frame, text=text, font=("Arial", 14), fg_color=background_color,
                   width=400, height=84, anchor='w', text_color=light_gray_color2,
                   justify='left')
    res.grid(columnspan=2, row=resolves_count, padx=padding_resolves_x, pady=padding_resolves_y)
    resolves.append(res)
    resolves_count += 3

##Title
title = CTkLabel(frame, text='Calculadora IR', font=("Arial Bold", 22),
                 fg_color=background_color, pady=30, padx=10, height=72, text_color=title_color)
title.grid(columnspan=2, row=0)

##Salary_Input
vcmd = frame.register(validate_length)
salary_input = CTkEntry(frame, font=("Arial", 14),  # placeholder_text='C$ - Ingrese su salario',
                        border_color=light_gray_color2, fg_color=background_color, width=400, height=80, justify='left',
                        text_color=text_color, validate='key', validatecommand=(vcmd, '%P'))
salary_input.grid(columnspan=2, row=2, padx=padding_inputs_x, pady=(padding_inputs_y, padding_inputs_y + 5))
salary_input.insert(0, 'C$ - Ingrese su salario')
salary_input.bind("<FocusIn>", on_entry_click)

##Calculate_Button
calculate_button = CTkButton(frame, text="Calcular ahora", border_color=button_color, fg_color=background_color,
                             hover_color=hover_color, corner_radius=12, border_width=1, command=validate_number,
                             height=80, text_color=button_color)
calculate_button.grid(columnspan=2, row=18, pady=20)

#Income_Tax_Law_Table
tree = ttk.Treeview(frame)

tree["columns"] = ("Min Value", "Max Value", "Remove Value", "Percentage", "Base Tax")
tree.column("#0", width=0, stretch=tk.NO)
tree.heading("#0", text="", anchor=tk.CENTER)
tree.heading("#1", text="", anchor=tk.CENTER)
styles = ttk.Style()
styles.configure('Treeview.Heading', foreground=blue_color, font=('Times New Roman', 7))
styles.configure('Treeview') #background=background_color, foreground=white_color)


table_header = ["Estratos de\nRenta Anual", "", "Sobre exceso\n          de", "Porcentaje\naplicable", "Impuesto base"]
table_values = [ ('De C$', 'Hasta C$', 'C$', '%', 'C$'), ('0.01', '100,000', '0', '0.0%', '0'), ('100,000.01', '200,000', '100,000', '15.0%', '0'),
    ('200,000.01', '350,000', '200,000', '20.0%', '15,000'),
    ('350,000.01', '500,000', '350,000', '25.0%', '45,000'),
    ('500,000.01', 'a más', '500,000', '30.0%', '82,500') ]
    
count = 1

for text_head, id in zip(table_header, tree["columns"]):
    tree.column(id, anchor=tk.CENTER, width=90)
    tree.heading(id, text=text_head, anchor=tk.CENTER)

for values in table_values:
    tree.insert("", "end", text=str(count), values=(table_values[count-1]))
    count += 1
        
tree.grid(padx=100, pady=10)

# InfoButton
info_label = CTkLabel(frame, text="Dev by Michelle Calderón, Luis Pineda, Gabriel Ortíz", font=("Arial", 13),
                       fg_color=background_color, padx=padding_inputs_x, pady=padding_inputs_y,
                       width=400, height=50, text_color=light_gray_color2)
info_label.grid(columnspan=2, row=20, pady=20)

# Cicle
window.mainloop()