# Telegram-Data-Collection
## Description
The method helps to deploy a Telegram data collection setup for extracting messages broadcast across channels. As a broadcasting social media platform, the channel administrator can broadcast their content as text or other media messages to disseminate information to the users of that channel. The method takes public channel IDs (as seeds), requires a telephone number with Telegram App, and extracts messages in JSON format across all seed channels as well as other public channels where the messages from the seed channels were forwarded. 

## Keywords
Telegram, Social-Media, Data Collection

## Repo Structure
The repository is organized as follows:
* Folders
  
    `public_group_messages folder` -output folder where messages from channels will be stored as txt files

    `seed folder` - input folder where the channel names from where messages should be collected is stored

    `src folder` - Main code for data collection using Telethon API

    `tracking folder` - output folder for tracking the channel names and the time of the last message collected

* Files

    `config.py` - configurable parameters of the framework

## Environment SetUp
This method requires Python 3.x to run.

## Dependencies
To install the dependencies you may use: 

  `pip3 install -r requirements.txt `

You should also have Telegram installed and a Telegram account in your phone


## Limitation
The method collects only the raw messages. For enrichments to the messages, further modifications to the code would be required

## How to Use

1. Run in command line:  

   `python 1_extract_from_seed_list.py`

2. The framework will ask for a phone number : Enter the phone number through which Telegram account has been created

3. The framework will ask for an one time password : Enter the OTP sent to you through the Telegram app




## Input data
The output of this method is channel names which needs to be specified in the public_group_seed_list.txt file in seed folder

## Sample Input to the method

    britishnewspatriot
     bloomberg
     SpotifyGroup`

## Sample Output of the method

```{
  "_": "Message",
  "id": 2004376,
  "peer_id": {
    "_": "PeerChannel",
    "channel_id": 1050982793
  },
  "date": "2024-01-25 16:13:00.000000",
  "message": "In math homework, Reem was given a value of x and was asked to find y using the following formula.\ny = x + exp(x/100)\nThe function exp(z) is exponentiation in the natural log base, that is, e to the power of z (also written as e^z).\nReem wrote down the value of y, which is equal to 418.23783639564084, but forgot to note the value of x. Can you help her recover the value of x?\nYour answer should be a real number x. The answer is considered correct if when substituted into the formula above, the result is very close to y. More precisely, the answer is considered correct if and only if the following holds.\n|y - (x + exp(x/100))| < 0.001",
  "out": false,
  "mentioned": false,
  "media_unread": false,
  "silent": false,
  "post": false,
  "from_scheduled": false,
  "legacy": false,
  "edit_hide": false,
  "pinned": false,
  "noforwards": false,
  "from_id": {
    "_": "PeerUser",
    "user_id": 5885885469
  },
  "fwd_from": null,
  "via_bot_id": null,
  "reply_to": null,
  "media": null,
  "reply_markup": null,
  "entities": [],
  "views": null,
  "forwards": null,
  "replies": {
    "_": "MessageReplies",
    "replies": 1,
    "replies_pts": 3145930,
    "comments": false,
    "recent_repliers": [],
    "channel_id": null,
    "max_id": 2004379,
    "read_max_id": null
  },
  "edit_date": null,
  "post_author": null,
  "grouped_id": null,
  "reactions": null,
  "restriction_reason": [],
  "ttl_period": null
}
```



# Contact
Susmita.Gangopadhyay@gesis.org


