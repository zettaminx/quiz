import tkinter as tk
from tkinter import filedialog, messagebox

class SimpleNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("간단한 메모장")
        self.root.geometry("600x400")
        
        # 텍스트 영역
        self.text_area = tk.Text(self.root, undo=True, font=("Malgun Gothic", 12))
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # 메뉴바
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # 파일 메뉴
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="파일", menu=self.file_menu)
        self.file_menu.add_command(label="새로 만들기", command=self.new_file)
        self.file_menu.add_command(label="열기", command=self.open_file)
        self.file_menu.add_command(label="저장", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="종료", command=self.root.quit)
        
        self.current_file = None

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.root.title("간단한 메모장")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, content)
                self.current_file = file_path
                self.root.title(f"간단한 메모장 - {file_path}")
            except Exception as e:
                messagebox.showerror("오류", f"파일을 열 수 없습니다: {e}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo("성공", "파일이 저장되었습니다.")
            except Exception as e:
                messagebox.showerror("오류", f"파일을 저장할 수 없습니다: {e}")
        else:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(self.text_area.get(1.0, tk.END))
                    self.current_file = file_path
                    self.root.title(f"간단한 메모장 - {file_path}")
                    messagebox.showinfo("성공", "파일이 저장되었습니다.")
                except Exception as e:
                    messagebox.showerror("오류", f"파일을 저장할 수 없습니다: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    notepad = SimpleNotepad(root)
    root.mainloop()
