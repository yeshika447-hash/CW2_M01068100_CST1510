# CST1510_GitHub
Student Name: Pooshita (Yeshika) Bhautoo
Student ID: M01068100
Course: CST1510 -CW2 - Multi-Domain Intelligence Platform

#Project description
This project is a comprehensive Streamlit-based analytical platform designed to support three professional domains:
   1. Cybersecurity
   2. Data Science
   3. IT Operations
It implements secure authentication, a structured SQLite database, OOP architecture, interactive visual analytics, and optional AI assistance.

# Week 7: Secure Authentication System
#Features overview
1. Password Hashing(Security)
   Using the bcrypt library the passwords are hashed before storing, so that they're not stored in plain text.
   During login, the password entered by user is verified against the stored hashed password.

2. User Registration
   The program collects username and password input.
   The program validates the username (ength should be betweem 3 and 30 and password should be of length 6-50).
   It also appends username and password to file users.txt.

3. Login user
   Prompts user for input.
   Reads all records from users.txt
   If user exists, login is successful.

#Technical implementation
1. Files and Variables
   Stores path for user data.
   bcrypt module is used for hashing

2. Password hashing functions
   Converts password into bytes
   Generates unique salt for each password
   Hashes the password and returns it as a UTF-8 string

3. Registration flow
   Hashes user's password before storing
   Appends user data to file
   Handles missing files and output error message

4. Login flow
   Reads stored data
   Check for match username
   Verify password for confirmation
   prints success or failure message

# Week 8 : Data pipeline and CRUD
# SQLite Database Layer
Includes relational tables for:
   1. users
   2. cyber_incidents
   3. datasets_metadata
   4. it_tickets

# Full Multi-Domain Dashboards (Tier 3)
The platform includes three fully developed dashboards, each solving a specific real-world problem:
1. Cybersecurity Dashboard
   - Phishing trend time-series
   - Severity distribution analytics
   - Resolution-time bottleneck detection
   - Interactive incident table + CRUD
2. Data Science Dashboard
   - Dataset size analysis
   - Row count distribution
   - Source dependency overview
   - Metadata CRUD operations
3. IT Operations Dashboard
   - Ticket resolution patterns
   - Staff performance anomaly detection
   - SLA breach analysis

# Week 9 : Web interface and Streamlit structure

# Week 10 : AI integration
AI Assistant
   - Integrates OpenAI API
   - Provides explanations, recommendations, and insights
   - Gives contextual advice based on dashboard interactions

# Week 11 : OOP (Optional)

# Technologies Used
   - Streamlit
   - SQLite
   - bcrypt
   - Pandas
   - Plotly
   - OpenAI/Gemini API
   - Python OOP Design Patterns (optional)
