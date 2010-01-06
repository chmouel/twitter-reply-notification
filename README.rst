================================
 Twitter notification via Email
================================

:Credits:   Copyright 2009--2010 Chmouel Boudjnah <chmouel@chmouel.com>
:Licence:   BSD

Installation
============

You need to have python-twitter installed you can install from source from here

    http://code.google.com/p/python-twitter/

or on Debian or Ubuntu installed directly from the apt repositories :

    aptitude install python-twitter

Config
======

- On the first run of the script it will create a file in
  your home directory called ~/.config/twitter-reply-notification/config.ini containing::

    [mail]
    to = 
    from = 
    sendmail_location = /usr/sbin/sendmail

    [auth]
    username = 
    password = 

- Fill them with the proper information with auth being the twitter
  auth and password.

- sendmail needs to be configured locally.

- setup it as a cron every 10mn or so to get the notification.
