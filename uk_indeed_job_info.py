"""All of the necessary variables and functions to scrape
job information data from Indeed UK"""

from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Constant variables
URL_PREFIX = 'https://uk.indeed.com'
REMOTE_LINK = '&remotejob=032b3046-06a3-4876-8dfd-474eb5e7ed11'

# Time and date variables
now = datetime.now()
file_date = now.strftime("%Y_%m_%d")


# Class selectors
company_class = "icl-u-lg-mr--sm icl-u-xs-mr--xs"
location_class = "icl-u-xs-mt--xs icl-u-textColor--secondary " \
                 "jobsearch-JobInfoHeader-subtitle " \
                 "jobsearch-DesktopStickyContainer-subtitle"
salary_class = 'icl-u-xs-mr--xs'


def main_page_setup(position, location, sort_type, search_page, remote):
    """Create soup object for main jobs page"""
    url = f'https://uk.indeed.com/jobs?q={position}&l={location}' \
                                f'&sort={sort_type}{remote}&start={search_page}'
    main_jobs_page = requests.get(url).text
    soup = BeautifulSoup(main_jobs_page, 'lxml')
    return soup


def prepare_job_links(soup):
    """Prepare list of job links from header titles"""
    job_links = []
    results = soup.select("a[class^=tapItem]")
    for i in range(len(results)):
        job_link = f"{URL_PREFIX}{results[i]['href']}"
        job_links.append(job_link)
    return job_links


def capture_time_posted(soup):
    """Prepare list of times when each job was posted"""
    posted_times = []
    results = soup.select('span[class*="date"]')
    for i in range(len(results)):
        posted_time = list(results[i].strings)[1]
        posted_times.append([posted_time])
    return posted_times


def capture_remote_tags(soup):
    """Capture remote tags to include in output file"""
    remote_tags = []
    results = soup.select('span[class="remote"]')
    for i in range(len(results)):
        remote_tag = results[i].text
        remote_tags.append([remote_tag])
    return remote_tags


def single_page_setup(job_link):
    """Create soup object for individual job page"""
    job_link_url = job_link
    job_information = requests.get(job_link_url).text
    soup = BeautifulSoup(job_information, 'lxml')
    return soup


def scrape_page_data(soup):
    """Scrape data from individual job listing page"""

    # Handle job listings where no title is provided
    title_provided = soup.find('h1')
    if title_provided:
        title = soup.find('h1').text
    else:
        title = "N/A"

    # Handle job listings with no salary details given
    salary_provided = soup.find('span', class_=f'{salary_class}')
    if salary_provided:
        salary = soup.find('span', class_=f'{salary_class}').text
    else:
        salary = "N/A"

    # Handle job listings where company name is not provided
    company_name_provided = soup.find('div', class_=f'{company_class}')
    if company_name_provided:
        company = soup.find('div', class_=f'{company_class}').text
    else:
        company = "N/A"

    # Handle job listings where location is not provided
    location_provided = soup.find('div', class_=f'{location_class}')
    if location_provided:
        location = soup.find('div', class_=f'{location_class}').find_all('div')[-1].text
    else:
        location = "N/A"

    # Handle job listings where no job description is provided
    job_info_provided = soup.find('div', id="jobDescriptionText")
    if job_info_provided:
        job_info = soup.find('div', id="jobDescriptionText").text
    else:
        job_info = "N/A"

    job_data = [title, salary, company, location, job_info]
    return job_data


def export_data(job_dict):
    """Create DataFrame and export data to CSV file"""
    job_data = pd.DataFrame.from_dict(job_dict, orient='index',
        columns=['Date', 'Time', 'Posted', 'Job Title', 'Salary', 'Company',
                 'Location', 'Job Description', 'Job URL'])
    # Export to CSV
    job_data.to_csv(r'output_data/uk_indeed_job_data_{}.csv'.format(file_date))
