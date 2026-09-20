import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path


class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №1")
        self.root.geometry("900x650")

        self.image = None

        toolbar = tk.Frame(root)
        toolbar.pack(fill="x", padx=10, pady=10)

        tk.Button(
            toolbar,
            text="Открыть",
            width=14,
            command=self.open_image
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar,
            text="Обработать",
            width=14,
            command=self.process_image
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar,
            text="Сохранить",
            width=14,
            command=self.save_image
        ).pack(side="left", padx=5)

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.canvas.bind("<Configure>", lambda event: self.redraw())

     

    def open_image(self):
        filename = filedialog.askopenfilename(
            title="Открыть изображение",
            filetypes=[
                ("PNG", "*.png"),
                ("GIF", "*.gif"),
                ("PPM", "*.ppm"),
                ("PGM", "*.pgm"),
                ("Все файлы", "*.*")
            ]
        )

        if not filename:
            return

        try:
            self.image = tk.PhotoImage(file=filename)
            self.redraw()
        except tk.TclError as error:
            messagebox.showerror(
                "Ошибка",
                "Не удалось открыть изображение.\n\n"
                f"{error}"
            )

    def process_image(self):
        if self.image is None:
            messagebox.showwarning(
                "Нет изображения",
                "Сначала откройте изображение."
            )
            return

        width = self.image.width()
        height = self.image.height()

     
        self.image.put("#000040", (0, 0))
        self.image.put("#404000", (0, height // 2))
        self.image.put("#400040", (width // 2, height - 1))
        self.redraw()

    def save_image(self):
        if self.image is None:
            messagebox.showwarning(
                "Нет изображения",
                "Сначала откройте изображение."
            )
            return

        filename = filedialog.asksaveasfilename(
            title="Сохранить изображение",
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("GIF", "*.gif"),
                ("PPM", "*.ppm")
            ]
        )

        if not filename:
            return

        suffix = Path(filename).suffix.lower()

        if suffix == ".gif":
            image_format = "gif"
        elif suffix == ".ppm":
            image_format = "ppm"
        else:
            if suffix != ".png":
                filename += ".png"
            image_format = "png"

        try:
            self.image.write(filename, format=image_format)
            messagebox.showinfo(
                "Готово",
                "Изображение успешно сохранено."
            )
        except tk.TclError as error:
            messagebox.showerror(
                "Ошибка сохранения",
                str(error)
            )

    def redraw(self):
        self.canvas.delete("all")

        if self.image is None:
            self.canvas.create_text(
                max(self.canvas.winfo_width() // 2, 1),
                max(self.canvas.winfo_height() // 2, 1),
                text="Откройте изображение",
                fill="gray",
                font=("Arial", 14)
            )
            return

        self.canvas.create_image(
            max(self.canvas.winfo_width() // 2, 1),
            max(self.canvas.winfo_height() // 2, 1),
            image=self.image,
            anchor="center"
        )


def main():
    root = tk.Tk()
    ImageApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
