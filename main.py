from websocket import create_connection
import json, time
import requests
import random
import cloudscraper

scraper = cloudscraper.create_scraper(
    browser={
        'custom': 'ScraperBot/1.0',
    }
)
