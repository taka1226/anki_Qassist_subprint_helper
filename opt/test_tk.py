import tkinter as tk

root = tk.Tk()
root.geometry("1000x700")
root.title("タイトル")

# label1 = tk.Label(root, text="aa", foreground='#ff0000', background='#ffaacc')
# label1.pack()

# ボタン作成
btn = tk.Button(root, text='終了')
# 配置
btn.pack(fill = 'x', padx=30)

root.mainloop()
