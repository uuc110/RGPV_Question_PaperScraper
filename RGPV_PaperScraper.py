import aiohttp
import asyncio
from pathlib import Path
import time


async def download_pdf(session, url, destination_folder):
    """
    Download a PDF from a given URL and save it to the specified destination folder.
    """
    try:
        async with session.get(url) as response:
            if response.status == 200:
                filename = url.split("/")[-1]
                file_path = Path(destination_folder) / filename
                with open(file_path, "wb") as file:
                    file.write(await response.read())
                return True, f"Downloaded: {file_path}"
            else:
                return False, f"Failed to download: {url} with status {response.status}"
    except Exception as e:
        return False, str(e)


async def generate_and_download_pdfs(
    base_url, years, months, destination_folder, subjects, branch
):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for year in years:
            for month in months:
                for course_code, course_name in subjects[branch].items():
                    url = (
                        base_url.format(
                            branch=branch.lower(),
                            course_code=course_code,
                            course_name=course_name.replace(" ", "-"),
                        )
                        + f"-{month}-{year}.pdf"
                    )
                    subject_folder = Path(destination_folder) / branch / course_code
                    subject_folder.mkdir(parents=True, exist_ok=True)
                    tasks.append(download_pdf(session, url, subject_folder))

        results = await asyncio.gather(*tasks)
        for task, (success, message) in zip(tasks, results):
            print(success, message)


# Run the function
async def main():
    base_url = "https://www.rgpvonline.com/be/{branch}-{course_code}-{course_name}"
    years = range(2011, 2024)
    months = ["may", "jun", "nov", "dec"]
    destination_folder = "Output"
    subjects = {
        "it": {
            "701": "soft computing",
            "802": "soft computing",
            "8002": "soft computing",
        },
    }
    selected_branches = ["it"]

    for selected_branch in selected_branches:
        await generate_and_download_pdfs(
            base_url, years, months, destination_folder, subjects, selected_branch
        )


# Measure the time taken for the aiohttp implementation
start_time = time.time()
asyncio.run(main())
end_time = time.time()
print(f"aiohttp implementation took {end_time - start_time:.2f} seconds")
