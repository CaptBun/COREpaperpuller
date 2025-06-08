# CORE Paper Searcher

A GUI tool to search and export open access papers from the CORE API. Built with Python and Tkinter.

The tool uses the api for the CORE database of open access reaserch papers across all diciplines. This tool is a simple method of searching this database and spitting them out in APA 7 text format. 

## Features

- Keyword search with sorting (by recently published)
- Year range filtering
- Export results in APA 7 format to txt doc

## CORE API
- inorder to use this app you will need to create a unique API key over at https://core.ac.uk/services/api
- This does require signing up with an email address, but it is a simple enough process.

## Windows Setup

- The current release is compiled as a windows EXE file. 
- in addidion to the exe you will need a `.env` file.
- This file can be created by making a new txt file and naming it '.env' (i.e. no file name, just the extension .env).
- in the env file you will need one line
    '''
    CORE_API_KEY=your_actual_api_key
    '''
- Once this is set up you should be able to launch the exe and have the app function.

## Python Script Setup

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
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Citation
  CORE: A Global Aggregation Service for Open Access Papers
 Knoth, P., Herrmannova, D., Cancellieri, M. et al. CORE: A Global Aggregation Service for Open Access Papers. 
 Nature Scientific Data 10, 366 (2023). https://doi.org/10.1038/s41597-023-02208-w 

 CORE: three access levels to underpin open access
 Knoth, P., & Zdrahal, Z. (2012). CORE: three access levels to underpin open access. D-Lib Magazine, 18(11/12). 
 Retrieved from http://oro.open.ac.uk/35755/ 