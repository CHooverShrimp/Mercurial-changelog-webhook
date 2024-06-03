# Mercurial-changelog-webhook
Simple Python implementation of a webhook for Mercurial source control

I suggest using the passive webhook, since the active one will do a loop every second and check for changes on the changelog (incredibly taxing)
I did both in case there's a need for it (probably won't)
