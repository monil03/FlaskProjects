# Flask CRUD Application

This is a simple CRUD (Create, Read, Update, Delete) application built with Flask and MongoDB. The application allows users to add, retrieve, update, and delete user data stored in a MongoDB database.

## Features

- **Add User Data**: Add a user's name, phone number, and address.
- **Retrieve User Data**: Fetch and display user details by name.
- **Update User Data**: Update a user's phone number and address.
- **Delete User Data**: Remove a user's data from the database.

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML, CSS
- **Template Engine**: Jinja2

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Install dependencies**:
    Make sure you have Python 3.x installed. Install the required Python packages using pip:
    ```bash
    pip install flask pymongo
    ```

3. **Start MongoDB**:
    Ensure MongoDB is installed and running on your local machine. By default, this app connects to `mongodb://localhost:27017/`.

4. **Run the application**:
    ```bash
    python main.py
    ```
    The application will be accessible at `http://127.0.0.1:5000/`.

## File Structure
```bash
.
├── main.py                # The main Flask application
├── templates/             # HTML templates
│   ├── index.html         # Home page
│   ├── adddata.html       # Form for adding data
│   ├── getdata.html       # Display retrieved data
│   ├── updatedata.html    # Form for updating data
│   ├── success.html       # Success message page
│   ├── error.html         # Error message page
└── README.md              # Documentation for the project
```


## Routes

| Route                  | Method | Description                                           |
|------------------------|--------|-------------------------------------------------------|
| `/`                    | `GET`  | Home page with navigation options.                    |
| `/post/`               | `GET`  | Displays the form to add new user data.               |
| `/postdata/`           | `POST` | Submits and saves new user data to the database.      |
| `/get/?fname=<name>`   | `GET`  | Retrieves and displays user data by name.             |
| `/update/?uname=<name>`| `GET`  | Displays the form to update a user's details.         |
| `/updatedata/`         | `POST` | Updates user details in the database.                 |
| `/delete/?dname=<name>`| `GET`  | Deletes user data by name.                            |

## Usage

1. Navigate to the home page at `http://127.0.0.1:5000/`.
2. Use the buttons to add, retrieve, update, or delete data.
3. Follow the instructions on the respective pages.

## Screenshots

### Home Page
<img width="320" height="400" alt="image" src="https://github.com/user-attachments/assets/485e0bb1-74ee-4d8c-ace2-6c37059571aa">

### Add Data
<img width="320" height="300" alt="image" src="https://github.com/user-attachments/assets/7e55b807-59a2-420a-bd81-1459b0ec5d6e">

### View Data
<img width="320" height="200" alt="image" src="https://github.com/user-attachments/assets/dd5868f3-2e7f-404c-b524-08bfeb360076">

### Update Data
<img width="320" height="200" alt="image" src="https://github.com/user-attachments/assets/2f48b958-a688-4b9a-8b74-d2d3e1e752b5">

### Delete Data
<img width="320" height="150" alt="image" src="https://github.com/user-attachments/assets/fafa22de-8dd5-44e8-a756-0dc10a748eac">



## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue to discuss your ideas first.

---

Happy Coding!

