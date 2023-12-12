import requests
from pathlib import Path


def download_pdf(url, destination_folder):
    """
    Download a PDF from a given URL and save it to the specified destination folder.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        filename = url.split('/')[-1]
        file_path = Path(destination_folder) / filename
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return True, f"Downloaded: {file_path}"
    except Exception as e:
        return False, str(e)


def generate_and_download_pdfs(base_url, years, months, destination_folder, subjects, branch):
    for year in years:
        for month in months:
            for course_code, course_name in subjects[branch].items():
                url = base_url.format(branch=branch.lower(), course_code=course_code,
                                      course_name=course_name.replace(' ', '-')) + f"-{month}-{year}.pdf"
                subject_folder = Path(destination_folder) / branch / course_code
                subject_folder.mkdir(parents=True, exist_ok=True)
                success, message = download_pdf(url, subject_folder)
                print(url, success, message)


# Define subjects directly in the script

# add subject code, subject name and branch ID, below.
subjects = {
    "it": {
        # "501": "operating system",
        #   "502": "computer networks",
        # "503": "c object oriented analysis and design",
        # "504": "c java programming",
        # "5002": "theory of computation",
        # "404": "analog and digital communication",
        "7002": "object oriented analysis and design",
        "701": "object oriented analysis and design",
        "503": "c object oriented analysis and design",


    },
    "cs-it-ee": {
        "405": "analog and digital communication",
    }
}

# User Input for Branch or enter the branch name which is in subjects variable above.
selected_branch = "it"

# Base URL template
base_url = "https://www.rgpvonline.com/be/{branch}-{course_code}-{course_name}"

# Define the range of years and months
years = range(2010, 2022)
months = ["may", "jun", "nov", "dec"]

# Main destination folder for downloads
destination_folder = "Output"

# Run the function
generate_and_download_pdfs(base_url, years, months, destination_folder, subjects, selected_branch)
