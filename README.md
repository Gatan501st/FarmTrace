# FarmTrace: A Web-Based System for Supply Tracking of Fertilizers in Real-Time across Kenya

## Project Overview
This project tracks the movement of fertilizer from the manufacturer to the farmer using blockchain technology to ensure authenticity and prevent tampering.

## Setup Instructions
1. Clone the repository
```sh
git clone https://github.com/yourusername/farmtrace.git
```

2. Navigate to the project directory
```sh
cd farmtrace
```

3. Create a virtual environment
```sh
python -m venv venv
```

4. Activate the virtual environment
- On Windows
  ```
  venv\Scripts\activate
  ```
- On macOS/Linux
  ```
  source venv/bin/activate
  ```

5. Install the dependencies:
```sh
pip install -r requirements.txt
```

6. Set up the environment variables
```sh
export FLASK_ENV=development
export SECRET_KEY='your_secret_key'
export DATABASE_URL='sqlite:///site.db'
```

7. Initialize the database
```sh
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

8. Run the application
```sh
flask run
```

## Usage
1. Manufacturers can log the production of fertilizer batches.
2. Wholesalers can receive and verify batches.
3. Retailers can receive and sell batches to farmers.
4. Farmers can verify the authenticity of the purchased fertilizer.

## File Structure
- `app/`: Contains the application code.
- `__init__.py`: Initializes the Flask application.
- `models.py`: Defines the database models.
- `views.py`: Contains view functions and routes.
- `forms.py`: Defines Flask-WTF forms.
- `templates/`: Contains HTML templates.
- `static/`: Contains static files (CSS, JavaScript, images).
- `blockchain/`: Contains blockchain-related code.
- `utils/`: Contains utility functions.
- `migrations/`: Contains database migration files.
- `tests/`: Contains unit tests.
- `config.py`: Configuration settings for the Flask application.
- `manage.py`: Script to run administrative tasks.
- `requirements.txt`: Lists all Python libraries and dependencies needed for the application.
- `README.md`: Documentation file describing the project.

## Database Schema
- `User`: Stores user information.
- `Batch`: Stores fertilizer batch details.
- `Transaction`: Stores transaction details.
- `DigitalCertificate`: Stores digital certificate details.

## Blockchain Integration
- Each major participant operates a blockchain node.
- Nodes validate transactions and update the blockchain.
- QR codes/RFID tags are used for verification.

## Testing
Run the tests using:
```sh
pytest
```

## Deployment
Ensure that the environment variables are set correctly for production:
```sh
export FLASK_ENV=production
export SECRET_KEY='your_secret_key'
export DATABASE_URL='your_database_url'
```

## Contributing
1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## License
This project is licensed under the MIT License.
