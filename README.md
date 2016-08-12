# PyQBot: A robot program for QQ, written in python. **&lt;NOT API LIBRARY!>**

## A project based on [pyQQRobot](https://github.com/eyeKill/pyQQRobot).

## Currently supported functions:

- Receive and display messages you got
- Display replies the program sent.
- Ping and Pong
- Wolfram|Alpha query **&lt;NEEDS API KEY!>**
- [Tuling(English: Turing) Robot](http://www.tuling123.com) **&lt;NEEDS API KEY!>**

## How To Use

First, get a .veri file by running:

    $ python3 genVeriFile.py

It will ask you to scan the QR in order to login. By default the QR image won't show automatically on Linux, you have to open it manually.

After getting the .veri file, a.k.a saved the login state, you can start the robot program:

    $ python3 bot.py &lt;*QQID*.veri>

Don't forget to re-generate the .veri file if your .veri file is not up-to-date. In this case, your robot won't login properly until you get a new .veri file.

When you successfully started the bot program, try typing 'wa &lt;query>' to activate Wolfram|Alpha search. Also you can talk with the Tuling Robot by typing 'wtmbot &lt;text>'. You can change 'wtmbot' to other names in the source file. For example, from this:

    41                log.i('Wolfram', 'response: ' + reMsg)
    42        elif msg[0:**7**].lower() == '**wtmbot **':
    43          msg = msg[**7**:]
    44          reMsg = user['nick'] + '：' + t.response(msg, uin)

To this:

    41                log.i('Wolfram', 'response: ' + reMsg)
    42        elif msg[0:**6**].lower() == '**tlbot **':
    43          msg = msg[**6**:]
    44          reMsg = user['nick'] + '：' + t.response(msg, uin)

    Note the number changed, and the space after the name.

## File structure:

- bot.py: the main program
- genVeriFile.py: generates .veri verication file for the robot program to login without scanning QRs every time
- tuling.py: Tuling Robot API Class
- wolfram.py: Wolfram|Alpha API Class
- original pyQQRobot Project
    - mlogger.py
    - qqfriends.py
    - qqhttp.py
    - qqhttp\_gevent.py
    - qqrobot.py
