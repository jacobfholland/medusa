# Medusa
Medusa is a powerful Python framework designed to simplify and accelerate your web application development. It offers modular database usage and web routing functionality, making it an ideal choice for a wide range of Python applications. With Medusa, you can hit the ground running, eliminating the need for extensive prerequisite setup and enabling you to focus on building your application.


## Two Main Components: Database and Server
Medusa consists of two powerful main components: the **Database** and the **Server**. These components can be used independently to cater to your specific project needs or seamlessly combined to create a comprehensive web application.

### Database
The **Database** component is responsible for managing all database-related operations and functionality. It simplifies the process of working with databases by offering the following features:

- **Data Models**: Define your data models effortlessly using Python classes. Medusa automates the generation of database tables based on these models.

- **CRUD Operations**: Perform Create, Read, Update, and Delete (CRUD) operations on your data models with ease. Medusa streamlines database interactions, reducing boilerplate code.

- **Modular and Extensible**: The Database component is designed to be modular and extensible. You can add custom data models and extend functionality as your project demands.

### Server
The **Server** component handles all aspects related to API endpoints and web server functionality. It simplifies the process of setting up and managing web routes and is packed with features:

- **Web Routing**: Define API endpoints, web pages, and routes with minimal effort. Medusa's Server component makes it easy to structure your web application.

-  **Cross-functionality**: Used in combination with the Database component, the Server component auto-generates base-level Model endpoints, simplifying common operations like Create, Read, Update, and Delete (CRUD) for your data models. This automation reduces repetitive code and speeds up your development process.

- **Modular Design**: The Server component follows a modular design, allowing you to add, remove, or override routes as needed. This makes it easy to adapt your application to changing requirements.

## Easy to Use
### Mix and Match
One of the key advantages of Medusa is its flexibility. You can use the Database and Server components individually or together, depending on your project's needs. Whether you're building a database-driven application, a RESTful API, or a dynamic web application, Medusa has you covered.

### Easy Configuration
Medusa provides a simple way to configure and control these components using environment variables. Check out the [Environment Variables](/docs/environment_variables.md) section to learn more about how to customize and fine-tune your Medusa environment.

## Full Documentation

For comprehensive information, detailed guides, and in-depth documentation about Medusa, please refer to our official documentation:

[**Medusa Documentation**](#)

Our documentation covers everything you need to know about using Medusa, including installation instructions, getting started guides, detailed component documentation, and advanced usage scenarios.

## Getting Started

Welcome to Medusa! Follow these simple steps to get started with our Python framework.

### Prerequisites

Before you begin, make sure you have the following prerequisites installed on your system:

- [Python](https://www.python.org/downloads/): Medusa is a Python framework, so you'll need Python installed.

### Installation

1. **Clone the Repository**

   First, clone the Medusa repository to your local machine using Git:

   ```bash
   git clone https://github.com/your-username/medusa.git
   ```

2. **Navigate to the Project Folder**

    Change your current directory to the project folder:

    ```bash
    cd medusa
    ```

3. **Install Dependencies**

    Medusa relies on various Python packages. To install these dependencies, use pip and the provided requirements.txt:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the Application**

    You can create a `.env` file anywhere in the project directory. Or you can rename `.env-example` in the project directory to just `.env`. Fill out your environment variables accordingly.

5. **Run the Application**
    
    You can now run the application with the following command

    ```bash
    python3 run.py
    ```
    
    This command will connect the database and start the web server is they are enabled in the environment variables