# SharkTank Project

Welcome to the **SharkTank Project**! This is a Django-based web application designed to simulate the popular TV show "Shark Tank." Entrepreneurs pitch their business ideas to investors (Sharks) in hopes of securing funding.

## Features

- User authentication (signup, login, logout)
- Entrepreneurs can create profiles and submit business ideas
- Admin panel to manage users, business ideas, and investments
- Responsive UI with custom styling and animations

## Prerequisites

Before setting up the project locally, ensure you have the following installed:

- **Python 3.x** (preferably Python 3.8 or newer)
- **Django** (installed using `pip`)
- **MySQL** (for database management)
- **Git** (for version control)
- **Node.js** (for frontend dependencies)

## Setup Instructions

Follow these steps to get the project up and running on your local machine:

### 1. Clone the repository 
Clone the repository from GitHub to your local machine:

```bash
git clone https://github.com/Bhavyadhan26/SymbiSharkTank.git
cd Miniproject
```
### 2. Install dependencies
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```
### 3. Set up the database
Create the necessary database and configure the database settings in settings.py. Ensure MySQL is running locally or use a remote database.

Ensure your MySQL database is created and configured with the correct settings in settings.py.
```bash
python manage.py migrate
```
### 4.Set up the environment variables
Create a .env file in the root directory of the project and add the necessary environment variables (such as database credentials, secret keys, etc.). 
Here's an example of what to include in .env:


```bash
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=sharktank
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```
You can refer to .env.example as a template.

### 6. Run the project
Now you can run the Django development server:

```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000/ in your web browser to see the project in action.

