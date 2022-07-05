Python Runner
=============

Source code of [@py3rbot](https://t.me/py3rbot)


**Requires** Linux with chroot support (otherwise very unsafe)

Usage
-----
1. Clone this repository
   ```bash
   git clone https://github.com/vabgalimov/py3rbot
   cd py3rbot
   ```
1. [Obtain API_KEY][api-key-obtain]
1. Add API_ID and API_HASH to .env
   ```bash
   echo 'API_ID=1234567890' >> .env
   echo 'API_HASH=abcdef123456' >> .env
   ```
1. Add BOT_TOKEN to .env
   ```bash
   echo 'BOT_TOKEN=1234567890:abcdef123456' >> .env
   ```
1. Create py3rbot user
   ```bash
   useradd -M py3rbot
   ```
1. Install requirements
   ```bash
   pip install -r requirements.txt
   ```
1. Run main.py
   ```bash
   python main.py
   ```

Commands
--------
* /start
* /help
* /py - execute code
* /inline - inline mode help

[api-key-obtain]: https://docs.pyrogram.org/start/setup#api-key
