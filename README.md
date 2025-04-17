# Math Game Project

A simple web-based math game built with Flask, PostgreSQL, and a modern CI/CD pipeline. Players solve addition problems with numbers from 0 to 10, tracking their scores and answer times. The project showcases robust software engineering practices, including automated testing, linting, security scanning, and a visually appealing neumorphic CSS design, making it a strong portfolio piece for demonstrating full-stack development skills.

## Features

- **Game Mechanics**: Players enter their name and solve random addition problems (0-10 range). Scores and answer times are recorded for each attempt.
- **Database**: PostgreSQL stores player data, game sessions, and attempt times, with SQLite support for testing.
- **Frontend**: Responsive design with neumorphic styling, featuring soft shadows, rounded elements, and a calming color palette.
- **Backend**: Flask handles routing, session management, and database interactions, with logging for debugging.
- **Deployment**: Containerized with Docker and deployed via Terraform and Ansible to Azure Container Apps.

## Tech Stack

- **Backend**: Python, Flask, PostgreSQL, SQLite (for testing)
- **Frontend**: HTML, CSS (neumorphic design), Jinja2 templating
- **DevOps**: Docker, Docker Compose, GitHub Actions, Terraform, Ansible
- **Testing & Linting**: unittest, Pylint, Bandit
- **CI/CD**: GitHub Actions for automated building, testing, linting, and deployment

## Getting Started

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- PostgreSQL (or use the provided Docker Compose setup)
- GitHub account for CI/CD integration
- Azure account for deployment (optional)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/math-game.git
   cd math-game
