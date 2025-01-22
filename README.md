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

    `Telegram Toolkit` - The folder offers a Telegram data enrichment toolkit that enhances the Telegram messages by uncovering implicit information, otherwise not directly available through the platform. It reveals the channel connections i.e., channel to channel graph, provide message forwarding chain and extracts entities across channels. The method reads raw Telegram messages as JSON and extracts the additional information aggregated into new JSON files. The nature of messages on the platform and their penetration across multiple channels can address interesting research questions. 

The Telegram Toolkit provides the following functionalities:

1. *Entities in Telegram*. Entities are provided only using text span indexes; the Telegram Toolkit extracts them.

2. *Channel to channel graph*. Given the collected data, it creates a channel-to-channel graph where nodes are the channels and edges are built when a message is forwarded from a channel (source) to a destination channel. This functionality creates a graph in [GML format](https://networkx.org/documentation/stable/reference/readwrite/gml.html). The edges are associated with the times when messages are forwarded.

3. *Message chain generation*. When you post a message and someone re-posts or forwards it, you can usually see where and when the message is forwarded. This does not happen with Telegram messages. As a solution, this functionality creates a CSV file where each source message (i.e., a new message) is associated at least with one destination message (i.e., forwarded message), the forwarding time, and the message text. Messages that are never forwarded do not appear in the CSV. The user must note that the source message and its channel might not be contained in the input collection of data; this is because Telegram does not provide information about where a message is forwarded and the proposed generation uses a backward mechanism starting from the destination messages.

4. *Compute the frequency of the entities over channels.* The tool computes the frequency of the entities for each channels.

5. *Compute the frequency of the entities over whole data collection.* The tool computes the frequency of the entities on the whole data.


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


