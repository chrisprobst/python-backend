import argparse

# Prepare arguments when started from console
# and start webserver

from backend.start_webserver import start_webserver
start_webserver(
	"default_config.json",
	"myDatabase.db"
)