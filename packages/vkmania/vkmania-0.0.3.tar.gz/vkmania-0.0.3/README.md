# VKMania - Lightweight framework for creating VK bots
<p align="center"><a href="https://pypi.org/project/vkmania/">
    <img alt="downloads" src="https://img.shields.io/static/v1?label=pypi%20package&message=0.0.1&color=brightgreen"></a> 
    <blockquote>VKMania - A simple and lightweight framework for creating VK bots. At an early stage of development.</blockquote>
</p>

## Installation
1) Using PIP:
   
   Newest version:
   ```sh
   pip install vkmania
   ```
   
   Last stable release:
   ```sh
   pip install vkmania===0.0.3
   ```
> Python version - python 3+

***
## Basic Usage
```python
from vkmania import Bot, ReplyMessage

bot = Bot(token = '...token...', group_id = 123...)

@bot.command(text = "hi")
async def test(msg:ReplyMessage):
    await msg.reply("Oh, hello, hello!")

bot.start_longpoll()
```
