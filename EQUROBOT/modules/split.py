from pyrogram import Client, filters
from pyrogram.types import Message
import os
from EQUROBOT import app


@app.on_message(filters.command("split"))
async def split_file(client: Client, message: Message):
    # Check for usage and reply filter
    if len(message.command) != 2:
        await message.reply("Usage: /split <number of splits>")
        return
    
    # Get the number of splits from the command argument
    try:
        num_splits = int(message.command[1])
        if num_splits <= 0:
            raise ValueError("Number of splits must be positive.")
    except ValueError as e:
        await message.reply(f"Invalid number of splits: {e}")
        return
    
    # Ensure the command is in reply to a document
    if not message.reply_to_message or not message.reply_to_message.document:
        await message.reply("Please reply to a document with this command.")
        return
    
    # Download the file
    doc = message.reply_to_message.document
    file_path = await doc.download()
    
    # Get the original filename without extension
    base_filename, _ = os.path.splitext(doc.file_name)
    
    # Split the file
    try:
        with open(file_path, "rb") as f:
            file_size = os.path.getsize(file_path)
            part_size = file_size // num_splits
            
            for i in range(num_splits):
                start = i * part_size
                end = (i + 1) * part_size if i != num_splits - 1 else file_size
                
                part_file_path = f"{base_filename}_{i+1}.txt"
                
                with open(part_file_path, "wb") as part_file:
                    f.seek(start)
                    part_file.write(f.read(end - start))
                
                # Send the part
                await client.send_document(
                    chat_id=message.chat.id,
                    document=part_file_path,
                    caption=f"Part: {i+1}/{num_splits}"
                )
                
                # Remove the part file
                os.remove(part_file_path)
                
    except Exception as e:
        await message.reply(f"An error occurred: {e}")
    finally:
        # Clean up the original file
        os.remove(file_path)
