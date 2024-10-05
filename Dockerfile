# scraper/Dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /home

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Scrapy project
COPY . .

# create folder for downloaded pdfs
RUN mkdir -p /home/pdf_downloader/container-data/pdf-files

# Set the entry point (can also be done in docker-compose.yml command)
RUN chmod +x /home/pdf_downloader/downloader-startup.sh

ENTRYPOINT ["./pdf_downloader/downloader-startup.sh"]
