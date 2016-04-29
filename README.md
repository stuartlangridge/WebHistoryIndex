# WebHistoryIndex

A search engine for all the web pages you've ever looked at.

This is an alarmingly simple implementation and not at all ready for production. But it works for me.

There are two parts: the server and the browser extension.

## The server

### Initial server setup

    git clone git@github.com:stuartlangridge/WebHistoryIndex.git
    cd WebHistoryIndex
    virtualenv --system-site-packages ./venv
    source ./venv/bin/activate
    pip install whoosh
    pip install Flask

### Running the server

    bash run.sh # you might want to put this in your crontab so it runs on reboot

## The browser extension

Only for Chrome right now, I'm afraid. In Chrome, go to <a href="chrome://extensions">chrome://extensions</a>, say "add unpacked extension", and add the `extensions/chrome` folder from this repository.

# Using it

Go to <a href="http://localhost:5150">http://localhost:5150</a>. Search in the box; see results. Robert's your mother's brother.

