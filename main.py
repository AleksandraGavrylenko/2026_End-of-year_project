import sys
import csv
import os
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QSpinBox, QComboBox,
    QListWidget, QListWidgetItem, QMessageBox, QTabWidget
)

CSV_FILE = "books.csv"
CATEGORIES = ["tbr", "current", "completed"]
CATEGORY_NAMES = {"tbr": "To Be Read", "current": "Currently Reading", "completed": "Completed"}


# ---------- CSV helpers ----------

def load_books():
    books = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                row["priority"] = int(row["priority"])
                books.append(row)
    return books


def save_books(books):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "author", "priority", "category", "date_added"])
        writer.writeheader()
        writer.writerows(books)


# ---------- Main window ----------

class BookApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Book List")
        self.setMinimumSize(600, 500)
        self.books = load_books()

        # Central widget + main layout
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # --- Input area ---
        layout.addWidget(QLabel("Title:"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Author:"))
        self.author_input = QLineEdit()
        layout.addWidget(self.author_input)

        # Priority and category on one row
        row = QHBoxLayout()

        row.addWidget(QLabel("Priority (1-5):"))
        self.priority_spin = QSpinBox()
        self.priority_spin.setRange(1, 5)
        self.priority_spin.setValue(3)
        row.addWidget(self.priority_spin)

        row.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        for key in CATEGORIES:
            self.category_combo.addItem(CATEGORY_NAMES[key], key)
        row.addWidget(self.category_combo)

        layout.addLayout(row)

        add_btn = QPushButton("Add Book")
        add_btn.clicked.connect(self.add_book)
        layout.addWidget(add_btn)

        # --- Tabs (one per category) ---
        self.tabs = QTabWidget()
        self.list_widgets = {}  # key -> QListWidget

        for key in CATEGORIES:
            list_widget = QListWidget()
            self.list_widgets[key] = list_widget
            self.tabs.addTab(list_widget, CATEGORY_NAMES[key])

        layout.addWidget(self.tabs)

        # --- Bottom buttons ---
        btn_row = QHBoxLayout()

        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_book)
        btn_row.addWidget(delete_btn)

        move_btn = QPushButton("Move Selected To...")
        move_btn.clicked.connect(self.move_book)
        btn_row.addWidget(move_btn)

        self.move_target = QComboBox()
        for key in CATEGORIES:
            self.move_target.addItem(CATEGORY_NAMES[key], key)
        btn_row.addWidget(self.move_target)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save)
        btn_row.addWidget(save_btn)

        layout.addLayout(btn_row)

        self.refresh_all_tabs()

    # ---------- Helpers ----------

    def get_sorted(self, category):
        """Return books for a category sorted by priority (high first), then date."""
        filtered = [b for b in self.books if b["category"] == category]
        filtered.sort(key=lambda b: (-b["priority"], b["date_added"]))
        return filtered

    def refresh_all_tabs(self):
        for key in CATEGORIES:
            lw = self.list_widgets[key]
            lw.clear()
            for book in self.get_sorted(key):
                text = f"[P{book['priority']}]  {book['title']}  —  {book['author']}  (added {book['date_added'][:10]})"
                item = QListWidgetItem(text)
                item.setData(1000, book)   # store the dict on the item
                lw.addItem(item)

    def current_list_widget(self):
        """Return the QListWidget that is currently visible."""
        return self.tabs.currentWidget()

    # ---------- Actions ----------

    def add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()

        if not title or not author:
            QMessageBox.warning(self, "Missing info", "Please fill in both title and author.")
            return

        book = {
            "title": title,
            "author": author,
            "priority": self.priority_spin.value(),
            "category": self.category_combo.currentData(),
            "date_added": datetime.now().isoformat()
        }
        self.books.append(book)
        self.refresh_all_tabs()

        # Switch to the tab where the book was added
        self.tabs.setCurrentIndex(CATEGORIES.index(book["category"]))

        self.title_input.clear()
        self.author_input.clear()
        self.priority_spin.setValue(3)

    def delete_book(self):
        lw = self.current_list_widget()
        item = lw.currentItem()
        if item is None:
            QMessageBox.information(self, "Nothing selected", "Click a book first, then press Delete.")
            return

        book = item.data(1000)
        reply = QMessageBox.question(
            self, "Delete?",
            f"Delete \"{book['title']}\"?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.books.remove(book)
            self.refresh_all_tabs()

    def move_book(self):
        lw = self.current_list_widget()
        item = lw.currentItem()
        if item is None:
            QMessageBox.information(self, "Nothing selected", "Click a book first, then press Move.")
            return

        book = item.data(1000)
        new_cat = self.move_target.currentData()
        book["category"] = new_cat
        self.refresh_all_tabs()
        self.tabs.setCurrentIndex(CATEGORIES.index(new_cat))

    def save(self):
        save_books(self.books)
        QMessageBox.information(self, "Saved", "Books saved to books.csv!")


# ---------- Run ----------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookApp()
    window.show()
    sys.exit(app.exec_())