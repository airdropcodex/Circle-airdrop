# Circle Bot for Circle Airdrop

This repository contains an automation script for watching ads as part of an airdrop project on Telegram called **Circle**. The script processes accounts stored in a file and automates the ad-watching process to earn rewards.

---

## Features

- **Ad Watching Automation**: Automatically interacts with ads to claim rewards for multiple accounts.  
- **Account Management**: Reads account details from a structured file (`data.txt`).  
- **Logging**: Tracks activity and errors in real-time via console and log files.  
- **Threaded Execution**: Processes multiple accounts concurrently to improve efficiency.  
- **Graceful Shutdown**: Allows for interruption handling using signals.  

---

## File Structure

- `circle.py` - The main script that handles the automation.  
- `data.txt` - A configuration file containing account details.  
- `app.log` - A log file to track script execution and errors.  
- `requirements.txt` - Contains Python dependencies for the project.  
- `README.md` - Documentation for the project.  
- `License` - License file for the project.  

---

## Pre-requisites

- Python 3.12  
- `pip` (Python package manager)  

---

## Setup

1. Clone the repository:  

   ```bash
   git clone https://github.com/YouTubeDLPro/Circle-bot.git
   ```
   Change the directory to the repo folder:
   ```bash
   cd Circle-bot
   ```
   
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Prepare the data.txt file with your account details. The file should follow this format:

```
tg_id=YOUR_TG_ID
tg_platform=YOUR_TG_PLATFORM
language=en
chat_type=sender
chat_instance=YOUR_CHAT_INSTANCE
top_domain=bot.toncircle.org

tg_id1=YOUR_TG_ID1
tg_platform1=YOUR_TG_PLATFORM1
language1=en
chat_type1=sender
chat_instance1=YOUR_CHAT_INSTANCE1
top_domain1=bot.toncircle.org

tg_id2=YOUR_TG_ID2
tg_platform2=YOUR_TG_PLATFORM2
language2=en
chat_type2=sender
chat_instance2=YOUR_CHAT_INSTANCE2
top_domain2=bot.toncircle.org
```
Note: You can add as many accounts as you want, but the details should strictly follow this format.

And there are place for giving 20 telegram accounts details.

---

## How to Use

1. Run the script:

python circle.py


2. The script will:

Load account data from data.txt.

Start automated ad-watching for each account.

Log progress and errors in app.log.



3. Use CTRL+C to gracefully shut down the script.




---

## Logs

All activities, errors, and debugging information are logged to: app.log

Console Output: Real-time updates.

app.log: Persistent log file.



---

## Troubleshooting

File Not Found: Ensure data.txt is in the same directory as the script or update the file path in the script.

Incomplete Data: Double-check data.txt for missing or malformed entries.

Dependencies: Use pip install -r requirements.txt to ensure all dependencies are installed.



---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

---
## Donation 

If you find this script helpful, then you can donate me via TON, TRON and TetherUSD(TRC20). 

Address:
TON :-
```bash
UQBzIaiaq09t1tkhvQqghENXvs-qXKvM1R9A5wLm7_nfUTz9
```
Tron and TetherUSD(TRC20) :-
```bash
TM84PPmuDEu1UfC5JrZ16XaX4s5Dqjz3Fi
```
---

## License

This project is licensed under the MIT License. See the License file for details.


---

## Disclaimer

Use this script at your own risk. Using automated scripts can lead to account bans.


---

## Happy Farming!
