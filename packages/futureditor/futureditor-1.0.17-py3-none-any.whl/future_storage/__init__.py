#!/usr/bin/python
from tkinter import *
import os
from sys import platform
import json
from tkinter import colorchooser
import threading
from PIL import ImageTk,Image

try:
	with open("user_settings","r") as read_file:
		d = json.load(read_file)
		colour = d["bg"]
		colour2 = d["fg"]
		_font_ = d["font"]
		font_size = d["font_size"]
		cursor = d["cursor"]
except:
	colour = "white"
	colour2 = "black"
	font_size = 18
	_font_ = "avenir"
	cursor = "True"

try:
	read_file =  open("future-editor-cache.py","r")
	x = read_file.read()
	read_file.close()
	if x == "":
		x = "Hello there type code here to run"
except:
	x = "Welcome to future editor type code here to run"




def future_editor(colour=colour,colour2=colour2,font_size=font_size,_font_=_font_,text=x,_cursor_=cursor):

	#styling of the button and textbox is given here
	font= _font_
	font_size_ = font_size

	data = {
	"font":font,
	"font_size":font_size_,
	"bg":colour,
	"fg":colour2,
	"cursor":_cursor_
	}

	with open("user_settings","w") as write_file:
		json.dump(data,write_file)

	with open("user_settings","r") as read_file:
		global d
		d = json.load(read_file)

	bg=colour
	fg=colour2

	#takes the code from the text-box and saves it as a file using python in usrs/ directory
	global i
	i = 0

	def show_colour(for_bg=False,for_fg=False):
		colour = colorchooser.askcolor()[1]
		if colour == "":
			pass
		else:
			if for_bg == True:
				text_colour.delete(0,"end")
				text_colour.insert(0,colour)
			elif for_fg == True:
				text_colour_1.delete(0,"end")
				text_colour_1.insert(0,colour)

	def change_colour(colour,colour2,font,font_size,cursor):
		bg = colour
		fg = colour2
		window.destroy()
		try:
			future_editor(colour,colour2,font_size=font_size,_font_ = font,_cursor_=cursor)
		except:
			print("You did not enter a valid colour/font try relaunching the editor")
	def run_code():
		code_given = str(code.get("1.0",'end-1c'))
		create_file =  open("future-editor-cache.py","w+")
		create_file.write(code_given)
		create_file.close()
		try:
			os.system("python future-editor-cache.py")
		except:
			print("Your system does not have python in its system variable.")
	def debug():
		code_given = str(code.get("1.0",'end-1c'))
		create_file =  open("future-editor-cache.py","w+")
		create_file.write(code_given)
		create_file.close()
		try:
			os.system("python -m pdb future-editor-cache.py")
		except:
			print("Your system does not have python in its system variable/pdb not installed")
	def copy_():
		window.clipboard_clear()
		code_given = str(code.get("1.0",'end-1c'))
		window.clipboard_append(code_given)
		try:
			window.clipboard_update()
		except:
			pass

	def clear_():
		code.delete("1.0","end")

	def theme_():
		window_theme = Toplevel()
		window_theme.title("Theme")
		window_theme.config(bg=bg)

		label_window = Label(window_theme,bg=bg,fg=fg,font=font,text="Colour of window")
		label_window.grid(row=0,column=0,columnspan=2)

		global text_colour
		text_colour = Entry(window_theme,bg=bg,fg=fg,insertbackground=fg,font=font)
		text_colour.grid(row=1,column=0,columnspan=1)
		try:
			text_colour.insert(0,d["bg"])
		except:
			text_colour.insert(0,"white")

		show_colours = Button(window_theme,bg="white",fg="black",font=font,command=lambda: show_colour(for_bg=True),text="show colours")
		show_colours.grid(row=1,column=1,pady=10)

		label_font = Label(window_theme,bg=bg,fg=fg,font=font,text="Colour of Text")
		label_font.grid(row=2,column=0,columnspan=2)

		global text_colour_1
		text_colour_1 = Entry(window_theme,bg=bg,fg=fg,insertbackground=fg,font=font)
		text_colour_1.grid(row=3,column=0,columnspan=1)
		try:
			text_colour_1.insert(0,d["fg"])
		except:
			text_colour_1.insert(0,"black")
		
		show_colours = Button(window_theme,bg="white",fg="black",font=font,command=lambda: show_colour(for_fg=True),text="show colours")
		show_colours.grid(row=3,column=1,pady=10)


		label_font_ = Label(window_theme,bg=bg,fg=fg,font=font,text="Font and Font size")
		label_font_.grid(row=4,column=0,columnspan=2)

		font_ = Entry(window_theme,bg=bg,fg=fg,insertbackground=fg,font=font)
		font_.grid(row=5,column=0,columnspan=2,sticky=W+E)
		try:
			font_.insert(0,d["font"])
		except:
			font_.insert(0,"avenir")

		_font_size_ = Entry(window_theme,bg=bg,fg=fg,insertbackground=fg,font=font)
		_font_size_.grid(row=6,column=0,columnspan=2,sticky=W+E,pady=10)
		try:
			_font_size_.insert(0,d["font_size"])
		except:
			_font_size_.insert(0,"20")

		cursor = Label(window_theme,text="Block cursor",bg=bg,fg=fg,font=font)
		cursor.grid(row=7,column=0)

		cursor_ = Entry(window_theme,bg=bg,fg=fg,font=font,insertbackground=fg)
		cursor_.grid(row=7,column=1,pady=10)
		try:
			cursor_.insert(0,d["cursor"])
		except:
			cursor_.insert(0,"True")

		apply_button = Button(window_theme,bg="white",fg="black",font=font,command = lambda: change_colour(str(text_colour.get()),str(text_colour_1.get()),str(font_.get()),int(_font_size_.get()),str(cursor_.get())),text="Apply")
		apply_button.grid(row=8,column=0,pady=10,columnspan=2)


	window = Tk()
	window.title("Future-editor")
	window.config(bg=bg)

	scrollbar = Scrollbar(window,bg=bg,activebackground=bg,highlightbackground=bg,highlightcolor=bg)
	scrollbar.pack(side=RIGHT,fill=BOTH)

	global code
	code = Text(window,bg=bg,fg=fg,insertbackground=fg,font=(font,font_size_),undo=True,blockcursor=True,yscrollcommand = scrollbar.set,relief=RAISED)
	code.pack(side=LEFT,fill=BOTH)
	code.insert(END,text)


	if _cursor_ == "True":
		code.config(blockcursor=True)
	elif _cursor_ == "False":
		code.config(blockcursor=False)

	scrollbar.config( command = code.yview )

	def find():
		
		#remove tag 'found' from index 1 to END 
		code.tag_remove('found', '1.0', END) 
		#returns to widget currently in focus 
		s =  find_text.get()
		if s: 
			idx = '1.0'
			while True: 
				#searches for desried string from index 1 
				idx = code.search(s, idx, nocase=1,stopindex=END) 

				if not idx:
					break
				
				#last index sum of current index and 
				#length of text 
				lastidx = '%s+%dc' % (idx, len(s)) 
				
				#overwrite 'Found' at idx 
				code.tag_add('found', idx, lastidx) 
				idx = lastidx 
			
			#mark located string as red 
			code.tag_config('found', foreground='red') 

	def findcode():
		global findWin
		findWin = Toplevel()
		findWin.lift()
		global find_text
		find_text = Entry(findWin,bg=bg,fg=fg,font=font,insertbackground=fg)
		find_text.pack(side=LEFT)

		global search
		search = Button(findWin,bg="white",fg="black",font=font,text="Search",command=find)
		search.pack(side=RIGHT)

	def paste():
		position = code.index(INSERT)
		code.insert(position,window.clipboard_get())

	def popup(e):
		menu.tk_popup(e.x_root,e.y_root)

	#assigning menu bar
	menubar = Menu(window)
	window.config(menu=menubar)

	#new option in menu edit
	edit = Menu(menubar,tearoff=False)
	menubar.add_cascade(label="Edit",menu=edit)

	#new option in menu build
	build = Menu(menubar,tearoff=False)
	menubar.add_cascade(label="Build",menu=build)

	#new option in menu bar
	find_ = Menu(menubar,tearoff=False)
	menubar.add_cascade(label="Find",menu=find_)
	find_.add_command(label="Find",command=findcode)

	#right click menu bar
	menu = Menu(window,tearoff=False)

	build.add_command(label="Build",command=run_code)
	build.add_command(label="Debug",command=debug)

	for values in [menu,edit]:
		values.add_command(label="Copy",command=copy_)
		values.add_command(label="Paste",command=paste)
		values.add_command(label="Redo",command=code.edit_redo)
		values.add_command(label="Undo",command=code.edit_undo)
		values.add_command(label="Clear",command=clear_)
		values.add_command(label="Theme",command=theme_)
		values.add_separator()
		values.add_command(label="Exit",command=window.quit)


	window.bind("<Button-2>",popup)
	window.bind("<Button-3>",popup)

	window.mainloop()

def StartScreen(appwidth=436,appheight=310,seconds=2,imagepath=os.path.join(os.path.dirname(__file__),"Future-editor.png"),imageheight=436,imagewidth=310,bg="black"):
		print("Hello")
		tk = Tk()
		tk.config(bg=bg,bd=0)

		tk.lift()

		screen_width = tk.winfo_screenwidth()
		screen_height = tk.winfo_screenheight()

		x = int((screen_width/2) - (appwidth/2))
		y = int((screen_height/2) - (appheight/2))

		tk.geometry(f'{appwidth}x{appheight}+{x}+{y}')

		global img
		img = Image.open(imagepath)
		img = img.resize((imageheight, imagewidth), Image.ANTIALIAS)
		img = ImageTk.PhotoImage(img)

		tk.overrideredirect(True)
		Label(tk,image=img).pack()
		def after_that():
			tk.destroy()
			future_editor()

		tk.after((seconds*1000),after_that)

		tk.mainloop()
	
if __name__=='__main__':
	try:
		StartScreen()
	except:
		print("Theme ERROR: you did not enter a valid theme last time, try changing it now and restart the app")
		future_editor(colour="black",colour2="white",_font_="avenir",font_size=20,_cursor_="True")
