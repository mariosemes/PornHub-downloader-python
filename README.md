# PornHub Downloader

[![GitHub Issues Open](https://github-basic-badges.herokuapp.com/issues/mariosemes/PornHub-downloader-python.svg)]()

Feel free to join my discord server if you have any ideas, features or even bugs to talk about, you are welcome!
[JOIN DISCORD](https://discord.gg/JV2NxhH)

If you feel like it, you can donate me a beer or two ;) Just for the troubles!
[DONATE BUTTON](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=7MTJVTTQM9YQE&source=url)

# Installation

Check what version of python you have: python --version
Recommended & tested usage is with python3.
Also, check if you have pip3 installed (apt install python3-pip).

```bash
1. $ apt install python3
2. $ apt install python3-pip
3. $ pip3 install youtube-dl
4. $ pip3 install prettytable
5. $ pip3 install bs4
6. $ wget https://github.com/mariosemes/PornHub-downloader-python/archive/master.zip
7. $ unzip master.zip
8. $ cd PornHub-downloader-python-master
9. $ python3 phdler.py
```
It will ask you for your download folder PATH. Please enter your full path without the last backslash. Like this: /home/username/media/phmedia
On first run, phdler will create a database.db which will be used later for everything.


# Usage
```bash

+-------------------+---------+------------------------------------------------------+
| Tool              | command | item                                                 |
+-------------------+---------+------------------------------------------------------+
| python3 phdler.py | start   |                                                      |
| python3 phdler.py | custom  | url | batch                                          |
| python3 phdler.py | add     | model | pornstar | channel | user | playlist | batch |
| python3 phdler.py | list    | model | pornstar | channel | user | playlist | all   |
| python3 phdler.py | delete  | model | pornstar | channel | user | playlist         |
+-------------------+---------+------------------------------------------------------+
```

# Example

## START
```bash
python3 phdler.py start
```

## CUSTOM
```bash
python3 phdler.py custom https://www.pornhub.com/view_video.php?viewkey=ph5d69a2093729e
or
python3 phdler.py custom batch
```
The batch option will ask you for the full path of your .txt file where you can import multiple URLs at once.
Take care that every single URL in the .txt file is in his own row.

## ADD
```bash
python3 phdler.py add https://www.pornhub.com/model/luxurygirl
or
python3 phdler.py add https://www.pornhub.com/pornstar/leolulu
or
python3 phdler.py add https://www.pornhub.com/channels/mia-khalifa
or
python3 phdler.py add https://www.pornhub.com/users/lasse98
or
python3 phdler.py add https://www.pornhub.com/playlist/30012401
or
python3 phdler.py add batch
```
The batch option will ask you for the full path of your .txt file where you can import multiple URLs at once.
Take care that every single URL in the .txt file is in his own row.

## LIST
```bash
python3 phdler.py list model
or
python3 phdler.py list pornstar
or
python3 phdler.py list channels
or
python3 phdler.py list users
or
python3 phdler.py list playlist
or
python3 phdler.py list all
```

## DELETE
```bash
python3 phdler.py delete model
or
python3 phdler.py delete pornstar
or
python3 phdler.py delete channels
or
python3 phdler.py delete users
or
python3 phdler.py delete playlist
```
The option DELETE will list the selected item type, list them from the database and give you an option to enter the item ID of which one you want to be deleted.


# Explained

Every time you add a new item (model/pornstar and so on), the script will scrape the real name from the website and write it to the database. That is how we can have pretty names in final folders. Every added item is treated with a status of NEW=1, so the script knows that it needs to download all videos from the selected item. After the download of all videos is completed for the selected item, the script will change it to NEW=0. This way, when you START the script, it will first run down trough the database and ask for all items that have the status of NEW=1, and after that, it will check for new videos from items with the status NEW=0.
This should not bother you... I just wanted to explain how it works.


# Big thanks to

YouTube-DL,
PrettyTables,
BS4 aka BeautifulSoup4 
and of course, all of you :)