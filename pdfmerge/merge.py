from csv import reader
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from tkinterdnd2 import DND_FILES, TkinterDnD

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))

class PdfMergeApp:
    def __init__(self, root: TkinterDnD.Tk) -> None:
        self.root = root
        self.root.title("PDF結合")
        self.root.geometry("700x500")

        self.pdf_files: list[Path] = []

        title_label = tk.Label(
            root,
            text=f"PDFを結合したい順番にドロップしてください",
            font=("", 14),
        )
        title_label.pack(pady=(15, 5))

        note_label = tk.Label(
            root,
            text="ドロップした順番で上から並びます",
        )
        note_label.pack(pady=(0, 10))

        self.drop_frame = tk.Frame(
            root,
            relief="groove",
            borderwidth=2,
        )
        self.drop_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5,
        )

        self.listbox = tk.Listbox(
            self.drop_frame,
            selectmode=tk.SINGLE,
            font=("", 11),
        )
        self.listbox.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0),
            pady=10,
        )

        scrollbar = tk.Scrollbar(
            self.drop_frame,
            orient="vertical",
            command=self.listbox.yview,
        )
        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 10),
            pady=10,
        )

        self.listbox.configure(yscrollcommand=scrollbar.set)

        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind("<<Drop>>", self.on_drop)

        button_frame = tk.Frame(root)
        button_frame.pack(fill="x", padx=15, pady=10)

        tk.Button(
            button_frame,
            text="上へ",
            width=10,
            command=self.move_up,
        ).pack(side="left", padx=3)

        tk.Button(
            button_frame,
            text="下へ",
            width=10,
            command=self.move_down,
        ).pack(side="left", padx=3)

        tk.Button(
            button_frame,
            text="選択削除",
            width=10,
            command=self.remove_selected,
        ).pack(side="left", padx=3)

        tk.Button(
            button_frame,
            text="すべて削除",
            width=10,
            command=self.clear_all,
        ).pack(side="left", padx=3)

        tk.Button(
            button_frame,
            text="結合して保存",
            width=15,
            command=self.merge_pdfs,
        ).pack(side="right", padx=3)

    def on_drop(self, event) -> None:
        dropped_items = self.root.tk.splitlist(event.data)

        added_count = 0

        for item in dropped_items:
            path = Path(item)

            if path.suffix.lower() != ".pdf":
                continue

            if not path.exists():
                continue

            self.pdf_files.append(path)
            added_count += 1

        if added_count == 0:
            messagebox.showwarning(
                "PDFがありません",
                "PDFファイルをドロップしてください。",
            )

        self.refresh_list()

    def refresh_list(self) -> None:
        self.listbox.delete(0, tk.END)

        for index, path in enumerate(self.pdf_files, start=1):
            self.listbox.insert(
                tk.END,
                f"{index:02d}. {path.name}",
            )

    def move_up(self) -> None:
        selection = self.listbox.curselection()

        if not selection:
            return

        index = selection[0]

        if index == 0:
            return

        self.pdf_files[index - 1], self.pdf_files[index] = (
            self.pdf_files[index],
            self.pdf_files[index - 1],
        )

        self.refresh_list()
        self.listbox.selection_set(index - 1)
        self.listbox.activate(index - 1)

    def move_down(self) -> None:
        selection = self.listbox.curselection()

        if not selection:
            return

        index = selection[0]

        if index >= len(self.pdf_files) - 1:
            return

        self.pdf_files[index + 1], self.pdf_files[index] = (
            self.pdf_files[index],
            self.pdf_files[index + 1],
        )

        self.refresh_list()
        self.listbox.selection_set(index + 1)
        self.listbox.activate(index + 1)

    def remove_selected(self) -> None:
        selection = self.listbox.curselection()

        if not selection:
            return

        index = selection[0]
        del self.pdf_files[index]

        self.refresh_list()

    def clear_all(self) -> None:
        self.pdf_files.clear()
        self.refresh_list()

    def merge_pdfs(self) -> None:
        if not self.pdf_files:
            messagebox.showwarning(
                "PDFがありません",
                "結合するPDFをドロップしてください。",
            )
            return

        output_path = filedialog.asksaveasfilename(
            title="結合したPDFの保存先",
            defaultextension=".pdf",
            filetypes=[("PDFファイル", "*.pdf")],
            initialfile="結合済み.pdf",
        )

        if not output_path:
            return

        writer = PdfWriter()

        try:
            for pdf_path in self.pdf_files:
                reader = PdfReader(pdf_path)

                for page in reader.pages:
                    overlay = create_overlay(
                        pdf_path.name,
                        float(page.mediabox.width),
                        float(page.mediabox.height),
                    )

                    page.merge_page(overlay)
                    writer.add_page(page)
        
            with open(output_path, "wb") as output_file:
                writer.write(output_file)

        except Exception as error:
            messagebox.showerror(
                "結合エラー",
                f"PDFを結合できませんでした。\n\n{error}",
            )
            return

        finally:
            writer.close()

        messagebox.showinfo(
            "完了",
            f"PDFを結合しました。\n\n{output_path}",
        )

def create_overlay(filename: str, width, height):
    buffer = BytesIO()

    c = canvas.Canvas(buffer, pagesize=(width, height))
    c.setFont("HeiseiKakuGo-W5", 9)

    # 左上（余白20pt）
    c.drawString(20, height - 20, filename)

    c.save()

    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def main() -> None:
    root = TkinterDnD.Tk()
    PdfMergeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
