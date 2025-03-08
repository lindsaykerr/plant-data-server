# from the app module import the create_app function which acts as the application factory
# return a new flask app object
from app import create_app
app = create_app()



# if the app is running as the main program, the app.run() method will run the app
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=7070, debug=True)


