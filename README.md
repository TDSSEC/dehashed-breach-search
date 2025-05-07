# DeHashed Domain Search

DeHashed has recently been updated in May 2025. With access to new data wells and a new API interface.

This is a command-line tool to fetch and export DeHashed breach data for a given domain. Results are saved as a CSV containing selected fields such as email, password, and username.

---

## 🚀 Features

- Query DeHashed API by domain (e.g. `example.com`)
- Supports wildcard and deduplication options
- Automatically paginates through all available results
- Exports clean, structured data to CSV
- Filters only key fields: `id`, `name`, `email`, `database`, `username`, `hashed_password`, `password`

---

## 📦 Requirements

- Python 3.7+
- A valid [DeHashed](https://www.dehashed.com/) API key

---

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/dehashed-breach-search.git
cd dehashed-breach-search
pip install -r requirements.txt
```

## 🔐 Set Your API Key
Edit the script and replace YOUR_API_KEY with your DeHashed key:  
`api_key = "YOUR_API_KEY"`

--- 

## 🧪 Usage
### Get Everything  
Pull all possible entries for a given domain (maximum 10,000 per license model):  
`python dehashed_search.py --domain example.com`

### Limit Pages  
To iterate through a set number of pages:  
`python dehashed_search.py --domain example.com --max-pages 3`

### Options
| Argument        | Description                           |
| --------------- | ------------------------------------- |
| `--domain`      | Domain to search (e.g. `example.com`) |
| `--size`        | Results per page (default: 100)       |
| `--wildcard`    | Enable wildcard match                 |
| `--regex`       | Enable regex matching                 |
| `--dedupe`      | Remove duplicate entries              |
| `--max-pages`   | Maximum number of pages to crawl      |

### Output 
File will be saved as:  
`dehashed_example.com.csv`

--- 

## 🛡 Disclaimer

This tool is intended for authorized use only. Make sure you comply with all local laws, DeHashed terms, and ethical guidelines before using this data.
