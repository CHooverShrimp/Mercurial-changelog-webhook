# Mercurial-changelog-webhook
Simple Python implementation of a webhook for Mercurial source control

I suggest using the passive webhook, since the active one will do a loop every second and check for changes on the changelog (incredibly taxing)

I did both in case there's a need for it (probably won't)

## Instruction

1. Create a python environment
2. Download the passive webhook file
3. Edit the hgrc of your repo to include
```
# [hooks]
# changegroup =/bin/bash -c '. /yourPythonEnvironment/bin/activate && python3 /yourPathToThisFile/passive_webhook.py https://username:password@your.repos.com/hg/repo/rev/ https://your.repos.com/hg/repo/rev/'
```
*(hgrc file is in .hg, you might have to create the file)*
4. give the appropriate permission for your web server to execute the hgrc webhook (chown www-data:www-data [DIRECTORY] -R)
