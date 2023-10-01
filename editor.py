import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import chardet
import tkinter.font as tkFont
import re
import keyword
from ttkthemes import ThemedStyle

root = tk.Tk()
root.title("Python Editor")
font_path = "./res/tk.ttf"
root.geometry("600x600")
custom_font = tkFont.Font(family="Consolas", size=16)

# Global variable to store the current file path
current_file = None
# Function to save a file
python_keywords = keyword.kwlist


class hotkey:
    def NewFile():
        editor.delete('1.0', tk.END)

    def OpenFile():
        global current_file
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    editor.delete('1.0', tk.END)
                    editor.insert('1.0', file.read())
                current_file = file_path

                exe.update_status_bar(current_file)
                highlight_syntax()
            except Exception as e:
                messagebox.showerror("错误", f"发生错误：\n{type(e).__name__}:{e}")
    def SaveFile():

        global current_file
        if current_file:
            if combo_var != '':
                try:
                    print(type(str(combo_var)),str(combo_var.get()))
                    with open(current_file, 'w', encoding='utf-8') as file:
                        file.write(editor.get('1.0', tk.END))

                    exe.update_status_bar(current_file)
                except Exception as e:
                    messagebox.showerror("错误", f"发生错误：\n{type(e).__name__}:{e}")
            else:
                pass

        else:
          hotkey.SaveAsFile()
          
    # Function to save file with a new name
    def SaveAsFile():
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(editor.get('1.0', tk.END))
            global current_file
            current_file = file_path
            with open(file_path, 'rb') as f:    
                coding = chardet.detect(f.read())['encoding']

            exe.update_status_bar(current_file)
            combo_var.set(coding.upper())


# Function to run the code
    def RunCode():
        code = editor.get('1.0', tk.END)
        try:
        # 将代码保存到一个临时文件
            with open('temp_script.py', 'w', encoding='utf-8') as file:
                file.write(code)
        
        # 打开命令行窗口并运行临时文件
            exec(code)
        except Exception as e:
            messagebox.showerror("错误", f"发生错误：\n{type(e).__name__}:{e}")


# Function to confirm and handle window close event
    def CloseWindow():
        if editor.edit_modified():
            result = messagebox.askyesnocancel("警告", "您有未保存的更改。是否保存？")
            if result is None:
                return  # User clicked "Cancel," do nothing
            elif result:
                hotkey.SaveFile()  # User clicked "Yes," save the file
        root.destroy()

    def edit_cut():
        editor.event_generate("<<Cut>>")
    def edit_copy():
        editor.event_generate("<<Copy>>")
    def edit_paste():
        editor.event_generate("<<Paste>>")
combo_var = tk.StringVar()
root.protocol("WM_DELETE_WINDOW", hotkey.CloseWindow)

class exe:
    # Function to update the status bar
    def update_status_bar(file_path):
        status_bar.config(text=f"当前文件：{file_path}")

    def highlight_syntax(event=None):
        text = editor.get("1.0", "end-1c")  # 获取文本框中的所有内容



# Menu Bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="文件", menu=file_menu)
file_menu.add_command(label="新建", command=hotkey.NewFile,accelerator="Ctrl+N")
file_menu.add_command(label="打开", command=hotkey.OpenFile,accelerator="Ctrl+O")
file_menu.add_command(label="保存", command=hotkey.SaveFile,accelerator="Ctrl+S")
file_menu.add_command(label="另存为", command=hotkey.SaveAsFile,accelerator="Ctrl+Shift+S")
file_menu.add_separator()
file_menu.add_command(label="退出", command=hotkey.CloseWindow,accelerator="Ctrl+Q")

# Edit Menu (same as before)
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="编辑", menu=edit_menu)
edit_menu.add_command(label="剪切", command=hotkey.edit_cut,accelerator="Ctrl+X")
edit_menu.add_command(label="复制", command=hotkey.edit_copy,accelerator="Ctrl+C")
edit_menu.add_command(label="粘贴", command=hotkey.edit_paste,accelerator="Ctrl+V")

code = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="代码", menu=code)
code.add_command(label="运行", command=hotkey.RunCode,accelerator="Ctrl+R")


editor = tk.Text(root,  wrap="none", font=custom_font)
editor.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
scrollbarx = tk.Scrollbar(editor,orient="horizontal")
scrollbary = tk.Scrollbar(editor)
scrollbary.config(command=editor.yview)
editor.config(yscrollcommand=scrollbary.set)

scrollbarx.config(command=editor.xview)
editor.config(xscrollcommand=scrollbarx.set)

scrollbary.pack(side="right", fill="y")
scrollbarx.pack(side="bottom", fill="x")

# Status Bar
status_bar = ttk.Label(root, text="")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

encoding = ttk.Combobox(status_bar,values=[
                                    "UTF-8", 
                                    "ASCII",
                                    "GBK",
                                    "BIG5"],textvariable=combo_var).pack(side=tk.BOTTOM,anchor=tk.SE)
tk.Label(status_bar,text='编码').pack(side=tk.BOTTOM,anchor=tk.E)
exe.update_status_bar("无")

root.bind_all("<Control-n>", lambda event: hotkey.NewFile)
root.bind_all("<Control-o>", lambda event: hotkey.OpenFile())
root.bind_all("<Control-s>", lambda event: hotkey.SaveFile())
root.bind_all("<Control-S>", lambda event: hotkey.SaveAsFile())
root.bind_all("<Control-x>", lambda event: hotkey.edit_cut())
root.bind_all("<Control-c>", lambda event: hotkey.edit_copy())
root.bind_all("<Control-q>", lambda event: hotkey.CloseWindow())
root.bind_all("<Control-r>", lambda event: hotkey.RunCode())

scrollbarx.config(bg="gray20", troughcolor="gray20")
scrollbary.config(bg="gray20", troughcolor="gray20")

def highlight_syntax(event=None):
    code = editor.get("1.0", "end-1c")

    # 清除之前的标记
    editor.tag_remove("keyword", "1.0", "end")
    editor.tag_remove("string", "1.0", "end")
    editor.tag_remove("comment", "1.0", "end")

    # 定义语法高亮规则
    keywords1 = [
     'int', 'float', 'long', 'complex', 'str', 'unicode',
    'list', 'tuple', 'bytearray', 'buffer',
    'xrange', 'set', 'frozenset', 'dict', 'bool'
    ]
    keyword_pattern1 = r'\b(' + '|'.join(keywords1) + r')\b'

    # 第二个关键字分组
    keywords2 = [
    'True', 'False', 'None', 'self', 'NotImplemented', 'Ellipsis',
    '__debug__', '__file__', 'and', 'del', 'from', 'not', 'while',
    'as', 'elif', 'global', 'or', 'with', 'assert', 'else', 'if',
    'pass', 'yield', 'break', 'except', 'import', 'print', 'class',
    'exec', 'in', 'raise', 'continue', 'finally', 'is', 'return',
    'def', 'for', 'lambda', 'try'
    ]
    keyword_pattern2 = r'\b(' + '|'.join(keywords2) + r')\b'

    keywords3 = [
    'ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException',
    'DeprecationWarning', 'EnvironmentError', 'EOFError', 'Exception',
    'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError',
    'ImportError', 'ImportWarning', 'IndexError', 'KeyError',
    'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError',
    'NotImplementedError', 'OSError', 'OverflowError',
    'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError',
    'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError',
    'SyntaxWarning', 'SystemError', 'SystemExit', 'TypeError',
    'UnboundLocalError', 'UserWarning', 'UnicodeError',
    'UnicodeWarning', 'UnicodeEncodeError', 'UnicodeDecodeError',
    'UnicodeTranslateError', 'ValueError', 'Warning', 'WindowsError',
    'ZeroDivisionError'
    ]
    keyword_pattern3 = r'\b(' + '|'.join(keywords3) + r')\b'

    string_pattern = r'("(\"|\\.|[^\"\n])*")|(\'(\'|\\.|[^\'\n])*\')'

    comment_pattern = r'#.*'

    # 应用语法高亮
    apply_highlight("keyword1", keyword_pattern1, code)
    apply_highlight("keyword2", keyword_pattern2, code)
    apply_highlight("keyword3", keyword_pattern3, code)
    apply_highlight("string", string_pattern, code)
    apply_highlight("comment", comment_pattern, code)

def apply_highlight(tag, pattern, code):
    matches = re.finditer(pattern, code)
    for match in matches:
        start = "1.0 + {} chars".format(match.start())
        end = "1.0 + {} chars".format(match.end())
        editor.tag_add(tag, start, end)
editor.bind("<KeyRelease>", highlight_syntax)


editor.tag_configure("keyword1", foreground="#808000")
editor.tag_configure("keyword2", foreground="#0033B3")
editor.tag_configure("keyword3", foreground="#800000")
editor.tag_configure("string", foreground="green")
editor.tag_configure("comment", foreground="gray")

root.mainloop()

