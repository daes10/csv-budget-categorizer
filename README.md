
## 🚧 **Heads up! WIP alert!** 🚧  
This project is still cooking. Use at your own risk 😎

---

## CSV Budget Categorizer

A simple tool to help categorize budget transactions stored in CSV files. It reads CSV data, applies categorization rules (by keywords, amounts, etc.), and outputs categorized transactions.

### 🚀 Features

- Parse CSV files with transaction data (date, description, amount, etc.)
- Define rules for categorizing transactions (e.g. “groceries”, “rent”, “entertainment”)
- Automatic assignment of categories based on matching criteria
- Generate summary reports (monthly/weekly) by category
- Export categorized transactions to CSV (or optionally JSON)

### 💡 Why

- Handling a bunch of bank transactions manually sucks. This project aims to:
- Save time by automating classification
- Give you insights into spending habits
- Be simple, extensible & usable without a heavy UI

### ⚙️ Requirements

- Python 3.13+
- Required libraries: `pandas`, `numpy`, `argparse`
