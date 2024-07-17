from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from urllib.parse import urlparse
import os
from EQUROBOT import app

# Function to download a file from URL
def download_file(url, output_dir):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for request errors

        # Get the filename from the URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)  # Extract filename from URL

        output_path = os.path.join(output_dir, filename)  # Output path with filename

        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"Downloaded {filename} successfully to {output_path}")
        return filename, output_path
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return None, None

# Command handler for /terabox command
@app.on_message(filters.command("terabox", prefixes="/"))
def terabox_command_handler(client, message):
    try:
        # Extract URL from command message
        download_link = message.command[1] if len(message.command) > 1 else None

        if download_link:
            output_directory = "./downloads"  # Change this to your desired output directory

            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            # Download the file
            filename, file_path = download_file(download_link, output_directory)

            if filename and file_path:
                # Send the downloaded file as a video (you can change this based on file type)
                message.reply_video(video=file_path, quote=True, caption=f"Downloaded video: {filename}")
            else:
                message.reply_text("Failed to download the file.")
        else:
            message.reply_text("Please provide a download link.")

    except Exception as e:
        print(f"Error processing /terabox command: {e}")
        message.reply_text("An error occurred while processing your command.")
