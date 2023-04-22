"""
Main entrypoint for the project

Immediately scrapes the configured Album
"""

from src.webscrapper import start

if __name__ == '__main__':
    start()
