.. Medusa documentation master file, created by
   sphinx-quickstart on Sun Sep 17 17:23:36 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 2
   :caption: Packages:

   source/medusa.database
   source/medusa.server
   source/medusa.utils

Getting Started
===============

Welcome to Medusa! Follow these simple steps to get started with our Python framework.

Prerequisites
^^^^^^^^^^^^^

Before you begin, make sure you have the following prerequisites installed on your system:

- `Python <https://www.python.org/downloads/>`_: Medusa is a Python framework, so you'll need Python installed.

Installation
^^^^^^^^^^^^

1. **Clone the Repository**

   First, clone the Medusa repository to your local machine using Git::

       git clone https://github.com/your-username/medusa.git

2. **Navigate to the Project Folder**

   Change your current directory to the project folder::

       cd medusa

3. **Install Dependencies**

   Medusa relies on various Python packages. To install these dependencies, use pip and the provided requirements.txt::

       pip install -r requirements.txt

4. **Configure the Application**

   You can create a `.env` file anywhere in the project directory. Or you can rename `env-example` in the project directory to just `.env`. Fill out your environment variables accordingly. Be sure to double-check the entire file is named just `.env`, including the dot.

5. **Run the Application**

   You can now run the application with the following command::

       python3 run.py

   This command will connect the database and start the web server is they are enabled in the environment variables

.. _environment_variables: /docs/environment_variables.md
.. _documentation: #


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
