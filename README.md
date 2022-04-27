# WotlkData

AiCore Scraping Project
Scrapes World of warcraft (The Lich King v3.5.5) in game character inventory items.
This is a web-site, I'm familiar with and is easy to scrape. It doesn't get reguary changes (if it get any changes at all).

## About the game

World of Warcraft (WoW) is a massively multiplayer online role-playing game (MMORPG) released in 2004 by Blizzard Entertainment. Set in the Warcraft fantasy universe, World of Warcraft takes place within the world of Azeroth, approximately four years after the events of the previous game in the series, Warcraft III: The Frozen Throne.[3] The game was announced in 2001, and was released for the 10th anniversary of the Warcraft franchise on November 23, 2004. Since launch, World of Warcraft has had eight major expansion packs: The Burning Crusade (2007), Wrath of the Lich King (2008), Cataclysm (2010), Mists of Pandaria (2012), Warlords of Draenor (2014), Legion (2016), Battle for Azeroth (2018), and Shadowlands (2020).

Similar to other MMORPGs, the game allows players to create a character avatar and explore an open game world in third- or first-person view, exploring the landscape, fighting various monsters, completing quests, and interacting with non-player characters (NPCs) or other players. The game encourages players to work together to complete quests, enter dungeons and engage in player versus player (PvP) combat, however the game can also be played solo without interacting with others. The game primarily focuses on character progression, in which players earn experience points to level up their character to make them more powerful and buy and sell items using in-game currency to acquire better equipment, among other game systems.

World of Warcraft was a major critical and commercial success upon its original release in 2004 and quickly became the most popular MMORPG of all time, reaching a peak of 12 million subscribers in 2010.The game had over one hundred million registered accounts by 2014[5] and by 2017, had grossed over $9.23 billion in revenue, making it one of the highest-grossing video game franchises of all time. The game has been cited by gaming journalists as the greatest MMORPG of all time and one of the greatest video games of all time and has also been noted for its long lifespan, continuing to receive developer support and expansion packs over 15 years since its initial release.In 2019, a vanilla version of the game titled World of Warcraft Classic was launched, allowing players to experience the base game before any of its expansions launched.


## Items

An item is something that a World of Warcraft player character can carry, either in their inventory, represented by an inventory icon, or tracked on a page in the character sheet. An item is a conceptual object in the player's head, not an object in the game world, although an item may also have an object associated with it. For example, clothing gear items are equipped, clothing gear objects appear on the character.

Item level (often abbreviated as ilevel or simply ilvl) is a rather important property of every item. It has two main functions — to reflect the item's usefulness and at the same time determine the minimum level a character must have in order to use it.
Item level serves as a rough indicator of the power and usefulness of an item, designed to reflect the overall benefit of using the item. Two items of equal ilvl should in theory therefore be of equal potential use.

## How the scraper works.

Lists : 'weapons' , 'armor' and 'armor_08' defines all the items available for scraping.
They are to be used as arguments to navigate to the main search page through drop down menu.
Main search page has filter section on the top, obtainable with a button(sometimes the filter 
appears to be on and the button change it's function to off). 
Items are filtered on item level base. 
Main page can only show 50 items at a time and up to 300 items obtainable with next page button.
To avoid missing an item while scraping, use_web_filter function set ranges of item level with step 10.
To get smaller than the max range(1-290) of items sctaped (for testing), variables min_item_lvl and max_item_lvl
can be changed inside the function.

woltk_scraper.py inherits functions from the ScraperBot class in scraper_bot.py, which allows opening chrome session, 
set of url, coockies management, hoovering over elements on the web page, clicking on elements and functions 
for filling text fields with keys from the keyboard.


## Running

Running wotlk_scraper.py as it is will start scraping all the items in predefined lists.
Headless and verbose options are available (headless for scraping without GIU, verbose - adds massages at different stages
of scraping process)and can be set to True or False while instantiate the Scraper class.
Directory named /raw_data will be created initaily in the file's current directory.
Ignore the error about already existance of this directory.
To upload on AWS S3, EC2 needs credentials to be configured inside the EC2 (aws configure).
Run docker image with :
           sudo docker run -d -p 5432:5432   -e "USER={DB master user name}"   -e "PASS={DB master password}"  -e "DATABASE=postgres" /
             -e "HOST={RDS end point}"   993845/wotlk:v{highest version}
## Dependencies 

python                    3.9.7 
selenium                  4.1.0
webdriver-manager         3.5.2 
pandas                    1.3.4
pillow                    9.0.1
urllib3
boto3
uuid
requests
datetime
psycopg2-binary
sqlalchemy

## Storing data

Data is stored in directory /raw_data localy, RDS and S3.
To opt-out uploading to the cloud - comment out /src/wotlk_scraper.py , lines : 199-231.
To upload to RDS from local computer - comment out /src/wotlk_scraper.py , lines : 194-196 
and enter your RDS cred in /config/cred_template.json (Don't forget to rename it as cred.json).

## Testing

Unittest can be run from test.py
It tests all the functions the scraper bot has.

## Monitoring

Scraper has been monitored with Grafana, set to visualise Prometheus (node exporter) metrics.
Configuration of the prometheus.yml-file take place on EC2 instance , while Grafana can be run localy or in additional EC2 instance.
Target port for monitoring the node is 9100, while grafana is listen to port 3000.
Prometheus can be run as a second container along with the scraper directly from docker-hub.









