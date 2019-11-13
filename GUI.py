from operation import OpenExchange
from tkinter import *
from tkinter import ttk

APP_ID = "8812fb8e3ec9476e8a164b511b20236c"
API_OBJECT = OpenExchange(APP_ID)

field_font = ("Times New Roman", "20")
entry_font = ("Times New Roman", "20")
button_font = ("Times New Roman", "20")


class MainUI:
    def __init__(self, root):
        self.root = root

        root.geometry("900x900")
        root.title("Currency Exchange Converter")

        self.Base_Field = Label(root, text="Base Currency: ", font=field_font)
        self.Base_Field.grid(row=0, column=0, sticky="W", pady=2)

        self.Output_Field = Label(root, text="Converted Currency: ", font=field_font)
        self.Output_Field.grid(row=1, column=0, sticky="W", pady=2)

        self.Base_Amount = Entry(root, width=15, font=entry_font)
        self.Base_Amount.grid(row=0, column=1, pady=2)

        self.Output_Amount = Label(root, width=15, text="0", font=entry_font)
        self.Output_Amount.grid(row=1, column=1, pady=2)

        self.Base_Selection = ttk.Combobox(root, font=entry_font, values=self.all_currencies())
        self.Base_Selection.grid(row=0, column=2, pady=2)
        self.Base_Selection.current(0)

        self.Output_Selection = ttk.Combobox(root, font=entry_font, values=self.all_currencies())
        self.Output_Selection.grid(row=1, column=2, pady=2)
        self.Output_Selection.current(0)

        self.convert_button = Button(root, text="Convert", command=self.get_conversion, font=button_font)
        self.convert_button.grid(row=2, column=0, pady=2)

        self.stats_button = Button(root, text="Stats", command=self.get_stats, font=button_font)
        self.stats_button.grid(row=2, column=1, pady=2)

        self.quit_button = Button(root, text="Quit", command=root.destroy, font=button_font)
        self.quit_button.grid(row=2, column=2, pady=2)

        self.alert = Label(root, text="General Alert", font=field_font)
        self.alert.grid(row=3, column=1, padx=5, pady=5)

    def pop_up(self, string):
        popup = Tk()
        popup.title("Alert!")
        label = ttk.Label(popup, text=string)
        label.pack(side="top", fill="x", pady=10)
        close_button = ttk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack()
        popup.mainloop()

    def error_handler(self, error):
        if isinstance(error, ValueError):
            string = "Invalid entry. Please only use numbers for base value."
            self.pop_up(string)

        elif isinstance(error, KeyError):
            string = "Unknown currency. Please make sure your currency is correct."
            self.pop_up(string)

        else:
            string = "Unknown error. Please restart the program."
            self.pop_up(string)
        return

    def get_conversion(self):
        amount = self.Base_Amount.get()
        base = self.Base_Selection.get()[:3].upper()
        output = self.Output_Selection.get()[:3].upper()

        try:
            user_input = float(amount)
            converted = API_OBJECT.convert(user_input, base, output)
            self.Output_Amount.configure(text=converted)
        except (ValueError, KeyError) as error:
            self.error_handler(error)
        return

    def all_currencies(self):
        data = API_OBJECT.get_all_currencies()
        return data

    def get_stats(self):
        stats = API_OBJECT.get_usage()
        string = f"Completed Request: {stats[0]}" \
                 f"\nRemaining Request: {stats[1]}" \
                 f"\nDays Elapsed: {stats[2]}" \
                 f"\nDaily Average: {stats[3]}"
        self.alert.configure(text=string)
        return
