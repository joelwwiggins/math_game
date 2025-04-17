Math Game Project

A simple web-based math game built with Flask, PostgreSQL, and a modern CI/CD pipeline. Players solve addition problems with numbers from 0 to 10, tracking their scores and answer times. The project showcases robust software engineering practices, including automated testing, linting, security scanning, and a visually appealing neumorphic CSS design, making it a strong portfolio piece for demonstrating full-stack development skills.

Features





Game Mechanics: Players enter their name and solve random addition problems (0-10 range). Scores and answer times are recorded for each attempt.



Database: PostgreSQL stores player data, game sessions, and attempt times, with SQLite support for testing.



Frontend: Responsive design with neumorphic styling, featuring soft shadows, rounded elements, and a calming color palette.



Backend: Flask handles routing, session management, and database interactions, with logging for debugging.



Deployment: Containerized with Docker and deployed via Terraform and Ansible to Azure Container Apps.

Tech Stack





Backend: Python, Flask, PostgreSQL, SQLite (for testing)



Frontend: HTML, CSS (neumorphic design), Jinja2 templating



DevOps: Docker, Docker Compose, GitHub Actions, Terraform, Ansible



Testing & Linting: unittest, Pylint, Bandit



CI/CD: GitHub Actions for automated building, testing, linting, and deployment

Getting Started

Prerequisites





Python 3.8+



Docker and Docker Compose



PostgreSQL (or use the provided Docker Compose setup)



GitHub account for CI/CD integration



Azure account for deployment (optional)

Installation





Clone the Repository:

git clone https://github.com/your-username/math-game.git
cd math-game



Set Up Environment Variables: Create a .env file in the project root with the following:

POSTGRES_DB=math_game
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=your_secret_key



Run with Docker Compose:

docker-compose up --build

The app will be available at http://localhost:8080.



Run Locally (without Docker):

pip install -r requirements.txt
python -m app

Ensure PostgreSQL is running and configured with the .env variables.

CI/CD Pipeline

The project leverages GitHub Actions for a robust CI/CD pipeline, ensuring code quality and automated deployment:





Build: On push or pull request to the main branch, Docker images are built using Docker Buildx with layer caching for efficiency.



Testing: Runs unittest suite (tests/test_app.py) to verify app functionality, using an in-memory SQLite database for isolation.



Linting: Executes Pylint on app.py to enforce Python coding standards.



Security Scanning: Uses Bandit to detect potential security vulnerabilities in the codebase.



Deployment:





Build & Push: Ansible playbook (ansible/deploy_container.yml) builds and pushes the Docker image to Azure Container Registry.



Infrastructure: Terraform (terraform/) provisions Azure Container Apps, Log Analytics, and other resources.



Triggered on push to main or manual workflow dispatch.

The pipeline is defined in main.yml (CI) and mathgamecontainer-AutoDeployTrigger-*.yml (CD), with secrets stored securely in GitHub.

Testing

The test suite (tests/test_app.py) uses unittest to validate core functionality:





Index Page: Verifies the welcome page loads correctly.



Game Page: Ensures the game interface displays with player name and math problem.



Results Page: Confirms score and answer times are displayed after gameplay.

Run tests locally:

python -m unittest discover -s tests

Or via Docker:

docker-compose run web python -m unittest discover -s tests

Linting & Security





Pylint: Enforces code quality with consistent style and error detection.

docker-compose run web pylint app.py



Bandit: Scans for security issues like hardcoded credentials or unsafe functions.

docker-compose run web bandit -r . -ll

CSS Styling

The frontend uses a neumorphic design (static/style.css) to create a modern, tactile UI:





Custom Properties: Defines variables for colors, shadows, and accents for easy theming.



Neumorphism: Combines inset and outset box-shadows for a soft, 3D effect on buttons, inputs, and containers.



Responsive Design: Uses flexbox and max-width containers for mobile-friendly layouts.



Background: Features a fixed, cover-sized background image for visual appeal.



Interactive Elements: Buttons and inputs have smooth hover transitions and consistent rounded aesthetics.

Example styling for buttons:

.btn {
    padding: 10px 20px;
    border-radius: 50px;
    background: var(--background);
    box-shadow: 5px 5px 10px var(--shadow-dark), -5px -5px 10px var(--shadow-light);
    transition: all 0.3s ease;
}
.btn:hover {
    box-shadow: inset 5px 5px 10px var(--shadow-dark), inset -5px -5px 10px var(--shadow-light);
}

Deployment

The app is deployed to Azure Container Apps using:





Terraform: Defines infrastructure (terraform/), including resource groups, container app environments, and Log Analytics.



Ansible: Automates Docker image building and pushing to Azure Container Registry (ansible/deploy_container.yml).



GitHub Actions: Orchestrates the deployment process, triggered on code push or manual trigger.

To deploy manually:





Configure Azure secrets in GitHub (e.g., REGISTRY_SERVER, RESOURCE_GROUP).



Run the mathgamecontainer-AutoDeployTrigger-*.yml workflow via GitHub Actions.

Project Structure

math-game/
├── ansible/                   # Ansible playbooks for image building
├── static/                    # CSS and static assets
│   └── style.css             # Neumorphic styling
├── templates/                 # Jinja2 templates
│   ├── index.html            # Home page
│   ├── game.html             # Game interface
│   └── results.html          # Results page
├── tests/                     # Test suite
│   └── test_app.py           # Unit tests
├── terraform/                 # Terraform infrastructure
├── app.py                     # Main Flask application
├── docker-compose.yml         # Docker Compose configuration
├── main.yml                   # CI pipeline
├── mathgamecontainer-*.yml    # CD pipeline
└── README.md                  # This file

Contributing





Fork the repository.



Create a feature branch (git checkout -b feature/YourFeature).



Commit changes (git commit -m 'Add YourFeature').



Push to the branch (git push origin feature/YourFeature).



Open a pull request.

License

This project is licensed under the MIT License.
