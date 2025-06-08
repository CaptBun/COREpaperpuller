# CORE Paper Searcher

A GUI tool to search and export open access papers from the CORE API. Built with Python and Tkinter.

## Features

- Keyword search with sorting (by recently published)
- Year range filtering
- Export results in APA 7 format to txt doc

## Setup

1. Clone the repo:
    ```
    git clone https://github.com/CaptBun/COREpaperpuller.git
    cd COREpaperpuller
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Add your API key to a `.env` file:
    ```
    CORE_API_KEY=your_actual_api_key
    ```

4. Run the app:
    ```
    python core_searcher.py
    ```

## License
MIT
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)