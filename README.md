# DynamicGrouping

DynamicGrouping is a Python application designed to help educators and organizers easily separate students or participants into groups. This app is particularly useful in school settings where it can be challenging to create balanced and randomized groups.

## Features

- **Dynamic Name Input**: Enter each member's name individually and press Enter to add a new name. This allows for easy and flexible input of participant names.
- **CSV Import**: Import member names from a CSV file with a single click. The CSV file should have a column named "Name".
- **Grouping Options**: Choose between grouping by the number of groups or the number of students per group.
- **Multiple Randomizations**: Specify the number of randomizations to perform, ensuring varied group compositions.
- **Progress Display**: A progress bar and animations build suspense during the grouping process.
- **Error Handling**: The app includes robust error handling to ensure valid input and prevent common mistakes like duplicate names or invalid group sizes.
- **Reset Functionality**: Easily reset the dataset to start over with new names or grouping criteria.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/DynamicGrouping.git
   ```
2. Navigate to the project directory:
   ```sh
   cd DynamicGrouping
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```sh
   python official.py
   ```
2. Enter each member's name in the input box and press Enter to add a new name.
3. Choose the grouping method (number of groups or number of students per group).
4. Enter the desired number of groups or students per group.
5. Specify the number of randomizations.
6. Click "Start Randomizing" to begin the grouping process.
7. Optionally, import member names from a CSV file by clicking "Import Members from CSV".
8. Reset the dataset at any time by clicking "Reset Dataset".

## Example CSV Format

To import members from a CSV file, ensure the file has the following format:

```csv
Name
Alice
Bob
Charlie
David
Eve
Frank
Grace
Hannah
Ivy
Jack
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or suggestions, please contact hailong552004@gmail.com.

---

Thank you for using DynamicGrouping! We hope it makes your group creation process easier and more efficient.
