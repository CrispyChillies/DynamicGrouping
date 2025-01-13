import sys
import random
import csv
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QWidget,
    QMessageBox,
    QProgressBar,
    QRadioButton,
    QButtonGroup,
    QFileDialog,
)


class GroupingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Dynamic Grouping with Multiple Randomization")
        self.setGeometry(100, 100, 600, 700)

        # Main layout
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        self.layout = QVBoxLayout()
        centralWidget.setLayout(self.layout)

        # Title
        self.label_title = QLabel(
            "Enter each member's name below. Press Enter to add a new name:"
        )
        self.layout.addWidget(self.label_title)

        # Dynamic input area for names
        self.name_inputs = QVBoxLayout()
        self.layout.addLayout(self.name_inputs)

        # Add the first input box
        self.add_new_input()

        # Grouping options
        self.label_options = QLabel("Choose grouping method:")
        self.layout.addWidget(self.label_options)

        self.grouping_option = QButtonGroup(self)
        self.radio_groups = QRadioButton("Number of Groups")
        self.radio_students = QRadioButton("Number of Students per Group")
        self.radio_groups.setChecked(True)
        self.grouping_option.addButton(self.radio_groups)
        self.grouping_option.addButton(self.radio_students)
        self.layout.addWidget(self.radio_groups)
        self.layout.addWidget(self.radio_students)

        # Input for groups or students
        self.label_groups = QLabel("Enter number:")
        self.layout.addWidget(self.label_groups)

        self.input_groups = QLineEdit()
        self.layout.addWidget(self.input_groups)

        # Input for number of randomizations
        self.label_iterations = QLabel("Enter the number of randomizations:")
        self.layout.addWidget(self.label_iterations)

        self.input_iterations = QLineEdit()
        self.layout.addWidget(self.input_iterations)

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.layout.addWidget(self.output_area)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        # Buttons
        self.button_generate = QPushButton("Start Randomizing")
        self.button_generate.clicked.connect(self.start_randomization)
        self.layout.addWidget(self.button_generate)

        self.button_import_csv = QPushButton("Import Members from CSV")
        self.button_import_csv.clicked.connect(self.import_members_from_csv)
        self.layout.addWidget(self.button_import_csv)

        self.button_reset = QPushButton("Reset Dataset")
        self.button_reset.clicked.connect(self.reset_dataset)
        self.layout.addWidget(self.button_reset)

    def add_new_input(self):
        input_box = QLineEdit()
        input_box.returnPressed.connect(self.handle_input_returned)
        self.name_inputs.addWidget(input_box)

    def handle_input_returned(self):
        sender = self.sender()
        self.add_new_input()
        next_input = self.name_inputs.itemAt(self.name_inputs.count() - 1).widget()
        next_input.setFocus()

    def get_all_names(self):
        names = []
        for i in range(self.name_inputs.count()):
            input_box = self.name_inputs.itemAt(i).widget()
            if input_box and input_box.text().strip():
                names.append(input_box.text().strip())
        return names

    def start_randomization(self):
        try:
            self.members = self.get_all_names()
            if not self.members:
                raise ValueError("Please enter at least one member.")

            # Validate duplicates
            if len(self.members) != len(set(self.members)):
                raise ValueError(
                    "Duplicate names detected. Please ensure all names are unique."
                )

            # Determine grouping method
            if self.radio_groups.isChecked():
                self.grouping_method = "groups"
                self.grouping_value = int(self.input_groups.text())
                if self.grouping_value > len(self.members):
                    raise ValueError(
                        "Number of groups cannot exceed the number of members."
                    )
            else:
                self.grouping_method = "students"
                self.grouping_value = int(self.input_groups.text())
                if self.grouping_value <= 0:
                    raise ValueError("Number of students per group must be positive.")

            # Get number of randomizations
            self.iterations = int(self.input_iterations.text())
            if self.iterations <= 0:
                raise ValueError("Number of randomizations must be positive.")

            # Initialize progress bar
            self.progress_bar.setMaximum(self.iterations)
            self.progress_bar.setValue(0)

            # Reset and start randomization
            self.current_iteration = 0
            self.output_area.clear()
            self.timer = QTimer()
            self.timer.timeout.connect(self.perform_next_randomization)
            self.timer.start(2000)  # 2-second interval

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def perform_next_randomization(self):
        if self.current_iteration < self.iterations:
            self.current_iteration += 1
            self.progress_bar.setValue(self.current_iteration)
            self.output_area.append(f"Randomization {self.current_iteration}:")

            # Perform grouping
            random.shuffle(self.members)
            if self.grouping_method == "groups":
                groups = self.group_by_groups(self.members, self.grouping_value)
            else:
                groups = self.group_by_students(self.members, self.grouping_value)

            # Display results
            for i, group in enumerate(groups, start=1):
                self.output_area.append(f"  Group {i}: {', '.join(group)}")
            self.output_area.append("\n")
        else:
            self.timer.stop()
            self.output_area.append("Randomization complete!")
            self.progress_bar.setValue(self.iterations)

    def group_by_groups(self, members, num_groups):
        groups = [[] for _ in range(num_groups)]
        for i, member in enumerate(members):
            groups[i % num_groups].append(member)
        return groups

    def group_by_students(self, members, students_per_group):
        return [
            members[i : i + students_per_group]
            for i in range(0, len(members), students_per_group)
        ]

    def import_members_from_csv(self):
        try:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getOpenFileName(
                self,
                "Import Members from CSV",
                "",
                "CSV Files (*.csv);;All Files (*)",
                options=options,
            )
            if not file_name:
                return  # User canceled

            with open(file_name, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                if "Name" not in reader.fieldnames:
                    raise ValueError("CSV must have a 'Name' column.")

                for row in reader:
                    name = row["Name"].strip()
                    if name:
                        self.add_member_to_ui(name)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import CSV: {e}")

    def add_member_to_ui(self, name):
        input_box = QLineEdit()
        input_box.setText(name)
        input_box.returnPressed.connect(self.handle_input_returned)
        self.name_inputs.addWidget(input_box)

    def reset_dataset(self):
        # Remove all input boxes
        while self.name_inputs.count():
            item = self.name_inputs.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Add a fresh input box
        self.add_new_input()

        # Clear input fields
        self.input_groups.clear()
        self.input_iterations.clear()

        # Clear output area
        self.output_area.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = GroupingApp()
    mainWindow.show()
    sys.exit(app.exec_())
