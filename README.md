# AI Attendance Management System

An AI-powered attendance management system that uses Face Recognition and Voice Recognition to automate student attendance. The application provides separate dashboards for teachers and students, making attendance tracking faster, secure, and efficient.

## Features

- AI-based Face Recognition attendance
- Optional Voice Recognition verification
- Teacher registration and login
- Student registration using face and voice
- Subject creation and enrollment
- Automatic attendance logging
- Student attendance dashboard
- Teacher dashboard with attendance records
- Supabase cloud database integration
- Streamlit-based interactive web interface

## Tech Stack

- Python
- Streamlit
- OpenCV
- NumPy
- Pillow
- Scikit-learn
- Supabase
- PostgreSQL
- bcrypt

## Project Structure

```
ai-attendance-project-app/
│
├── src/
│   ├── components/
│   ├── database/
│   ├── pipelines/
│   ├── screens/
│   └── ui/
│
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
```

## Installation

Clone the repository

```bash
git clone https://github.com/Zabi1817/ai-attendance-project-app.git
```

Go to the project folder

```bash
cd ai-attendance-project-app
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

## Environment Variables

Create a `.streamlit/secrets.toml` file and add:

```toml
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"
```

## Database

This project uses Supabase PostgreSQL for storing:

- Teacher profiles
- Student profiles
- Face embeddings
- Voice embeddings
- Subjects
- Subject enrollments
- Attendance logs

## Future Improvements

- QR Code attendance
- Mobile application
- Email notifications
- Attendance analytics dashboard
- Multi-factor authentication
- Live classroom monitoring

## Author

Md Zabiulla

Artificial Intelligence & Machine Learning Engineering Student

## License

This project is developed for educational and learning purposes.
