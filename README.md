# Attendance Tracker System with Face Detection

## Introduction

Welcome to the Attendance Tracker System with Face Detection! This system provides an efficient and automated way to track attendance using facial recognition technology. By leveraging computer vision algorithms, the system identifies individuals in real-time and records their attendance, eliminating the need for manual attendance-taking processes.

## Features

- **Face Detection:** Utilizes state-of-the-art face detection algorithms to identify individuals in images or live video streams.
- **Face Recognition:** Matches detected faces against a database of known individuals to accurately recognize and identify attendees.
- **Attendance Logging:** Records attendance data, including timestamps and the identities of attendees, in a centralized database.
- **Real-time Monitoring:** Provides real-time monitoring of attendance status, allowing administrators to track attendance as it happens.
- **Reporting:** Generates comprehensive reports and analytics on attendance patterns, trends, and statistics.

## Installation

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/garimasubedi/flask-attendanceMS.git
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up the database:

   ```
   flask --app flaskr init-db
   ```

4. Run the development server:

   ```
   flask --app flaskr run --debug
   ```

5. Access the system at `http://127.0.0.1:5000/` in your web browser.

## Usage

1. **User Registration:** Administrators can register users and enroll their faces in the system.
2. **Face Enrollment:** Users' faces are enrolled and stored in the system for recognition.
3. **Attendance Tracking:** Users' attendance is automatically tracked when their faces are detected by the system.
4. **Reporting:** Administrators can generate attendance reports and analyze attendance data.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [OpenCV](https://opencv.org/) - Open Source Computer Vision Library
- [dlib](http://dlib.net/) - C++ Library for Machine Learning & Computer Vision
