# __init__.py defines that app is a module and the create_app() function is the flask application factory
# In this module we import Flask and SQLAlchemy from the flask and flask_sqlalchemy modules respectively
import os, sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template, g
#from instance.app_config import Config



def create_app(test_config=True):

    # create a new flask app object within the context of the app module
    app = Flask(__name__)
    @app.after_request
    def add_cors_headers(response):
        """Adds CORS headers to every response."""
        response.headers['Access-Control-Allow-Origin'] = '*'  # Or your specific origin
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
        return response
    
    # the following will be used set default configurations for the app
    app.config.from_mapping(
        SECRET_KEY='dev', 
        DATABASE=os.path.join(os.path.realpath(''), 'instance', 'plant_data.db')
        )
    
    app.config['APPLICATION_ROOT'] = '/plant-server'
    
    """
    # ensure the instance folder exists and that it contains the database file
    def make_instance_folder(instance_path):
        try:
            os.makedirs(instance_path)
            # create the database file in the instance folder
            with open(os.path.join(instance_path, 'plant_data.db'), 'w') as f:
                pass

        except OSError:
            pass
            exit('Could not find instance folder, exiting...')

    # define the path to the instance folder
    instance_path = os.path.join(os.path.realpath(''), 'instance')
    print(f"Instance path: {instance_path}")

    # check if the instance folder exists, if not create it
    os.path.exists(instance_path) or make_instance_folder(instance_path)

    # create a new flask app object using the Flask constructor and the instance folder
    app = Flask(__name__, instance_path=instance_path)

    # the following will be used set default configurations for the app
    app.config.from_mapping(
        SECRET_KEY='dev', 
        DATABASE=instance_path + '/' + 'plant_data.db'
        )
    
    # when not in testing phase load a config object
    if test_config is None:
        app.config.from_mapping(test_config)
    
    else:
        # load the test config if passed in
        app.config.from_object(Config)
    
    print(f"Database path: {app.config['DATABASE']}")
    """

    # ensures that the database is initialized within the context of the app
    with app.app_context():
        # from parent directory import the db object   
        from . import db
        # initialize the database to the app
        database_path = app.config['DATABASE']
        if not os.path.exists(database_path):
            print("Database file does not exist")
            @app.route('/api/v1')
            def index():
                return render_template('error.html'), 404
            
            @app.route('/api/v1/submit', methods=['POST'])
            def submit_data():
                return jsonify({'error': 'Database file does not exist'}), 404
            
            @app.route('/api/v1/data/<plantid>/latest', methods=['GET'])
            def get_data(plantid):
                return jsonify({'error': 'Database file does not exist'}), 404

        else:    
            if os.stat(database_path).st_size == 0:
                print("Database file is empty, initializing the database")
                db.init_db()
        
        
            # ROUTES
            
            # submit data to the database
            @app.route('/api/v1/submit', methods=['POST'])
            def submit_data():
                # ensure that the sqlite3 connection is available to local conext variable g
                pdb = g.pdb = db.get_db()
                try:
                    data = request.json
                    value = data.get('value')
                    value = int(value)
                    if value is not None and 0 <= value <= 10:
                        c = pdb.cursor()
                        c.execute(
                            f'''
                            INSERT INTO moisture_reading (plant_id, reading, recorded_at) 
                            VALUES (
                                (SELECT id FROM plant WHERE name = 'Fred' LIMIT 1),
                                {value},
                                '{datetime.now()}'
                            );
                            ''')
                        pdb.commit()
                        print("Data submitted successfully")
                        return jsonify({'message': 'Data submitted successfully'}), 201
                    else:
                        return jsonify({'error': 'Invalid data'}), 400
                except sqlite3.Error as e:
                    print(f"Database error: {e}")
                    pdb.rollback() #rollback on error.
                    return jsonify({'error': 'Database error'}), 500
                finally:
                    pdb.close() #close the database connection.
                


            # get the latest plant state from the database
            @app.route('/api/v1/data/<plantid>/latest', methods=['GET'])
            def get_data(plantid):
                plantid = int(plantid)
                pdb = g.pdb = db.get_db();
                c = pdb.cursor()
                result = c.execute(f'''
                                    SELECT 
                                        name, 
                                        common_name, 
                                        species, 
                                        moisture_min,
                                        moisture_max, 
                                        moisture_ideal,
                                        reading,
                                        recorded_at 
                                        FROM plant
                                        JOIN moisture_reading
                                        ON plant.id = moisture_reading.plant_id
                                        WHERE plant.id = {plantid}
                                        ORDER BY recorded_at DESC
                                        LIMIT 1;
                                    ''')
                row = result.fetchone()
                data = {
                    'name': row[0],
                    'common_name': row[1],
                    'species': row[2],
                    'moisture_min': row[3],
                    'moisture_max': row[4],
                    'moisture_ideal': row[5],
                    'reading': row[6],
                    'recorded_at': row[7]
                }
                return  jsonify(data), 200 
            
            # resets the data collected in the testing database        
            @app.route('/ap1/v1/new/db', methods=['DELETE'])
            def reset_db():
                db.init_db()
                return jsonify({'message': 'Database reset successfully'}), 200

            # Provides informaiton the services resources
            @app.route('/api/v1')
            def index():
                return render_template('index.html')
            
            return app
