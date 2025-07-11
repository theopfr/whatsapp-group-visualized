# WhatsApp Data Extraction
Note: This only works on Android. iOS users — I can't help you :/

## 1. Extracting a backup
The following steps were copied and modified from [this guide](https://gist.github.com/TraceM171/0e6bd8f930cddb5e468e9e6d0460d22a#gistcomment-5667561).

1. **Open WhatsApp** on an Android phone that contains all the messages you want to extract.
2. Go to **Backup Settings**:
   - Navigate to `Settings -> Chats -> Chat backup` (path may vary in future versions of WhatsApp).
3. **Manage End-to-End Encrypted Backup**:
   - If backup encryption is **disabled**, proceed to Step 4.
   - If encryption with a **password** is enabled, disable it and proceed to Step 4.
   - If encryption with a **64-digit encryption key** is enabled and you **don’t know the key**, disable it and proceed to Step 4.
   - If encryption with a **64-digit encryption key** is enabled and you **know the key**, proceed to Step 5.
4. **Enable Backup Encryption**:
   - Choose to use a **64-digit encryption key**.
   - After the key is generated, **take note of it**, as it will be needed later.
   - Then create a backup and wait until it's done.
5. **Extract WhatsApp Data from your File System**:
   - Locate the `WhatsApp/Databases` folder on your Android phone. It's probably under:
     `/Android/media/com.whatsapp/WhatsApp/Databases/`
   - In that folder, you will find `msgstore.db.crypt15`. Download it and send it to your computer.
6. **Decrypt the Encrypted File**:
   - Use the encrypted `.crypt15` file and the 64-digit encryption key with the tool [wa-crypt-tools](https://github.com/ElDavoo/wa-crypt-tools).
   - Example command:
     ```bash
     wadecrypt <64digitkey> msgstore.db.crypt15 msgstore.db
     ```
   - You now have a `msgstore.db` SQLite file with all your chat data!

## 2. Exporting the chat group data
In this step you will locate the actual group chat within your `msgstore.db` file and export it to CSV. To do so, follow these steps:
- Download [sqlitebrowser](https://sqlitebrowser.org/) or any other database explorer.
- Open your `msgstore.db` file.
- Open the `chat` table and filter for your group's name in the "subject" column.
- Once found, take note of the `_id` column — this is the group chat's ID on your phone.
- Open the `messages` table and filter the `chat_row_id` column for the `_id` of your group chat.
- You should now only see messages from that group. Click the "Save table as currently displayed" icon and export to CSV.

Done!

## 3. Mapping JIDs to member names
Every row in the resulting CSV file is a message and has a `sender_jid_row_id` column. Each user corresponds to one **or more** of those IDs.  
I currently don’t have a great way to automatically map this, so you’ll need to go through the messages in the CSV (or easier: in sqlitebrowser) and take note of which user corresponds to which JID(s). Write that down somewhere, as it’s needed later.
