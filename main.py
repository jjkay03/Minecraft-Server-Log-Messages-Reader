# Minecraft Server Log Reader | By jjkay03 | Started on 11/01/2023

import gzip
import os
import re

logs_folder_path = "logs/"
player_messages_folder_path = "players messages/"
player_message_pattern = r"<(\w+)>\s(.+)$"
player_message_counts = {}


# Unzip all .gz files in the logs folder
def unzip_log_files():
    global logs_folder_path

    for file_name in os.listdir(logs_folder_path):
        if file_name.endswith(".gz"):
            # Open the .gz file and extract its contents
            with gzip.open(logs_folder_path + file_name, "rb") as gz_file:
                file_content = gz_file.read()
            # Write the extracted content to a new file
            with open(logs_folder_path + file_name[:-3], "wb") as extracted_file:
                extracted_file.write(file_content)
            # Delete the original .gz file
            os.remove(logs_folder_path + file_name)


# Count messages for each player
def count_each_players_messages():
    global logs_folder_path
    global player_message_pattern
    global player_message_counts

    for file_name in os.listdir(logs_folder_path):
        if file_name.endswith(".log"):
            with open(os.path.join(logs_folder_path, file_name), "r", encoding="utf-8") as log_file:
                for line in log_file:
                    match = re.search(player_message_pattern, line)
                    if match:
                        player_name = match.group(1)
                        player_message_counts[player_name] = player_message_counts.get(player_name, 0) + 1

    # Print the message counts for each player
    for player_name, message_count in sorted(player_message_counts.items(), key=lambda item: item[1], reverse=True):
        print(f"{player_name}: {message_count} messages")


# Save players messages to a file
def save_players_messages():
    global logs_folder_path
    global player_messages_folder_path
    global player_message_pattern

    for file_name in os.listdir(logs_folder_path):
        if file_name.endswith(".log"):
            with open(os.path.join(logs_folder_path, file_name), "r", encoding="utf-8") as log_file:
                for line in log_file:
                    match = re.search(player_message_pattern, line)
                    if match:
                        player_name = match.group(1)
                        message = match.group(2)
                        file_path = os.path.join(player_messages_folder_path, f"{player_name} messages.txt")
                        with open(file_path, "a", encoding="utf-8") as player_messages_file:
                            player_messages_file.write(f"{message}\n")

    # Sort messages in each player's file by timestamp
    for file_name in os.listdir(player_messages_folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(player_messages_folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as player_messages_file:
                lines = player_messages_file.readlines()
            lines.sort()  # Sort lines by timestamp
            with open(file_path, "w", encoding="utf-8") as player_messages_file:
                player_messages_file.writelines(lines)


# Main
unzip_log_files()
count_each_players_messages()
save_players_messages()

input("\nPress enter to exit...")