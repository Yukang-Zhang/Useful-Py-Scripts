import re
# import numpy as np
import tkinter as tk

letter_dist_outside = [
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 2],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 2],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 2],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2],
    [1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 2],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 2, 1, 1],
    [1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2]
] # 两个字母之间除标准间隔的额外间隔数，单位为粗笔画宽度

#                           a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z
letter_dist_inside_small = [2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 3, 2, 1, 2, 2, 1, 1, 1, 2, 2, 2, 1, 2, 1] # 单个字母的粗笔画数量
letter_dist_inside_large = [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 2, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0] # 单个字母内的标准间隔数量
large_dist_inside =        [14,16,16,16,12,12,14,14,12,12,14,12,16,12,12,12,12,14,12,12,12,10,12,12,12,14] # 大写字母的宽度
small_dist_inside =        [4, 1, 1, 4, 1, 1, 4, 4, 1, 1, 4, 1, 7, 4, 1, 4, 4, 1, 1, 1, 4, 1, 4, 1, 4, 1]

small_dist = 1 # 粗笔画宽度
large_dist = 2 # 标准间隔宽度
space_dist = large_dist * 2 + small_dist # 空格宽度

example = "All work and no play makes Jack a dull boy."


test_list = list("abcdefghijklmnopqrstuvwxyz")
test_list = test_list + [i + j for i in test_list for j in test_list]
test_list = test_list + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
# print(test_list)



root = tk.Tk()
root.title("Engraver's Script单句长度估算器")


def calculate():
    example = input_textbox.get("1.0", tk.END)
    result = 0
    example_list = list(example)

    try:
        param1 = float(param1_entry.get())
    except ValueError:
        param1 = small_dist
    try:
        param2 = float(param2_entry.get())
    except ValueError:
        param2 = large_dist
    try:
        param3 = float(param3_entry.get())
    except ValueError:
        param3 = space_dist

    i = 0
    while True:
        if i == len(example_list):
            example_list.insert(i, str(int(result)))
            break
        elif example_list[i] == '\n':
            example_list.insert(i, str(int(result)))
            result = 0
            i += 1
        elif example_list[i] == ' ':
            example_list.insert(i, str(int(result)))
            result += param3
            i += 1
        elif example_list[i] >= 'a' and example_list[i] <= 'z':
            result += small_dist_inside[ord(example_list[i]) - ord('a')]
            if i > 0 and example_list[i - 1] >= 'a' and example_list[i - 1] <= 'z':
                result += (letter_dist_outside[ord(example_list[i - 1]) - ord('a')][ord(example_list[i]) - ord('a')] * param1 + param2)
        elif example_list[i] >= 'A' and example_list[i] <= 'Z':
            result += large_dist_inside[ord(example_list[i]) - ord('A')] * param1
        else:
            example_list.pop(i)
            continue
        i += 1

    example = "".join(example_list)
    output_textbox.config(state = "normal")
    output_textbox.delete("1.0", tk.END)
    output_textbox.insert(tk.END, example)
    output_textbox.config(state = "disabled")
    pass

def advanced_settings():
    advanced_settings_window = tk.Toplevel(root)
    advanced_settings_window.title("高级设置")

    text_widget = tk.Text(advanced_settings_window, height=10, width=40)
    text_widget.pack()
    
    
def readme():
    output = "在左边的文本框输入文段，可以换行\n除大小写字母，空格外的任何字符将被忽略\n输出将在每行的每个单词后（即每个空格前）输出一个数，表示这一行写到这个词大概有多长\n参数不填或填入非数字的话默认为1，2，5\n可以填入小数\n单位不重要，输出值是按比例的\n大写字母没有仔细地测量，估算可能不太准\n目前的估算长度在WAB的范本上似乎总是偏短5\u0025到10\u0025的样子，可以根据自己的结果稍加注意\n高级设置应该能够定义每两个字母之间的距离的每个字母的宽度，但是懒的写了"
    output_textbox.config(state = "normal")
    output_textbox.delete("1.0", tk.END)
    output_textbox.insert(tk.END, output)
    output_textbox.config(state = "disabled")


def placeholder():
    pass



def on_input_y_scroll(*args):
    input_textbox.yview(*args)

def on_input_x_scroll(*args):
    input_textbox.xview(*args)

def on_output_y_scroll(*args):
    output_textbox.yview(*args)

def on_output_x_scroll(*args):
    output_textbox.xview(*args)

menu_bar = tk.Menu(root)
menu_bar.add_command(label="计算", command = calculate)
menu_bar.add_command(label="高级设置", command = advanced_settings)
menu_bar.add_command(label="帮助", command = readme)
root.config(menu=menu_bar)

menu_bar.entryconfigure(2, state=tk.DISABLED)


input_label = tk.Label(root, text="在下面输入需要估算长度的句子或段落：")
input_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
input_textbox = tk.Text(root, height=10, width=40, wrap = "none")
input_textbox.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
input_textbox_scrollbar_x = tk.Scrollbar(root, orient="horizontal", command=on_input_x_scroll)
input_textbox_scrollbar_x.grid(row=2, column=0, sticky="ew")
input_textbox.config(xscrollcommand=input_textbox_scrollbar_x.set)



output_label = tk.Label(root, text="分行显示的估算结果：")
output_label.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
output_textbox = tk.Text(root, height=10, width=40, wrap = "none")
output_textbox.grid(row=1, column=1, padx=10, pady=5, sticky=tk.E)
output_textbox.config(state = "disabled")
output_textbox_scrollbar_x = tk.Scrollbar(root, orient="horizontal", command=on_output_x_scroll)
output_textbox_scrollbar_x.grid(row=2, column=1, sticky="ew")
output_textbox.config(xscrollcommand=output_textbox_scrollbar_x.set)


param1_label = tk.Label(root, text="输入小写字母'n'粗笔画的水平宽度:")
param1_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
param1_entry = tk.Entry(root)
param1_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
param1_label_1 = tk.Label(root, text="(mm)")
param1_label_1.grid(row=3, column=1, padx=10, pady=5, sticky=tk.E)

param2_label = tk.Label(root, text="输入小写字母'n'两个粗笔画内侧的水平距离:")
param2_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
param2_entry = tk.Entry(root)
param2_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
param2_label_1 = tk.Label(root, text="(mm)")
param2_label_1.grid(row=4, column=1, padx=10, pady=5, sticky=tk.E)

param3_label = tk.Label(root, text="输入一个空格的水平宽度:")
param3_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
param3_entry = tk.Entry(root)
param3_entry.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)
param3_label_1 = tk.Label(root, text="(mm)")
param3_label_1.grid(row=5, column=1, padx=10, pady=5, sticky=tk.E)

input_textbox.insert(tk.END, example)

root.mainloop()


