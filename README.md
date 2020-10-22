# Indeed.co.uk Job Scraper

This is a simple program that extracts the following information from job listings on https://www.indeed.co.uk/:

- Posted (When the job listing was posted)
- Job Title
- Salary
- Company
- Location
- Job Description
- Job URL

Two columns are also generated and prepended to the extracted data:

- Date (The date the search was performed)
- Time (The time the search was performed)

## How to use

To use the program, follow the steps below:

- Ensure both uk_indeed_job_info.py and uk_indeed_scraper.py are in the same directory
- Create a new directory inside the directory that contains the above files and name it 'output_data'
- Change the `NUMBER_OF_SEARCH_PAGES` variable inside of uk_indeed_scraper.py to the number of pages you would like to extract (each page currently contains 15 job listings)
- Run uk_indeed_scraper.py

Once the program has finished running, a CSV titled with the current date will be downloaded into the 'output_data' folder. From here, you can open the CSV file and sort through the job listing data.

---
**NOTE**

The program is currently set up to search for Junior Data job listings in the London area which are then sorted by date posted, however, the `location`, `sort_type`, and `position` variables within uk_indeed_scraper.py can be changed to generate different search results. You can also set the `remote_results` variable to True if you would only like to return jobs which have been tagged as remote.

---
