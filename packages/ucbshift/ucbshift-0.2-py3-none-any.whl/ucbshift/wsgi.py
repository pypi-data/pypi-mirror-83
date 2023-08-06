#This file tells the Gunicorn server how to interact with the application.

from ucbshift.apps.index import server

if __name__ == "__main__":
	server.run()
