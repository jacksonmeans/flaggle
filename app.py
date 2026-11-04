import os
from PIL import Image, ImageTk
import tkinter as tk
import random
from tkinter import ttk
import platform
import unicodedata
from unidecode import unidecode
import sys
from os.path import dirname

class Flag:
    def __init__(self):
        if category == -1:
            num = random.randint(0, len(standard) + len(historic) + len(historic_shapes) - 1)
            if num + 1 <= len(standard):
                self.subdir = flag_categories_list[0]
                self.territory = sorted(os.listdir(base_dir+'/flag_icons'+self.subdir),reverse=True)[num]
            elif num + 1 <= len(standard) + len(historic):
                self.subdir = flag_categories_list[1]
                self.territory = sorted(os.listdir(base_dir+'/flag_icons'+self.subdir),reverse=True)[num - len(standard)]
            elif num + 1 <= len(standard) + len(historic) + len(historic_shapes):
                self.subdir = flag_categories_list[2]
                self.territory = sorted(os.listdir(base_dir+'/flag_icons'+self.subdir),reverse=True)[num - len(standard) - len(historic)]
            else:
                self.subdir = flag_categories_list[3]
                self.territory = sorted(os.listdir(base_dir+'/flag_icons'+self.subdir),reverse=True)[num - len(standard) - len(historic) - len(historic_shapes)]
        else:
            self.subdir = random.choice(flag_categories_list)
            self.random_num = random.randint(0,len(os.listdir(base_dir+'/flag_icons'+self.subdir))-1)
            self.territory = sorted(os.listdir(base_dir+'/flag_icons'+self.subdir),reverse=True)[self.random_num]
                
    def show_image(self):
        #do after correct answer
        img = Image.open(base_dir+'/flag_icons'+self.subdir+self.territory)
        resized = img.resize((200, 120))
        tk_img = ImageTk.PhotoImage(resized)
        
        #config instead of create new, make sure guess is cleared and new flag is set

        label1.image = tk_img
        label1.config(image=tk_img)

    def reset(self):
        self.__init__()
        self.show_image()
        
    def guess(self, label):
        #scrollable root
        #actual flag, comparison to answer
        flag_categories_list = ['/standard/','/historic/','/historic_shapes/','/modern_shapes/']
        for i in flag_categories_list:
            try:
                a_subdir = os.path.dirname(base_dir+'/flag_icons' + i + flags[a.text_variable.get()])
                img = Image.open(a_subdir + '/' + flags[a.text_variable.get()])
            except:
                pass
        
        resized = img.resize((200, 120))
        tk_img = ImageTk.PhotoImage(resized)
        label.image=tk_img

        label.config(image=tk_img)
        #MAKE SAME CHANCE FOR ALL
        if flags[a.text_variable.get()] == self.territory:
            self.reset()
            a.text_variable.set('')



class AutoFillCombobox(tk.Frame):
    def __init__(self, master, values: list = None, text_variable: tk.StringVar = None,
                 entry_width=10, listbox_length=100, relief="groove", borderwidth=1, *args, **kwargs):
        super().__init__(master, *args, relief=relief, borderwidth=borderwidth, **kwargs)

        self.text_variable = text_variable or tk.StringVar(self)
        self.values = values or []

        # Some widget sizes
        self._entry_width = entry_width
        self._listbox_length = listbox_length

        # Dropdown window references
        self._dropdown_window = None
        self._dropdown_open = False
        self._listbox = None

        self._create_widgets()
        self._bind_events()


    def _create_widgets(self):
        self.entry = tk.Entry(self, width=self._entry_width, relief="flat", textvariable=self.text_variable)
        self.dropdown_button = tk.Button(self, text='▼', relief="flat", command=self._on_dropdown_button_click)

        self.entry.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.dropdown_button.pack(side=tk.RIGHT, fill=tk.BOTH)

    def _bind_events(self):
        self.text_variable.trace_add("write", self._on_entry)

        # Bind arrow key event on entry to interact with dropdown
        self.entry.bind("<Up>", lambda *_: self._move_selection(-1))
        self.entry.bind("<Down>", lambda *_: self._move_selection(1))

        # Bind events from root to close dropdown
        self.winfo_toplevel().bind("<Button>", self._on_root_event, add="+")
        self.winfo_toplevel().bind("<Configure>", self._on_root_event, add="+")

    def _on_entry(self, *_) -> None:
        term = self.text_variable.get()
        if not term:
            # Closes the dropdown if no user input
            self.toggle_dropdown(False)
            return

        values = self.filter_values(term)
        if not values:
            # Closes the dropdown if no values match the term
            self.toggle_dropdown(False)
            return

        self.toggle_dropdown(True)
        self._fill_listbox(values)

    def _on_dropdown_button_click(self) -> None:
        if self._dropdown_open:
            # Closes the dropdown if already open
            self.toggle_dropdown(False)
            return

        # Opens the dropdown even if no values are filtered
        values = self.filter_values(self.text_variable.get())
        self.toggle_dropdown(True)
        self._fill_listbox(values)

    def _on_root_event(self, e) -> None:
        widget = e.widget
        # Don't close dropdown if event was on 'entry' or 'dropdown_button'
        if widget == self.dropdown_button or widget == self.entry:
            return
        self.toggle_dropdown(False)

    def _on_select(self, *_) -> None:
        if self._dropdown_open:
            self.text_variable.set(self._listbox.get(tk.ACTIVE))
            self.toggle_dropdown(False)
            self.entry.icursor(tk.END)
            flag.guess(label)

    def _on_mouse_over(self, e) -> None:
        widget = e.widget
        x, y = e.x, e.y
        index = widget.nearest(y)

        for i in range(widget.size()):
            self._listbox.selection_clear(i)

        self._listbox.activate(index)
        self._listbox.selection_set(index)

    def _move_selection(self, direction: int) -> None:
        if self._dropdown_open:
            index = self._listbox.curselection()[0] if self._listbox.curselection() else 0
            new_index = max(0, min(self._listbox.size() - 1, index + direction))

            self._listbox.selection_clear(first=index)
            self._listbox.see(new_index)
            self._listbox.selection_set(first=new_index)
            self._listbox.activate(new_index)

    def _fill_listbox(self, values: list[str]) -> None:
        if self._listbox is None:
            return

        self._listbox.delete(0, tk.END)
        for v in values:
            self._listbox.insert(tk.END, v)

        # Activates and selects the first index of listbox
        self._listbox.activate(0)
        self._listbox.selection_set(0)

    def _delete(self, _):
        self.text_variable.set('')

    def _create_dropdown_window(self) -> tuple[tk.Listbox, tk.Toplevel]:
        w = tk.Toplevel(self)
        w.wm_overrideredirect(True)

        frame = tk.Frame(w)
        listbox = tk.Listbox(frame)

        # Binds every event required for smooth interaction with listbox
        listbox.bind_all("<Return>", self._on_select)
        listbox.bind_all("<Control-BackSpace>",self._delete)
        listbox.bind("<Button-1>", self._on_select)
        listbox.bind("<Motion>", self._on_mouse_over)
        listbox.bind("<Enter>", self._on_mouse_over)

        def on_scroll(number, e):
            listbox.yview_scroll(number, "units")
            listbox.after(0, lambda: self._on_mouse_over(e))

        if platform.system() == "Windows":
            listbox.bind("<MouseWheel>", lambda e: on_scroll(-1 if e.delta > 0 else 1, e))
        else:
            listbox.bind("<Button-4>", lambda e: on_scroll(-1, e))
            listbox.bind("<Button-5>", lambda e: on_scroll(1, e))

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        listbox.pack(side="left", fill="both", expand=True)

        frame.pack(fill="both", expand=True)
        return listbox, w

    def toggle_dropdown(self, state: bool) -> None:
        """ Opens and closes the dropdown by calling 'wm_deiconify()' and 'wm_withdraw()'."""
        if state == self._dropdown_open:
            return

        if state:
            if not self._dropdown_window:
                # Creates a new dropdown window if not exists
                self._listbox, self._dropdown_window = self._create_dropdown_window()

            # Changes window geometry based on instance current size and position
            width, height = self.winfo_width(), self._listbox_length
            x, y = self.winfo_rootx(), (self.winfo_rooty() + self.winfo_height())
            self._dropdown_window.wm_geometry(f"{width}x{height}+{x}+{y}")

            self._dropdown_window.wm_deiconify()
        else:
            if self._dropdown_window is not None:
                self._dropdown_window.wm_withdraw()

        self._dropdown_open = state

    def filter_values(self, term: str) -> list[str]:
        # Filters every value that contains 'term' case-insensitive
        term = unidecode(term.lower())
        #keep visible option string raw, but filter by unidecoded value
        return [v for v in self.values if term in unidecode(v.lower())]


root = tk.Tk()
root.title("Flaggle")
root.geometry("500x500+400+100")


class OptionDialog(tk.Toplevel):
    """
        This dialog accepts a list of options.
        If an option is selected, the results property is to that option value
        If the box is closed, the results property is set to zero
    """
    def __init__(self,parent,title,question,options):
        tk.Toplevel.__init__(self,parent)
        self.title(title)
        self.question = question
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW",self.cancel)
        self.options = options
        self.result = '_'
        self.createWidgets()
        self.grab_set()
        ## wait.window ensures that calling function waits for the window to
        ## close before the result is returned.
        self.wait_window()
    def createWidgets(self):
        frmQuestion = tk.Frame(self)
        tk.Label(frmQuestion,text=self.question).grid()
        frmQuestion.grid(row=1)
        frmButtons = tk.Frame(self)
        frmButtons.grid(row=2)
        column = 0
        for option in self.options:
            btn = tk.Button(frmButtons,text=option,command=lambda x=option:self.setOption(x))
            btn.grid(column=column,row=0)
            column += 1 
    def setOption(self,optionSelected):
        self.result = optionSelected
        self.destroy()
    def cancel(self):
        self.result = 'All'
        self.destroy()


values = ['All','Standard','Historic','Historic Shapes', 'Modern Shapes']
dlg = OptionDialog(root,'Category Selection','Select a category',values)
try:
    category = (values.index(dlg.result) - 1)
except ValueError:
    sys.exit(0)


label1 = tk.Label(root, image=None)
label1.pack(side='top',pady=20)


options = tk.Menu(root)
options.geometry=(f'500x100+{(root.winfo_screenwidth()-500)/2}+{(root.winfo_screenheight() - 100)/2}')
root.config(menu=options)
'''button = tk.Button(options, text = 'All', height=1,width=5)
button.grid()'''

base_dir = os.getcwd()
dir_list = sorted(os.listdir(dirname(__file__) + '/flags/flag_icons'))

standard = ['Andorra','United Arab Emirates','Afghanistan','Antigua and Barbuda','Anguilla','Albania','Armenia','Angola','Antarctica','Argentina','American Samoa','Austria','Australia','Aruba','Åland','Azerbaijan','Bosnia and Herzegovina','Barbados','Bangladesh','Belgium','Burkina Faso','Bulgaria','Bahrain','Burundi','Benin','Saint Barthélemy','Bermuda','Brunei','Bolivia','Bonaire','Brazil','Bahamas','Bhutan','Bouvet Island','Botswana','Belarus','Belize','Canada','Cocos (Keeling) Islands','Democratic Republic of the Congo','Central African Republic','Republic of the Congo','Switzerland',"Côte d'Ivoire",'Cook Islands','Chile','Cameroon','China','Colombia','Costa Rica','Cuba','Cabo Verde','Curaçao','Christmas Island','Cyprus','Czech Republic','Germany','Djibouti','Denmark','Dominica','Dominican Republic','Algeria','Ecuador','Estonia','Egypt','Sahrawi Arab Democratic Republic','Eritrea','Spain','Ethiopia','Finland','Fiji','Falkland Islands','Federated States of Micronesia','Faroe Islands','France','Gabon','England','Northern Ireland','Scotland','Wales','United Kingdom','Grenada','Georgia','French Guiana','Guernsey','Ghana','Gibraltar','Greenland','The Gambia','Guinea','Guadeloupe','Equatorial Guinea','Greece','South Georgia and the South Sandwich Islands','Guatemala','Guam','Guinea-Bissau','Guyana','Hong Kong','Heard and McDonald Islands','Honduras','Croatia','Haiti','Hungary','Indonesia','Ireland','Israel','Isle of Man','India','British Indian Ocean Territory','Iraq','Iran','Iceland','Italy','Jersey','Jamaica','Jordan','Japan','Kenya','Kyrgyzstan','Cambodia','Kiribati','Comoros','Saint Kitts and Nevis','North Korea','South Korea','Kuwait','Cayman Islands','Kazakhstan','Laos','Lebanon','Saint Lucia','Liechtenstein','Sri Lanka','Liberia','Lesotho','Lithuania','Luxembourg','Latvia','Libya','Morocco','Monaco','Moldova','Montenegro','Madagascar','Marshall Islands','North Macedonia','Mali','Myanmar','Mongolia','Macau','Northern Mariana Islands','Martinique','Mauritania','Montserrat','Malta','Mauritius','The Maldives','Malawi','Mexico','Malaysia','Mozambique','Namibia','New Caledonia','Niger','Norfolk Island','Nigeria','Nicaragua','The Netherlands','Norway','Nepal','Nauru','Niue','New Zealand','Oman','Panama','Peru','French Polynesia','Papua New Guinea','The Philippines','Pakistan','Poland','Saint Pierre and Miquelon','Pitcairn Islands','Puerto Rico','Palestine','Portugal','Palau','Paraguay','Qatar','Réunion','Romania','Serbia','Russia','Rwanda','Saudi Arabia','Solomon Islands','Seychelles','Sudan','Sweden','Singapore','Saint Helena','Slovenia','Svalbard and Jan Mayen','Slovakia','Sierra Leone','San Marino','Senegal','Somalia','Suriname','South Sudan','São Tomé and Príncipe','El Salvador','Sint Maarten','Syria','Eswatini','Turks and Caicos Islands','Chad','French Southern and Antarctic Lands','Togo','Thailand','Tajikistan','Tokelau','Timor-Leste','Turkmenistan','Tunisia','Tonga','Türkiye','Trinidad and Tobago','Tuvalu','Taiwan','Tanzania','Ukraine','Uganda','United States of America','Uruguay','Uzbekistan','Vatican City','Saint Vincent and the Grenadines','Venezuela','British Virgin Islands','United States Virgin Islands','Vietnam','Vanuatu','Wallis and Futuna','Samoa','Kosovo','Yemen','Mayotte','South Africa','Zambia','Zimbabwe']
historic = ['Belgian Congo','Burgenland','China (1912-1923)','Federated Malay States','Lesotho (1966-1987)','Manchukuo','Rhodesia','South Vietnam','Surinam (1959-1975)']
historic_shapes = ['Descate','Double-tailed descate','Gonfanon','Lanceolate','Schwenkel','Triangular (historic)']#
modern_shapes = ['Double swallow-tailed', 'Gonfalon', 'Swallow-tailed','Triangular','Triangular swallow-tailed']
flag_names = standard + historic + historic_shapes + modern_shapes

flag_categories_list = ['/standard/','/historic/','/historic_shapes/', '/modern_shapes/']

flags = {}
flag_names_images = {}



count = 0
for y in flag_categories_list:
    for _,x in enumerate(sorted(os.listdir(base_dir+'/flag_icons'+y))):
        flags[flag_names[count]] = x
        count += 1

count = 0

flag_categories_list = [flag_categories_list[category]]

match category:
    case -1:
        flag_names = standard + historic + historic_shapes + modern_shapes
        flag_categories_list = ['/standard/','/historic/','/historic_shapes/','/modern_shapes']
    case 0:
        flag_names = standard
    case 1:
        flag_names = historic
    case 2:
        flag_names = historic_shapes
    case 3:
        flag_names = modern_shapes

for y in flag_categories_list:
    for _,x in enumerate(sorted(os.listdir(base_dir+'/flag_icons'+y))):
        flag_names_images[flag_names[count]] = x
        count += 1


flag_names = standard + historic + historic_shapes + modern_shapes
a = AutoFillCombobox(root, sorted(flag_names, key = lambda x: unicodedata.normalize('NFD',x)), entry_width=20, listbox_length=len(flag_names))
a.pack()


label = tk.Label(root)
label.place(relx=.3,rely=.5)

flag = Flag()
flag.show_image()

if __name__ == "__main__":
    options.mainloop()
