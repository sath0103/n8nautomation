# Week 3 – Day 5: News Headlines Scraper

## Project overview

Build a small Python script that fetches a news website, extracts headlines from its HTML, and prints up to five unique headlines in the terminal.

- **Website:** BBC News — https://www.bbc.com/news
- **Main file:** `headlines.py`
- **Python version:** Python 3.11.9

## Step 1: Create the project folder

Open the VS Code PowerShell terminal and run:

```powershell
mkdir headlines
```

## Step 2: Navigate into the project folder

```powershell
cd headlines
```

Project location used in this walkthrough:

```text
F:\n8nautomation\headlines
```

## Step 3: Check the Python version

The `python` command was not found on this computer, so we used the Python launcher:

```powershell
py --version
```

Expected output:

```text
Python 3.11.9
```

## Step 4: Create a virtual environment

```powershell
py -3.11 -m venv venv
```

This creates a project-specific virtual environment in the `venv` folder.

## Step 5: Activate the virtual environment

PowerShell initially blocked script execution. For this terminal session, we ran:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activated the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

The terminal prompt should begin with `(venv)`.

> The execution-policy change applies only to the current PowerShell process.

## Step 6: Install required packages

```powershell
py -m pip install requests beautifulsoup4
```

- `requests` fetches the webpage.
- `beautifulsoup4` parses the HTML.

## Step 7: Create `headlines.py`

In VS Code Explorer, create a file named `headlines.py` inside the `headlines` folder.

Expected structure:

```text
headlines/
├── venv/
└── headlines.py
```

## Step 8: Fetch the webpage

The first version of the script was:

```python
import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=10)

print("HTTP Status Code:", response.status_code)
print("Webpage fetched successfully!")
```

Run it with:

```powershell
py headlines.py
```

We received HTTP status code `200`, confirming that the page request succeeded.

## Step 9: Inspect the webpage HTML

1. Open https://www.bbc.com/news in Chrome.
2. Press `F12` to open Developer Tools.
3. Use the **Elements** tab.
4. Right-click directly on an article headline and choose **Inspect**.

The inspected headline was inside an element similar to:

```html
<h2 data-testid="card-headline" class="...">
    Arab parties could hold key as Netanyahu and Eisenkot set to fall short of victory
</h2>
```

The selector identified during inspection was:

```css
h2[data-testid="card-headline"]
```

Note: The HTML returned to Python can differ from what the browser displays. If the selector stops finding headlines, inspect the current page and adjust the selector.

## Step 10: Extract headlines

We then used BeautifulSoup to find headline elements:

```python
soup = BeautifulSoup(response.text, "html.parser")
items = soup.select('h2[data-testid="card-headline"]')

print("Headlines found:", len(items))

for item in items[:5]:
    print(item.get_text(strip=True))
```

The terminal reported `Headlines found: 49` during our test, and printed five headlines.

## Step 11: Final version of `headlines.py`

Replace the contents of `headlines.py` with this version:

```python
import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def main():
    try:
        response = requests.get(
            URL,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select('h2[data-testid="card-headline"]')

        headlines = []
        seen = set()

        for item in items:
            headline = item.get_text(strip=True)

            if headline and headline not in seen:
                headlines.append(headline)
                seen.add(headline)

            if len(headlines) == 5:
                break

        if not headlines:
            print("No headlines found.")
            return

        for number, headline in enumerate(headlines, 1):
            print(f"{number}. {headline}")

        if len(headlines) < 5:
            print(f"Only {len(headlines)} unique headlines found.")

    except requests.RequestException as error:
        print(f"Unable to fetch the news website: {error}")


if __name__ == "__main__":
    main()
```

### Run the final script

Save the file using `Ctrl + S`, then run:

```powershell
py headlines.py
```

Expected output format (the actual news changes over time):

```text
1. First news headline
2. Second news headline
3. Third news headline
4. Fourth news headline
5. Fifth news headline
```

The script strips whitespace, skips empty and duplicate headlines, prints up to five unique headlines, checks HTTP errors, and handles request failures. If fewer than five unique headlines are available, it prints those found and reports the count.

## How the application works

1. **Requests** downloads the BBC News webpage.
2. **BeautifulSoup** parses the HTML.
3. A CSS selector finds elements matching `h2[data-testid="card-headline"]`.
4. Python removes empty and duplicate headline text.
5. The script prints up to five headlines, numbered from 1.

## Final submission checklist

According to the assignment PDF, submit:

- [ ] A screenshot of the terminal showing five headlines.
- [ ] The `headlines.py` file pushed to GitHub, with the repository link shared in WhatsApp.
- [ ] A screen-recorded video of the script running, posted in the community.

## Troubleshooting

### `python` is not found

Use the Python launcher instead:

```powershell
py --version
py headlines.py
```

### PowerShell blocks virtual-environment activation

Run the following in the current PowerShell session, then activate the environment:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### No headlines are found

The BBC page may have changed or may return different HTML to Python than it displays in Chrome. Inspect the current HTML and confirm that the selector is still correct. Some sites load content with JavaScript; in that case, `requests` alone may not retrieve the rendered headlines.
