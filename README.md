# Pantry Inventory

A Python command-line pantry manager by **Daniel Pena Arias**, created for a Logic & Design final project in December 2025.

## Features

- Add items and categories, update quantities, remove stock, and search inventory.
- Track unit cost, notes, entry date, and expiration date.
- Save and restore inventory as CSV using Python's standard library.
- Display inventory value by entry month, with a text chart grouped by category.

## Run

Requires Python 3. No third-party packages are needed. Open a terminal in this folder:

```sh
python pantry_main.py
```

On Windows, `py pantry_main.py` also works if the Python launcher is installed.
Choose **7 — Save/Exit** to save. The program stores `pantry.csv` beside the scripts; this personal working file is excluded from Git.

For a demo, optionally copy `pantry.example.csv` to `pantry.csv` before launching. The example contains invented inventory. If you already have a `pantry.csv`, keep a backup before replacing it.

## Structure and checks

`pantry_main.py` contains the menu. `pantry_classes.py` contains the item model, manager, reports, and persistence. Run the regression tests with:

```sh
python -m unittest -v
```

The tests use temporary files and do not modify your inventory.

## Coursework and maintenance

The original project demonstrates classes, lists, loops, input validation, file handling, and menu-driven program design. October 2026 portfolio maintenance addressed CSV quoting, positive quantities, nonnegative finite costs, deletion feedback, saved categories, predictable file location, and safe module imports. See [CHANGES.md](CHANGES.md).

## Current limits

- Names and searches are case-sensitive. Adding an existing exact name increases its quantity while retaining its original details.
- Dates are entered as text. The report groups the current inventory by entry month across all years; it is not a purchase history or accounting report.
- Changes are saved when choosing Save/Exit, not automatically after each edit.
- Categories with no saved items are not retained after restarting.
- The program expects its CSV schema; manually malformed files may produce an error.

Source: [danpena27/pantry-inventory](https://github.com/danpena27/pantry-inventory)
