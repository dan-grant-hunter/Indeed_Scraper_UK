"""
Scrapes job information from Indeed UK including Job Title,
Salary, Company, Location, Job Description and Job URL
and then outputs data to a CSV file. Outputted data
also includes date and time when scrape was performed.
"""

from datetime import datetime
import uk_indeed_job_info as ukid


# Change number_of_search_pages to specify how many pages to be scraped
number_of_search_pages = 3


# Constant variables
PAGE_RESULTS_NUMBERS = list(range(0, 300, 10))
URL_SUFFIX_NUMBERS = PAGE_RESULTS_NUMBERS[:number_of_search_pages]


# Location, sorting and language
location = "London"
sort_type = "date"
position = "Junior Data"


# Formatting for search
position = position.lower().replace(' ', '+')


# Time and date variables
now = datetime.now()
current_date = now.strftime("%d/%m/%Y")
current_time = now.strftime("%H:%M:%S")
date_time_list = [current_date, current_time]


# Main program
def main():
    # Create empty dictionary to store job listing information for each job
    job_dict = {}
    # Creating a running count that will act as a unique ID for each job listing
    count = 1
    # Loop through each page of job adverts
    for search_page in URL_SUFFIX_NUMBERS:
        # Create soup object for current main jobs listing page
        soup = ukid.main_page_setup(position, location, sort_type, search_page)
        # Extract job links from page
        job_links = ukid.prepare_job_links(soup)
        # Extract the times each job was posted from the main jobs page
        posted_times = ukid.capture_time_posted(soup)
        # Loop through each link, extract all data from job listing into list and add to dict
        for i, job_link in enumerate(job_links):
            # Create soup object for individual job listing page
            soup = ukid.single_page_setup(job_link)
            # Scrape individual job data from page
            job_data = ukid.scrape_page_data(soup)
            # Insert current date and time
            job_data = date_time_list + posted_times[i] + job_data + [job_links[i]]
            # Add job data to dict
            job_dict[count] = job_data
            # Increment count
            count += 1
    ukid.export_data(job_dict)


# Run program
if __name__ == '__main__':
    main()
