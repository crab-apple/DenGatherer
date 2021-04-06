# DenGatherer

This project is mostly based on [Flathunter](https://github.com/flathunters/flathunter) (a bot that scrapes flat listing websites and sends notifications to telegram) and has the aim of expanding Flathunter's functionality in ways that may be a bit too drastic for it to be just a fork.

Right now the main goal is to decouple the scraping/info-gathering part of the project from the notifying part of it (the integration with telegram). Communication between them will happen through a pub/sub service (Redis). This will then allow to easily implement other consumers of the flat offerings data, possibly written in other languages.
