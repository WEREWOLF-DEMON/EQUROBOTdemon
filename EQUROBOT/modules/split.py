from pyrogram import Client, filters
from pyrogram.types import Message
import os
from EQUROBOT import app

# Command to split the file
@app.on_message(filters.command("split"))
async def split_file(client: Client, message: Message):
    # Parse command arguments
    if len(message.command) != 3:
        await message.reply("Usage: /split <number of split> <filename>")
        return
    
    num_splits = int(message.command[1])
    base_filename = message.command[2]
    
    # Check if a document is sent with the command
    if not message.reply_to_message or not message.reply_to_message.document:
        await message.reply("Please reply to a document with this command.")
        return
    
    # Download the file
    doc = message.reply_to_message.document
    file_path = await doc.download()
    
    # Split the file
    try:
        with open(file_path, "rb") as f:
            file_size = os.path.getsize(file_path)
            part_size = file_size // num_splits
            
            for i in range(num_splits):
                start = i * part_size
                end = (i + 1) * part_size if i != num_splits - 1 else file_size
                
                part_file_path = f"{base_filename}{i+1}.txt"
                
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
