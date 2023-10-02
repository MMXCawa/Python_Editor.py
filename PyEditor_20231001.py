'''
Python Editor.py
###############################
# Made by AchryFI and MMXCawa #
###############################
更新日志:
20231001:添加了信息，行列字符显示和将文件运行方式改为os.system
'''

import keyword
import os
import re
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog, messagebox, ttk

import chardet

root = tk.Tk()
combo_var = tk.StringVar()
root.title("Python Editor Version 1.1")
font_path = "./res/tk.ttf"
root.geometry("600x600")


default_size=11
size=default_size
custom_font = tkFont.Font(family="Consolas", size=size)

# Global variable to store the current file path
current_file = None

python_keywords = keyword.kwlist


class hotkey:#热键
    global file_path
    def Readwithencoding(encoding='utf8'):
        global current_file
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, 'r', encoding=encoding) as file:
                editor.delete('1.0', tk.END)
                editor.insert('1.0', file.read())
                current_file = file_path

    def NewFile():#新建文件
        editor.delete('1.0', tk.END)

    def OpenFile():#打开文件
        global current_file
        try:
            hotkey.Readwithencoding()
            exe.update_status_bar(current_file)
            highlight_syntax()
        except LookupError:
            hotkey.Readwithencoding('GBK')
        except Exception as e:
            messagebox.showerror("错误", f"发生错误：\n{type(e).__name__}:{e}")
    def SaveFile():

        global current_file
        if current_file:
            if combo_var != '':
                try:
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
            os.system('python temp_script.py')
        except Exception as e:
            messagebox.showerror("错误", f"发生错误：\n{type(e).__name__}:{e}")


# 关闭窗口
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
    def help_Info():
        print('Nope')

root.protocol("WM_DELETE_WINDOW", hotkey.CloseWindow)

class exe:
    # Function to update the status bar
    def update_status_bar(file_path):
        try:
            with open(file_path, 'rb') as f:    
                coding = chardet.detect(f.read())['encoding']
            status_bar.config(text="当前文件:{} | 编码:{}".format(file_path,coding))
        except FileNotFoundError:
            status_bar.config(text="当前文件:{} | 编码:utf-8".format(file_path))

    def update_status_bar2(Row,Col):
        status_bar2.config(text=f"Line {Row}, Column {Col} | 第{Row}行，第{Col}个字符")

    def highlight_syntax(event=None):
        combo_var = tk.StringVar()
        text = editor.get("1.0", "end-1c")  # 获取文本框中的所有内容

def get_current_line_number():
        cursor_pos = editor.index("insert")
        line_number = cursor_pos.split('.')[0]
        col = cursor_pos.split('.')[1]
        exe.update_status_bar2(line_number,col)

# 菜单栏...
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# 文件
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="文件", menu=file_menu)
file_menu.add_command(label="新建", command=hotkey.NewFile,accelerator="Ctrl+N")
file_menu.add_command(label="打开", command=hotkey.OpenFile,accelerator="Ctrl+O")
file_menu.add_command(label="保存", command=hotkey.SaveFile,accelerator="Ctrl+S")
file_menu.add_command(label="另存为", command=hotkey.SaveAsFile,accelerator="Ctrl+Shift+S")
file_menu.add_separator()
file_menu.add_command(label="退出", command=hotkey.CloseWindow,accelerator="Ctrl+Q")

#编辑[剪切复制粘贴等功能]
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="编辑", menu=edit_menu)
edit_menu.add_command(label="剪切", command=hotkey.edit_cut,accelerator="Ctrl+X")
edit_menu.add_command(label="复制", command=hotkey.edit_copy,accelerator="Ctrl+C")
edit_menu.add_command(label="粘贴", command=hotkey.edit_paste,accelerator="Ctrl+V")

code = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="代码", menu=code)
code.add_command(label="运行", command=hotkey.RunCode,accelerator="Ctrl+R")

help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="帮助", menu=help_menu)
help_menu.add_command(label="信息", command=hotkey.help_Info,accelerator="Ctrl+T")

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
status_bar2 = ttk.Label(root, text="")
status_bar2.pack(side=tk.TOP, fill=tk.X)
exe.update_status_bar("无")



root.bind_all("<Control-n>", lambda event: hotkey.NewFile)
root.bind_all("<Control-o>", lambda event: hotkey.OpenFile())
root.bind_all("<Control-s>", lambda event: hotkey.SaveFile())
root.bind_all("<Control-S>", lambda event: hotkey.SaveAsFile())
root.bind_all("<Control-x>", lambda event: hotkey.edit_cut())
root.bind_all("<Control-c>", lambda event: hotkey.edit_copy())
root.bind_all("<Control-q>", lambda event: hotkey.CloseWindow())
root.bind_all("<Control-r>", lambda event: hotkey.RunCode())
root.bind_all("<Control-t>", lambda event: hotkey.help_Acknowledgement())


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
editor.bind("<KeyRelease>", lambda event: get_current_line_number())
editor.bind("<Button-1>", lambda event: get_current_line_number())
editor.bind("<ButtonPress-1>", lambda event: get_current_line_number())
editor.bind("<ButtonRelease-1>", lambda event: get_current_line_number())

editor.tag_configure("keyword1", foreground="#808000")
editor.tag_configure("keyword2", foreground="#0033B3")
editor.tag_configure("keyword3", foreground="#800000")
editor.tag_configure("string", foreground="green")
editor.tag_configure("comment", foreground="gray")

root.mainloop()

