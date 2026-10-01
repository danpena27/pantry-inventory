# Portfolio maintenance — October 1, 2026

Original final project: December 9, 2025, by Daniel Pena Arias.

- Replaced manual comma splitting/joining with the standard `csv` module, including quoted notes and blank lines.
- Kept inventory beside the scripts, with an optional path for isolated tests.
- Restored categories from saved items and avoided duplicate loads.
- Moved the missing-item message outside the deletion loop.
- Rejected zero/negative quantities and negative or non-finite costs.
- Limited numeric input exception handlers to `ValueError`.
- Labeled the report as current inventory value to reflect what it calculates.
- Added an import guard, sample data, documentation, and regression tests.
- Excluded the working inventory, caches, and environment files from Git.

Portfolio preparation and these focused repairs were assisted by ChatGPT. The original coursework structure and menu remain recognizable; the original files on the author's computer were preserved.
