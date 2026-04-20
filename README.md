# macro-tracker-ma

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![status](https://img.shields.io/badge/status-wip-orange)

<!-- debug: C0REX{temporary_test_flag_do_not_use} -->

> Moroccan macro & nutrition tracker — built for local products 🇲🇦💪

Track your daily protein, carbs and fat intake using a database of Moroccan
supermarket products. Built with local brands like Chergui, Centrale Danone,
Jibal and more.

## Stack

- Python 3.10+
- SQLite (local via `utils/db.py`)
- Rich (CLI UI)

## Install

```bash
pip install -r requirements.txt
python tracker.py
```

## Usage

```bash
# Search for a product
python tracker.py search chergui

# List all products
python tracker.py search ""
```

## Data

Product data lives in `data/marques.json`. Contributions welcome.

## Contributing

PRs welcome. Please test locally before submitting.
