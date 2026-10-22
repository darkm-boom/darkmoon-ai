import customtkinter as ctk

from tkinter import filedialog
from pathlib import Path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DarkMoonAI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DarkMoon AI")
        self.geometry("850x550")
        self.minsize(650, 450)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            self,
            text="DarkMoon AI",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20)

        self.output = ctk.CTkTextbox(self, font=("Arial", 15))
        self.output.grid(
            row=1, column=0, padx=20, pady=10, sticky="nsew"
        )
        self.output.insert(
            "1.0",
            "Welcome to DarkMoon AI!\n\n"
            "Your personal desktop assistant starts here.\n"
            "Next: file search and document reading."
        )

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text="Type a command..."
        )
        self.entry.grid(
            row=2, column=0, padx=20, pady=10, sticky="ew"
        )
        self.entry.bind("<Return>", self.handle_command)

        self.search_button = ctk.CTkButton(
        self,
            text="Search Files",
            command=self.choose_folder
        )
        self.search_button.grid(
            row=3, column=0, padx=20, pady=5
        )    

        
        self.read_button = ctk.CTkButton(
            self,
            text="Read Document",
            command=self.read_document
        )
        self.read_button.grid(
            row=5, column=0, padx=20, pady=5
        )

        
        self.summarize_button = ctk.CTkButton(
            self,
            text="Summarize Text",
            command=self.summarize_document
        )
        self.summarize_button.grid(
            row=6, column=0, padx=20, pady=5
        )

        
        self.button = ctk.CTkButton(
            self, text="Run", command=self.handle_command
        )
        self.button.grid(row=4, column=0, padx=20, pady=(0, 20))

    
    def choose_folder(self):
        folder = filedialog.askdirectory(
            title="Choose a folder to search"
        )

        if not folder:
            return

        self.output.insert(
            "end", f"\n\nSearching folder: {folder}\n"
        )

        files = list(Path(folder).rglob("*"))

        self.output.insert(
            "end", f"Found {len(files)} items in this folder.\n"
        )

        for file in files[:30]:
            if file.is_file():
                self.output.insert("end", f"📄 {file.name}\n")

        self.output.see("end")

    
    
    def read_document(self):
        filename = filedialog.askopenfilename(
            title="Choose a text document",
            filetypes=[("Text files", "*.txt")]
        )

        if not filename:
            return

        try:
            content = Path(filename).read_text(
                encoding="utf-8",
                errors="replace"
            )

            self.output.insert(
                "end",
                f"\n\n--- {Path(filename).name} ---\n"
            )
            self.output.insert("end", content + "\n")
            self.output.see("end")

        except OSError as error:
            self.output.insert(
                "end", f"\nCould not read file: {error}\n"
            )

    
    def summarize_text(self, text, max_sentences=3):
        import re

        sentences = re.split(
            r'(?<=[.!?])\s+', text.strip()
        )
        sentences = [s for s in sentences if s]

        if len(sentences) <= max_sentences:
            return "\n".join(sentences)

        words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        stop_words = {
            "the", "and", "for", "are", "was", "were",
            "this", "that", "with", "from", "have",
            "has", "had", "you", "your", "but", "not"
        }

        frequencies = {}
        for word in words:
            if word not in stop_words:
                frequencies[word] = frequencies.get(word, 0) + 1

        scored = []
        for index, sentence in enumerate(sentences):
            terms = re.findall(
                r"\b[a-zA-Z]{3,}\b", sentence.lower()
            )
            score = sum(
                frequencies.get(word, 0)
                for word in terms if word not in stop_words
            )
            scored.append((score, index, sentence))

        best = sorted(
            scored, key=lambda item: item[0], reverse=True
        )[:max_sentences]

        best.sort(key=lambda item: item[1])
        return "\n".join(item[2] for item in best)

    
    def summarize_document(self):
        filename = filedialog.askopenfilename(
            title="Choose a document to summarize",
            filetypes=[("Text files", "*.txt")]
        )

        if not filename:
            return

        try:
            content = Path(filename).read_text(
                encoding="utf-8", errors="replace"
            )

            if not content.strip():
                self.output.insert(
                    "end", "\nThis document is empty.\n"
                )
                return

            summary = self.summarize_text(content)

            self.output.insert(
                "end",
                f"\n\n--- Summary: {Path(filename).name} ---\n"
            )
            self.output.insert("end", summary + "\n")
            self.output.see("end")

        except OSError as error:
            self.output.insert(
                "end", f"\nCould not summarize file: {error}\n"
            )

    
    def handle_command(self, event=None):
        command = self.entry.get().strip()

        if not command:
            return

        self.output.insert("end", f"\n\nYou: {command}\n")
        self.output.insert(
            "end",
            "DarkMoon AI: I received your command. "
            "More abilities are coming next."
        )
        self.output.see("end")
        self.entry.delete(0, "end")


if __name__ == "__main__":
    app = DarkMoonAI()
    app.mainloop()
