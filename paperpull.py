    #  CORE: A Global Aggregation Service for Open Access Papers
    # Knoth, P., Herrmannova, D., Cancellieri, M. et al. CORE: A Global Aggregation Service for Open Access Papers. 
    # Nature Scientific Data 10, 366 (2023). https://doi.org/10.1038/s41597-023-02208-w 

    # CORE: three access levels to underpin open access
    # Knoth, P., & Zdrahal, Z. (2012). CORE: three access levels to underpin open access. D-Lib Magazine, 18(11/12). 
    # Retrieved from http://oro.open.ac.uk/35755/ 

# CORE Paper Searcher
# This script provides a GUI to search for academic papers using the CORE API,
# allowing users to filter by keywords, sort by relevance or publication date,
# and specify a publication year range. Results can be saved in APA 7 format.

import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
from tkinter import filedialog
from tkinter import messagebox
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("CORE_API_KEY")

# Global state for pagination
current_query = ""
current_sort_by = "relevance"
current_sort_order = "desc"
current_year_from = None
current_year_to = None
current_offset = 0
current_limit = 10

def search_papers(query, limit=10, offset=0, sort_by="relevance", sort_order="desc", year_from=None, year_to=None):
    """Search for papers using the CORE API with given parameters."""
    url = "https://api.core.ac.uk/v3/search/works"
    headers = {"authorization": f"Bearer {API_KEY}"}
    params = {
        "q": query,
        "limit": limit,
        "offset": offset,
        "sortBy": sort_by,
        "sortOrder": sort_order
    }
    if year_from is not None:
        params["yearPublishedFrom"] = year_from
    if year_to is not None:
        params["yearPublishedTo"] = year_to
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        messagebox.showerror("API Error", f"Error fetching data: {str(e)}")
        return None
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        tk.messagebox.showerror("Error", f"Failed to fetch results: {response.status_code}\n{response.text}")
        return None

def format_apa7(paper): # Function to format paper data in APA 7 style
    authors = paper.get('authors', [])
    if authors:
        author_strs = []
        for a in authors:
            name = a.get('name', '')
            if ',' in name:
                last, first = name.split(',', 1)
                author_strs.append(f"{last.strip()}, {first.strip()[0]}." if first.strip() else last.strip())
            else:
                author_strs.append(name)
        authors_fmt = ', '.join(author_strs)
    else:
        authors_fmt = ""
    year = paper.get('yearPublished') or ""
    title = paper.get('title') or ""
    source = paper.get('publisher') or ""
    url = paper.get('landingPageUrl') or paper.get('fullTextUrl')
    doi = paper.get('doi')
    if not url and doi:
        url = f"https://doi.org/{doi}"
    apa = f"{authors_fmt} ({year}). {title}. *{source}*. {url if url else ''}"
    return apa.strip()

def run_search(reset_offset=True): # Function to run the search based on user input
    global current_query, current_sort_by, current_sort_order, current_year_from, current_year_to, current_offset
    if not query:
        messagebox.showwarning("Input required", "Please enter keywords before searching.")
        return
    query = keyword_entry.get()
    sort_by = "publishedDate" if sort_var.get() else "relevance"
    sort_order = "desc"
    year_from = year_from_entry.get().strip()
    year_to = year_to_entry.get().strip()
    year_from = int(year_from) if year_from.isdigit() else None
    year_to = int(year_to) if year_to.isdigit() else None

    # If new search, reset offset
    if reset_offset:
        current_offset = 0
        results_text.delete(1.0, tk.END)
    else:
        current_offset += current_limit

    # Save current search parameters
    current_query = query
    current_sort_by = sort_by
    current_sort_order = sort_order
    current_year_from = year_from
    current_year_to = year_to

    data = search_papers(
        query=current_query,
        limit=current_limit,
        offset=current_offset,
        sort_by=current_sort_by,
        sort_order=current_sort_order,
        year_from=current_year_from,
        year_to=current_year_to
    )
    # Display results in the text area
    if data and "results" in data and data["results"]:
        for paper in data["results"]:
            apa = format_apa7(paper)
            results_text.insert(tk.END, apa + "\n\n")
    else:
        if reset_offset:
            results_text.insert(tk.END, "No results found.\n")
        else:
            results_text.insert(tk.END, "No more results.\n")

    # Enable or disable the next button based on results
    if data and "results" in data and data["results"]:
        next_btn.config(state=tk.NORMAL)
        for paper in data["results"]:
            apa = format_apa7(paper)
            results_text.insert(tk.END, apa + "\n\n")
    else:
        if reset_offset:
            results_text.insert(tk.END, "No results found.\n")
            next_btn.config(state=tk.DISABLED)
        else:
            results_text.insert(tk.END, "No more results.\n")
            next_btn.config(state=tk.DISABLED)

def save_results():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(results_text.get(1.0, tk.END))

root = tk.Tk()
root.title("CORE Paper Searcher")

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(row=0, column=0, sticky="NSEW")

for i in range(5):
    mainframe.columnconfigure(i, weight=1)
mainframe.rowconfigure(4, weight=1)

ttk.Label(mainframe, text="Keywords:").grid(row=0, column=0, sticky="W")
keyword_entry = ttk.Entry(mainframe, width=40)
keyword_entry.grid(row=0, column=1, columnspan=3, sticky="EW")

separator = ttk.Separator(mainframe, orient='horizontal')
separator.grid(row=1, column=0, columnspan=5, sticky="EW", pady=5)

sort_var = tk.BooleanVar()
sort_check = ttk.Checkbutton(mainframe, text="Sort by most recent", variable=sort_var)
sort_check.grid(row=2, column=0, sticky="W")

ttk.Label(mainframe, text="Year from:").grid(row=2, column=1, sticky="E")
year_from_entry = ttk.Entry(mainframe, width=6)
year_from_entry.grid(row=2, column=2, sticky="W")
ttk.Label(mainframe, text="to").grid(row=2, column=3, sticky="E")
year_to_entry = ttk.Entry(mainframe, width=6)
year_to_entry.grid(row=2, column=4, sticky="W")

search_btn = ttk.Button(mainframe, text="Search", command=lambda: run_search(reset_offset=True))
search_btn.grid(row=3, column=0, pady=5)

next_btn = ttk.Button(mainframe, text="10 more Results", command=lambda: run_search(reset_offset=False))
next_btn.grid(row=3, column=1, columnspan=2,)
next_btn.config(state=tk.DISABLED)

save_btn = ttk.Button(mainframe, text="Save Results", command=save_results)
save_btn.grid(row=3, column=4,)

results_text = scrolledtext.ScrolledText(mainframe, width=100, height=25, wrap=tk.WORD)
results_text.grid(row=4, column=0, columnspan=5, pady=5, sticky="NSEW")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.rowconfigure(3, weight=1)

root.mainloop()