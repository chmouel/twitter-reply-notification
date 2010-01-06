#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
# Chmouel Boudjnah <chmouel@chmouel.com>
import twitter
import rfc822
import datetime
import os
import ConfigParser
import stat
import sys

CONFIG_FILE = os.path.expanduser("~/.config/twitter-reply-notification/config.ini")
CACHE_FILE = os.path.expanduser("~/.cache/twitter-reply-notification/cache")

def setup_dir():
    if not os.path.exists(os.path.dirname(CONFIG_FILE)):
        os.mkdir(os.path.dirname(CONFIG_FILE), 0755)
    if not os.path.exists(os.path.dirname(CACHE_FILE)):
        os.mkdir(os.path.dirname(CACHE_FILE), 0755)

def send_mail(config, text):
    p = os.popen("%s -t" % config['sendmail_location'], "w")
    p.write("From: %s\n" % config['mail_from'])
    p.write("To: %s\n" % config['mail_to'])
    p.write("Subject: New Twits\n")
    p.write("\n") # 
    p.write(text)
    status = p.close()
    if status == 256:
        sys.exit(1)
    
def parse_config(config_file):
    if not os.path.exists(config_file):
        config = ConfigParser.ConfigParser()
        config.add_section("auth")
        config.set("auth", "username", "")
        config.set("auth", "password", "")
        config.add_section("mail")
        config.set("mail", "from", "")
        config.set("mail", "to", "")
        config.set("mail", "sendmail_location", "/usr/sbin/sendmail")
        config.write(open(config_file, 'w'))
        return

    filemode = stat.S_IMODE(os.stat(config_file).st_mode) & 0777
    if filemode != 384:
        os.chmod(config_file, 0600)    

    config = ConfigParser.ConfigParser()
    cfh = config.read(config_file)
    if not cfh:
        return 
    username = config.get('auth', 'username').strip()
    password = config.get('auth', 'password').strip()
    mail_from = config.get('mail', 'from').strip()
    mail_to = config.get('mail', 'to').strip()
    sendmail_location = config.get('mail', 'sendmail_location').strip()

    if not all([username, password, mail_from, mail_to]):
        return 

    return {
        'username' : username,
        'password' : password,
        'mail_from' : mail_from,
        'mail_to' : mail_to,
        'sendmail_location' : sendmail_location,
        }

def get_replies(config):
    ret = []
    api = twitter.Api(config['username'], config['password'])
    replies = api.GetReplies()
    if not replies:
        return (None, None)
    last = replies[0].id
    for reply in replies:
        fdate = datetime.datetime(*rfc822.parsedate(
                reply.created_at)[:-2]).strftime("%H:%M")
        ret.append("%s - %s: %s" % (fdate, reply.user.name, reply.text))
    return (ret, last)

def parse_last_seen_id():
    if not os.path.exists(CACHE_FILE):
        return
    last_seen_id = open(CACHE_FILE, 'r').read().strip()
    if last_seen_id:
        return last_seen_id
    return None
    
def main():
    setup_dir()
    config = parse_config(CONFIG_FILE)
    if not config:
        print "Configuration is missing"
        sys.exit(1)
        return
    config['last_seen_id'] = parse_last_seen_id()
    
    text, last_seen_id = get_replies(config)
    if not text or not last_seen_id:
        return

    if config['last_seen_id'] and \
            (int(last_seen_id) == int(config['last_seen_id'])):
        return

    open(CACHE_FILE, "w").write(str(last_seen_id))

    send_mail(config, "\n".join(text))
    
if __name__ == '__main__':
    main()
