Flathunter (https://github.com/flathunters/flathunter) is a Telegram bot that scrapes flat listing websites and sends notifications to telegram when a flat comes up that matches the required criteria.

This is an attempt at decoupling the two parts of it (the part about finding flats, and the part about sending messages to telegram) and ideally provide a way to integrate the first part with other systems, possibly written in other languages. For example, one could send the flats to another service which maintains a database, on top of which other filtering or notification functionality can be built.
