import sys
import csv
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QSpinBox, QScrollArea,
    QFrame, QMessageBox, QTabWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

CSV_FILE = "books.csv"
CSV_FIELDS = ["title", "author", "priority", "category", "date_added"]


def load_books():
    books = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["priority"] = int(row["priority"])
                books.append(row)
    return books


def save_books(books):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(books)


def sort_books(books, category):
    filtered = [b for b in books if b["category"] == category]
    # Sort by priority descending (5 = most urgent first), then date ascending
    filtered.sort(key=lambda b: (-b["priority"], b["date_added"]))
    return filtered


CATEGORY_LABELS = {
    "tbr": "To Be Read",
    "current": "Currently Reading",
    "completed": "Completed"
}

PRIORITY_COLORS = {
    5: "#e70049",
    4: "#e62298",
    3: "#fb67e5",
    2: "#d175ef",
    1: "#ab85dc"
}


class BookCard(QFrame):
    def __init__(self, book, on_delete, on_move):
        super().__init__()
        self.book = book
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background: #230142;
                border-radius: 6px;
                border: 1px solid #51fcf4;
                margin: 2px 4px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)

        # Priority badge
        priority_label = QLabel(f"P{book['priority']}")
        priority_label.setFixedWidth(30)
        priority_label.setAlignment(Qt.AlignCenter)
        color = PRIORITY_COLORS.get(book["priority"], "#e9b3ff")
        priority_label.setStyleSheet(f"""
            background: {color};
            color: white;
            border-radius: 4px;
            font-weight: bold;
            font-size: 11px;
            padding: 2px;
        """)
        layout.addWidget(priority_label)

        # Book info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(1)

        title_label = QLabel(book["title"])
        title_label.setStyleSheet("color: #f0f0f0; font-weight: bold; font-size: 13px; border: none;")
        info_layout.addWidget(title_label)

        author_label = QLabel(f"by {book['author']}")
        author_label.setStyleSheet("color: #aaa; font-size: 11px; border: none;")
        info_layout.addWidget(author_label)

        date_label = QLabel(f"Added: {book['date_added'][:10]}")
        date_label.setStyleSheet("color: #666; font-size: 10px; border: none;")
        info_layout.addWidget(date_label)

        layout.addLayout(info_layout)
        layout.addStretch()

        # Move button (only show relevant moves)
        category = book["category"]
        if category != "current":
            move_btn = QPushButton("▶ Current")
            move_btn.setFixedWidth(90)
            move_btn.setStyleSheet(self._btn_style("#2980b9"))
            move_btn.clicked.connect(lambda: on_move(book, "current"))
            layout.addWidget(move_btn)

        if category != "completed":
            done_btn = QPushButton("✔ Done")
            done_btn.setFixedWidth(75)
            done_btn.setStyleSheet(self._btn_style("#7627ae"))
            done_btn.clicked.connect(lambda: on_move(book, "completed"))
            layout.addWidget(done_btn)

        if category != "tbr":
            tbr_btn = QPushButton("↩ TBR")
            tbr_btn.setFixedWidth(70)
            tbr_btn.setStyleSheet(self._btn_style("#8e44ad"))
            tbr_btn.clicked.connect(lambda: on_move(book, "tbr"))
            layout.addWidget(tbr_btn)

        # Delete button
        del_btn = QPushButton("🗑")
        del_btn.setFixedWidth(36)
        del_btn.setStyleSheet(self._btn_style("#c02ba7"))
        del_btn.clicked.connect(lambda: on_delete(book))
        layout.addWidget(del_btn)

    def _btn_style(self, color):
        return f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 6px;
                font-size: 11px;
            }}
            QPushButton:hover {{ background: #555; }}
        """


class BookListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✨ Book List ✨")
        self.setMinimumSize(700, 600)
        self.books = load_books()
        self._build_ui()
        self._refresh_all_tabs()

    def _build_ui(self):
        self.setStyleSheet("""
            QMainWindow { background: #1e1e1e; }
            QWidget { background: #1e1e1e; color: #f0f0f0; }
            QLineEdit, QSpinBox, QComboBox {
                background: #2c2c2c;
                color: #f0f0f0;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px;
                font-size: 13px;
            }
            QTabWidget::pane { border: 1px solid #444; border-radius: 4px; }
            QTabBar::tab {
                background: #2c2c2c;
                color: #aaa;
                padding: 8px 18px;
                border-radius: 4px 4px 0 0;
                margin-right: 2px;
            }
            QTabBar::tab:selected { background: #3a3a3a; color: #f0f0f0; font-weight: bold; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # ── Add book form ──
        form_frame = QFrame()
        form_frame.setStyleSheet("QFrame { background: #252525; border-radius: 8px; border: 1px solid #444; }")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(12, 10, 12, 10)
        form_layout.setSpacing(8)

        form_title = QLabel("Add a New Book")
        form_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #e0e0e0; border: none;")
        form_layout.addWidget(form_title)

        row1 = QHBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Book title...")
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Author name...")
        row1.addWidget(self.title_input, 3)
        row1.addWidget(self.author_input, 2)
        form_layout.addLayout(row1)

        row2 = QHBoxLayout()

        priority_label = QLabel("Priority (1–5):")
        priority_label.setStyleSheet("border: none; color: #ccc; font-size: 12px;")
        self.priority_spin = QSpinBox()
        self.priority_spin.setRange(1, 5)
        self.priority_spin.setValue(3)
        self.priority_spin.setFixedWidth(60)

        category_label = QLabel("Category:")
        category_label.setStyleSheet("border: none; color: #ccc; font-size: 12px;")
        self.category_combo = QComboBox()
        for key, label in CATEGORY_LABELS.items():
            self.category_combo.addItem(label, key)

        add_btn = QPushButton("＋ Add Book")
        add_btn.setStyleSheet("""
            QPushButton {
                background: #2980b9; color: white; border: none;
                border-radius: 5px; padding: 7px 16px; font-size: 13px; font-weight: bold;
            }
            QPushButton:hover { background: #3498db; }
        """)
        add_btn.clicked.connect(self._add_book)

        row2.addWidget(priority_label)
        row2.addWidget(self.priority_spin)
        row2.addSpacing(12)
        row2.addWidget(category_label)
        row2.addWidget(self.category_combo)
        row2.addStretch()
        row2.addWidget(add_btn)
        form_layout.addLayout(row2)

        main_layout.addWidget(form_frame)

        # ── Tabs ──
        self.tabs = QTabWidget()
        self.tab_widgets = {}
        self.scroll_areas = {}

        for key, label in CATEGORY_LABELS.items():
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)
            tab_layout.setContentsMargins(0, 8, 0, 0)

            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("QScrollArea { border: none; }")

            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setAlignment(Qt.AlignTop)
            container_layout.setSpacing(6)

            scroll.setWidget(container)
            tab_layout.addWidget(scroll)

            self.tabs.addTab(tab, label)
            self.tab_widgets[key] = container_layout
            self.scroll_areas[key] = scroll

        main_layout.addWidget(self.tabs)

        # ── Save button ──
        save_btn = QPushButton("Save")
        save_btn.setFixedHeight(38)
        save_btn.setStyleSheet("""
            QPushButton {
                background: #27ae60; color: white; border: none;
                border-radius: 5px; font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background: #2ecc71; }
        """)
        save_btn.clicked.connect(self._save)
        main_layout.addWidget(save_btn)

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _refresh_all_tabs(self):
        for key in CATEGORY_LABELS:
            self._refresh_tab(key)

    def _refresh_tab(self, category):
        layout = self.tab_widgets[category]
        self._clear_layout(layout)

        sorted_books = sort_books(self.books, category)
        if not sorted_books:
            empty = QLabel("No books here yet.")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("color: #666; font-size: 13px; padding: 20px;")
            layout.addWidget(empty)
        else:
            for book in sorted_books:
                card = BookCard(book, self._delete_book, self._move_book)
                layout.addWidget(card)

    def _add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        if not title or not author:
            QMessageBox.warning(self, "Missing Info", "Please enter both a title and an author.")
            return

        book = {
            "title": title,
            "author": author,
            "priority": self.priority_spin.value(),
            "category": self.category_combo.currentData(),
            "date_added": datetime.now().isoformat()
        }
        self.books.append(book)
        self._refresh_all_tabs()
        self.title_input.clear()
        self.author_input.clear()
        self.priority_spin.setValue(3)

        # Switch to the tab of the added book
        keys = list(CATEGORY_LABELS.keys())
        self.tabs.setCurrentIndex(keys.index(book["category"]))

    def _delete_book(self, book):
        reply = QMessageBox.question(
            self, "Delete Book",
            f'Are you sure you want to delete "{book["title"]}"?',
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.books.remove(book)
            self._refresh_all_tabs()

    def _move_book(self, book, new_category):
        book["category"] = new_category
        self._refresh_all_tabs()
        keys = list(CATEGORY_LABELS.keys())
        self.tabs.setCurrentIndex(keys.index(new_category))

    def _save(self):
        save_books(self.books)
        QMessageBox.information(self, "Saved", "Your book list has been saved!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = BookListApp()
    window.show()
    sys.exit(app.exec_())