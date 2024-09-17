# appointment
## Prerequisites
- Python 3.x
- Django
- PostgreSQL
- pgAdmin (optional, for database management)
you can see in requirement.txt for details

## Installation

Follow the steps below to set up the project locally:

### Step 1: Clone the Repository

```bash
git clone https://github.com/jafekri/appointment.git
```
### Step 2: Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### Step 3: Install Dependencies
```bash 
pip install -r requirement.txt
```
### Step 4:Configure Local Settings
Create a file named .env in the root directory to set up database parameters and the SECRET_KEY. Here is an example of what the local_settings.py file should contain:
```bash
SECRET_KEY = 'django-insecure*****************'

insert your database information in [../.env] file like this:
DATABASE_URL='postgres://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/DATABASE_NAME'

```
### Step 5: Apply Migrations
Run the following commands to apply the migrations and set up the database tables:
```
python manage.py makemigrations
python manage.py migrate
```
### Step 6: Run the Development Server
Start the Django development server:
```
python manage.py runserver
```
Open your browser and navigate to http://127.0.0.1:8000/ to access the application.