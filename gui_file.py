import tkinter as tk
from tkinter import ttk


class ScrollFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)  # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")  # Canvas to scroll
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")  # This frame will hold the child widgets
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)  # Attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")  # Pack scrollbar to right - change as needed
        self.canvas.pack(side="left", fill="both",
                         expand=True)  # Pack canvas to left and expand to fill - change as needed
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.viewPort,
            anchor="nw",
            tags="self.viewPort",
        )  # Add view port frame to canvas

        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        self.first = True
        self.onFrameConfigure(None)  # Initial stretch on render

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def on_mousewheel(self, event):
        '''Allows the mousewheel to control the scrollbar'''
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def bnd_mousewheel(self):
        '''Binds the mousewheel to the scrollbar'''
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def unbnd_mousewheel(self):
        '''Unbinds the mousewheel from the scrollbar'''
        self.canvas.unbind_all("<MouseWheel>")

    def delete_all(self):
        '''Removes all widgets from the viewPort, only works if grid was used'''
        children = self.viewPort.winfo_children()
        for child in children:
            child.grid_remove()


class CodeSampleForStackoverflow:
    def __init__(self, window):

        self.main_window = window
        self.mainframe = ttk.Frame(self.main_window, padding='15 3 12 12')
        self.mainframe.grid(column=0, row=0, sticky="W, E, N, S")

        self.file_choice = tk.StringVar()
        self.contents_list = list()

        self.display_folder_btn = ttk.Button(self.mainframe, text="Display list of choices", width=20,
                                             command=self.list_folder_contents)
        self.display_folder_btn.pack(side="top")

        self.folder_contents_frame = ScrollFrame(self.mainframe)
        self.folder_contents_frame.pack(side="top", fill="x", expand=False, padx=20, pady=20)

    def list_folder_contents(self):
        try:
            self.contents_list = ['A dictum nulla auctor id.', 'A porttitor diam iaculis quis.',
                                  'Consectetur adipiscing elit.', \
                                  'Curabitur in ante iaculis', 'Finibus tincidunt nunc.', 'Fusce elit ligula', \
                                  'Id sollicitudin arcu semper sit amet.', 'Integer at sapien leo.',
                                  'Lorem ipsum dolor sit amet', \
                                  'Luctus ligula suscipit', 'Nam vitae erat a dolor convallis', \
                                  'Praesent feugiat quam ac', 'Pretium diam.', 'Quisque accumsan vehicula dolor', \
                                  'Quisque eget arcu odio.', 'Sed ac elit id dui blandit dictum',
                                  'Sed et eleifend leo.', \
                                  'Sed vestibulum fermentum augue', 'Suspendisse pharetra cursus lectus',
                                  'Ultricies eget erat et', \
                                  'Vivamus id lorem mi.']
            contents_dict = dict()
            self.folder_contents_frame.delete_all()
            counter = 0
            for i in self.contents_list:
                contents_dict[str(counter + 1)] = i
                counter += 1
            for (text, value) in contents_dict.items():
                ttk.Radiobutton(self.folder_contents_frame.viewPort, text=value, variable=self.file_choice, value=text,
                                style="TRadiobutton").grid(column=0, columnspan=2, sticky=tk.W)

        except Exception as exc:
            print(exc)


# -----------------------------------------

def example():
    root = tk.Tk()
    root.title('Scrollable radiobutton list')
    root.geometry("500x600")
    tabs = ttk.Notebook(root)
    tabs.pack(fill="both")
    scrollable_radiobutton_list_frame = ttk.Frame(tabs)
    tabs.add(scrollable_radiobutton_list_frame, text="Scrollable radiobutton list")

    my_checker = CodeSampleForStackoverflow(window=scrollable_radiobutton_list_frame)

    root.mainloop()


