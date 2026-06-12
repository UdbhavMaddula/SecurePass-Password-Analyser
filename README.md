# SecurePass

A Password Security Assessment Tool built using Streamlit and zxcvbn that helps users analyze password strength, identify security risks, and receive actionable recommendations for creating safer passwords.

---

## Overview

SecurePass is designed to promote cybersecurity awareness by providing real-time password analysis. It combines the industry-standard zxcvbn password strength estimator with custom security logic to evaluate passwords beyond simple complexity checks.

The tool highlights potential attack vectors, provides recommendations for improvement, and educates users about secure password practices.

---

## Features

### Password Strength Analysis
- Evaluates password strength using zxcvbn.
- Displays strength levels:
  - Weak
  - Medium
  - Strong
  - Very Strong

### Security Score
- Generates a security score out of 100.
- Uses custom scoring logic with bonuses and penalties.

### Estimated Crack Time
- Shows estimated offline crack time.
- Helps users understand the real-world resistance of their passwords.

### Password Checklist
Checks whether the password contains:

- Minimum 8 characters
- Minimum 12 characters
- Uppercase letters
- Lowercase letters
- Numbers
- Special characters

### Attack Awareness
Identifies common attack risks such as:

- Dictionary Attacks
- Sequential Pattern Attacks
- Social Engineering Risks
- Brute Force Attacks
- Personal Information Guessing

### Security Recommendations
Provides personalized suggestions to improve password quality.

### Cybersecurity Awareness
Displays rotating cybersecurity best practices and tips.

### User-Friendly Interface
- Built with Streamlit.
- Clean responsive layout.
- Custom CSS styling.

---

## Technologies Used

- Python
- Streamlit
- zxcvbn
- Pandas
- Regular Expressions (re)

---

## Project Structure

```
SecurePass/
│
├── app.py
├── requirements.txt
├── README.md
└── screenshots/
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/UdbhavMaddula/SecurePass-Password-Analyser.git
```

Navigate into the project directory:

```bash
cd SecurePass-Password-Analyser
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## Example Use Cases

### Weak Password

Password:

```
password123
```

Possible Output:

- Weak Password
- High Risk
- Dictionary Attack
- Sequential Pattern Attack

---

### Strong Password

Password:

```
N3v3r_Gu3ss_MyP@ss!
```

Possible Output:

- Very Strong Password
- Minimal Risk
- Long Crack Time

---

## Educational Objective

SecurePass was developed as an educational cybersecurity project to increase awareness about password hygiene and common attack techniques.

It demonstrates how security tools can combine usability with practical defensive guidance.

---

## Future Enhancements

Potential improvements include:

- Password breach checking using Have I Been Pwned API
- PDF report generation
- Password history analysis
- Exportable assessment reports
- Password generation feature
- Deployment on Streamlit Community Cloud

---

## Author

**Udbhav Maddula**

Cybersecurity Student | Chess Player | Aspiring Security Professional

GitHub:
https://github.com/UdbhavMaddula

---

## License

This project is intended for educational and portfolio purposes.

Feel free to fork, learn from, and improve upon it.
