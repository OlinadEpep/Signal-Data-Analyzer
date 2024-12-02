# Signal Data Analyzer

**Signal Data Analyzer** is a Python-based application for visualizing and analyzing Signal messaging data. The application includes features for importing data, generating reports, and visualizing insights like message counts, word clouds, and timelines.

## Features

- **Data Import**: Load and process Signal data files (CSV or text).
- **Message Statistics**: View message counts by conversation.
- **Timeline Analysis**: Analyze message activity over time.
- **Word Clouds**: Visualize frequently used words in your messages.
- **Message Search**: Filter messages by text, date, conversation, or type.
- **Export to PDF**: Save filtered messages as a PDF report.
- **Database Extraction**: Extract Signal databases using pre-configured scripts.

## Requirements

- Python 3.7+
- Required Python packages:
  - `tkinter`
  - `pandas`
  - `matplotlib`
  - `wordcloud`
  - `reportlab`
  - `ttkthemes`
  - `pysqlcipher3`

## Install dependencies using:

```bash
pip install -r requirements.txt
```
## Usage 

```bash
Clone the repository:
git clone https://github.com/your-username/signal-data-analyzer.git
cd signal-data-analyzer
python sda.py
```
## License
This project is licensed under the MIT License. See the LICENSE file for details.
