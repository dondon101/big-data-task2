# Python project with Docker

This is a simple Python project for scraping news headlines from [Delfi](www.delfi.lt/en) website. 
The script is containerized using Docker for ease of deployment.

## Scraper
The code is a web scraper designed to extract news article headlines, URLs, and labels. 
I used the `requests` library to fetch web pages, `BeautifulSoup` for parsing HTML, and `pandas` for 
saving the scraped data to a CSV file. Here's a brief description of each function and the main script:

1. **get_sections(_url_)**
   Fetches the main page of the news website.
   Parses the HTML to find and collect URLs of different sections (e.g., politics, business).
   Returns the first five section URLs.

2. **get_section_links(_menu_item_link_)**
   Takes a list of section URLs.
   For each section URL, it fetches and parses the HTML to find pagination buttons and determine the number of pages (up to 3) available in that section.
   Constructs URLs for the first three pages of each section and returns a list of these URLs.

3. **get_articles(_url_final_list_)**
   Takes a list of page URLs.
   For each URL, it fetches and parses the HTML to extract the headline, URL, and label of each news article on the page.
   Stores the extracted data in a list of dictionaries and returns this list.

**Main Script:**
  Defines the base URL of the news website.
  Calls **get_sections()** to get section URLs.
  Calls **get_section_links()** to get URLs of the first few pages in each section.
  Calls **get_articles()** to scrape headlines, URLs, and labels from these pages.
  Converts the scraped data into a Pandas DataFrame and saves it as a CSV file (article_data.csv).

## Docker
The Dockerfile named **scraper.Dockerfile** does the following:
* `FROM python:3.11-slim` -- uses a slim version of Python 3.11 as the base image;
* `WORKDIR /main_task` -- sets the working directory in the container to **_/main_task_**;
* `COPY . /main_task` -- copies all the files from the current directory on the host to the working directory in the container;
* `RUN pip install --upgrade pip && pip install -r requirements.txt` -- upgrades pip and installs the required Python packages listed in **requirements.txt**;
* `CMD ["python", "scraper.py"]` -- Specifies the command to run the Python script `scraper.py` when the container starts.

To build a Docker image in cmd run: 
```bash
`docker build -t my_scraper_pythonproject -f scraper.Dockerfile .`
```

Run the scraper container:
```bash
`docker run -v "$(PWD):/main_task" my_scraper_pythonproject` 
```

This command mounts the current directory ($(PWD)) to the **_/main_task_** directory
inside the Docker container, allowing the scraper.py script to write the **article_data.csv** file to local file system.

### Docker Image
The Docker image for this project is available on Docker Hub. You can pull the image using the following command:

```bash
docker pull donatassl/my_scraper_pythonproject:latest
```
