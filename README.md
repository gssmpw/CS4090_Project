# Team 18
Members: Gaven Smith, Chase Kempker, and Matthew Schepers

## Assigned Roles
Team Lead: Matthew Schepers

Documentation Lead: Gaven Smith

Developer: Chase Kempker, Matthew Schepers, and Gaven Smith

## Project Description
This is a full-stack software development project with the intention of developing a group scheduling service that allows users to view their upcoming events without the obstruction of events unrelated to them.

### User Role Descriptions
Users will be split into one of 4 roles - Event Organizer, Regular Member, Cross-Group Collaborator, and Faculty Advisor.

**Event Organizers** are responsible for creating and editing groups, adding new users to existing groups, and creating and editing new and existing events.

**Regular Users** are the default user, having the least amount of access to the service. These users can view their associated events, as well as receive notifications when events are created or edited.

**Cross-Group Collaborators** are similar to Regular Users, the sole difference being that they are associated with more than one event group.

**Faculty Advisors** provide oversight and guidance to event groups.

## Prerequisites

Before running this project, ensure you have the following installed on your computer:

### Node.js and npm
- **Node.js** (version 14.0 or higher recommended)
- **npm** (comes with Node.js)

To check if Node.js and npm are installed:
```bash
node --version
npm --version
```

If not installed, download from [nodejs.org](https://nodejs.org/)

### React
React will be installed automatically when you install the project dependencies (covered in the Installation section below).

### Python
- **Python 3.8 or higher**

To check if Python is installed:
```bash
python --version
# or
python3 --version
```

If not installed, download from [python.org](https://www.python.org/downloads/)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Python Dependencies
Navigate to the project root directory and install the required Python packages:
```bash
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

### 3. Install Frontend Dependencies
Navigate to the frontend folder and install React and other npm packages:
```bash
cd frontend
npm install
```

This will automatically install React and all other dependencies listed in `package.json`.

## Running the Project

To run the project, you need to start both the backend APIs and the frontend server.

### 1. Start the Backend APIs
Open three separate terminal windows/tabs and start each Python API:

**Terminal 1 - Group API:**
```bash
python group.py
# or
python3 group.py
```

**Terminal 2 - User API:**
```bash
python user.py
# or
python3 user.py
```

**Terminal 3 - Event API:**
```bash
python event.py
# or
python3 event.py
```

### 2. Start the Frontend Server
Open a fourth terminal window/tab, navigate to the frontend folder, and start the development server:
```bash
cd frontend
npm run dev
```

### 3. Access the Application
Once all services are running, open your browser and navigate to:
```
http://localhost:5173
```
(The exact port may vary - check your terminal output for the correct URL)

## Project Structure
```
project-root/
├── frontend/           # React frontend application
│   ├── src/
│   ├── package.json
│   └── ...
├── group.py           # Group management API
├── user.py            # User management API
├── event.py           # Event management API
├── requirements.txt   # Python dependencies
└── README.md
```

## Troubleshooting

### Port Already in Use
If you get an error that a port is already in use, you may need to:
- Stop any existing instances of the application
- Change the port in the configuration files
- Kill the process using that port

### Module Not Found Errors
If you encounter "module not found" errors:
- Ensure you've run `pip install -r requirements.txt`
- Ensure you've run `npm install` in the frontend directory
- Check that you're using the correct Python version

### React Not Working
If React isn't working properly:
- Delete the `node_modules` folder in the frontend directory
- Delete `package-lock.json`
- Run `npm install` again

### database issues
- The database is hosted on azure and works by allowing whitelisted ips to access it
- to get access please email ctk24b@umsystem.edu requesting it.