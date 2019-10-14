import tkinter as tk
from logger import Logger, LogLevels, DefaultFormat

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.logLevel = tk.StringVar()
        self.logLevel.set(LogLevels.INFO.name)

        self.message_field = None
        self.format_field = None
        self.filename_field = None

        self.pack()
        self.create_widgets()

    def create_loglevel_control(self):
        for level in LogLevels:
            button = tk.Radiobutton(
                self,
                variable=self.logLevel,
                value=level.name,
                text=level.name
            )
            button.pack()

    def create_message_field(self):
        text = tk.Label(self, text='Message')
        text.pack()
        self.message_field = tk.Entry(self)
        self.message_field.pack()

    def create_format_field(self):
        text = tk.Label(self, text='Format')
        text.pack()
        self.format_field = tk.Entry(self)
        self.format_field.insert(tk.END, DefaultFormat)
        self.format_field.pack()

    def create_filename_field(self):
        text = tk.Label(self, text='File Name (leave empty for console mode)')
        text.pack()
        self.filename_field = tk.Entry(self)
        self.filename_field.insert(tk.END, './file.csv')
        self.filename_field.pack()

    def create_send_button(self):
        send_button = tk.Button(
            self,
            text='Send',
            command=self.__log
        )
        send_button.pack()

    def create_widgets(self):
        self.create_message_field()
        self.create_format_field()
        self.create_filename_field()
        self.create_loglevel_control()
        self.create_send_button()

    def __log(self):
        level = self.logLevel.get()
        message = self.message_field.get()
        message_format = self.format_field.get()

        logger = Logger(None if self.filename_field.get() == '' else self.filename_field.get())
        logger.setFormat(DefaultFormat if message_format == None or '' else message_format)

        if level == LogLevels.INFO.name:
            logger.info(message)
        elif level == LogLevels.TRACE.name:
            logger.trace(message)
        elif level == LogLevels.ERROR.name:
            logger.error(message)
        else:
            raise NotImplementedError

def main():
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()

main()
