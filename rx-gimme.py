
from tkinter import (Tk, Grid, Frame, Entry, Button, Label, END, ttk, VERTICAL,
                     Checkbutton, IntVar, messagebox, Text, Scrollbar,
                     filedialog)
from bs4 import BeautifulSoup, SoupStrainer
import requests
import sys
import os


def inutil():
    if len(sys.argv) <= 1:
        sys.exit("ERROR: You should provide at least one URL")
        columns = int(os.popen('stty size', 'r').read().split()[1])
        separator = '-' * columns
        sys.argv.pop(0)

        for arg in sys.argv:
            try:
                url = arg
                page = requests.get(url)
                data = page.text
                soup = BeautifulSoup(data, "html.parser")
                print("\n" + separator)
                print("\nGetting links from: " + url + "\n")

                for link in soup.find_all('a'):
                    if link.get('href') is not None:
                        if link.get('href')[0] == "/":
                            print(url + link.get('href'))
                        elif link.get('href')[0] == "#":
                            print(url + "/" + link.get('href'))
                        else:
                            print(link.get('href'))
                            print("\n" + separator + "\n")
            except Exception:
                sys.exit("ERROR: Not valid URL -->: " + url)


class Window():
    def __init__(self, root):

        self.root = root
        self.root.title("rx-gimme  v0.1")
        self.root.grid_anchor(anchor='c')

        self.first_row = 0
        self.first_column = 0
        self.max_plot = 10

        frame = Frame(root)

        self.label_url = Label(frame, text="Enter URL: ")
        self.label_url.grid(row=self.first_row, column=self.first_column,
                            sticky="w", padx=4, pady=4)

        self.entry_url = Entry(frame, width=50)
        self.entry_url.grid(row=self.first_row, column=self.first_column + 1)
        self.entry_url.insert(0, "http://www.google.com/")

        self.button_url = Button(frame, text="Gimme!", width=10,
                                 command=self.gimme)
        self.button_url.grid(row=self.first_row, column=self.first_column + 2)

        self.button_save = Button(frame, text="Save buffer...", width=10,
                                  command=self.file_save_as)
        self.button_save.grid(row=self.first_row, column=self.first_column + 3)

        self.lines = 40
        self.scrollbar = Scrollbar(frame, orient="vertical")
        self.text = Text(frame, height=self.lines,
                         yscrollcommand=self.scrollbar.set)
        self.text.grid(row=self.first_row + 1, column=self.first_column,
                       columnspan=4, sticky="EW", padx=4, pady=4)
        self.scrollbar.grid(row=self.first_row + 1,
                            column=self.first_column + 4, sticky="NS")
        self.scrollbar.config(command=self.text.yview)

        frame.grid()

    def gimme(self):
        self.text.delete('1.0', END)
        self.text.insert(END, "\nGetting links from: " + self.entry_url.get()
                         + "\n\n")
        self.text.see("end")

        try:
            url = self.entry_url.get()
            page = requests.get(url)
            data = page.text
            soup = BeautifulSoup(data, "html.parser")

            for link in soup.find_all('a'):
                if link.get('href') is not None:
                    if link.get('href')[0] == "/":
                        self.text.insert(END, url + link.get('href') + '\n')
                    elif link.get('href')[0] == "#":
                        self.text.insert(END, url + "/" + link.get('href')
                                         + '\n')
                    else:
                        self.text.insert(END, link.get('href') + '\n')

                self.text.see("end")

        except Exception:
            self.error("Not valid URL:" + url)

    def file_save_as(self, event=None, filepath=None):
        if filepath is None:
            filepath = filedialog.asksaveasfilename(
                filetypes=(
                    ('Text files', '*.txt'),
                    ('Python files', '*.py *.pyw'),
                    ('All files', '*.*'),
                ),
            )
        try:
            with open(filepath, 'wb') as f:
                textt = self.text.get(1.0, "end-1c")
                f.write(bytes(textt, 'UTF-8'))
                self.editor.edit_modified(False)
                self.file_path = filepath
                self.set_title()
                self.error("File saved!")
        except FileNotFoundError:
            self.error("File not saved!")

    def error(self, message):
        messagebox.showerror("Error", message)

    def main(self):
        pass


if __name__ == "__main__":
    root = Tk()
    window = Window(root)
    window.main()
    root.mainloop()
