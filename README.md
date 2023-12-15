# ExpenSync - Expense Tracking App

## Overview

Expense Tracker is a web application powered by Django, designed to simplify the management and tracking of personal expenses. With user authentication for secure access, it allows users to effortlessly add, edit, and delete expenses, categorize them for better analysis, and generate insightful reports. The responsive design ensures a seamless experience across devices, providing users with a comprehensive tool to gain control over their financial activities.

## Features

- **User Authentication:** Securely manage your expenses with user authentication.
- **Expense Entry:** Easily add, edit, and delete your expenses.
- **Category Management:** Categorize your expenses to better analyze your spending patterns.
- **Reports:** Reports to visualize your expenses over time.
- **Responsive Design:** Access your expense data on any device with a responsive user interface.

## Installation

### Prerequisites

Make sure you have the following installed on your machine:

- Python (3.6 and above)
- Django

### Steps
1. Clone the repository:

   ```bash
   git clone https://github.com/F0laf0lu/ExpenSync.git

   
2. Change into ExpenSync directory:

     ```bash
   cd ExpenSync

3. Install dependecies:

    ```bash
   pip install -r requirements.txt

4. Apply database migrations:

    ```bash
    python manage.py make makemigrations
    python manage.py migrate

5. Create a superuser account:

     ```bash
   python manage.py createsuperuser

6. Run the development server:

    ```bash
     python manage.py runserver

7.  Open your browser and navigate to http://127.0.0.1:8000/ to access the Expense Tracker.

## Usage

- Log in using the superuser credentials created during installation.
- Click on new entry button on the dashboard to add transactions.
- View all transactions in the transactions page
- Explore other features such as category management and reports.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvement, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
  
