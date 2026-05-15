# Marriage Predictor

A simple Python application that calculates or predicts marriage compatibility based on user input metrics.
Check your Lagna Kundali for the Venus, Jupiter, and Saturn placements. Your month and year of birth.

## Features

- Interactive command-line interface (CLI) for user data entry.
- Built-in conditional logic to determine custom prediction scores.
- Lightweight design running entirely inside a isolated Python environment.

## Prerequisites

- Python 3.13 or higher

## Getting Started

Follow these steps to set up and run the project locally on your machine.

### 1. Clone the Repository
```bash
git clone https://github.com
cd Marriage-Predictor
```

### 2. Set Up the Virtual Environment
Create a clean environment without bundled pip to avoid Windows installation hangs, then activate it:
```powershell
python -m venv venv --without-pip
.\venv\Scripts\activate
```

### 3. Restore Pip and Dependencies
```powershell
(New-Object System.Net.WebClient).DownloadFile('https://pypa.io', 'get-pip.py')
python get-pip.py
Remove-Item get-pip.py
pip install -r requirements.txt
```

### 4. Run the Script
```powershell
python main.py
```
