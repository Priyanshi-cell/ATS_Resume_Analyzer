# ATS_Resume_Analyzer

📄 Project Description
This is an all-in-one tool for the best learning and applying rules to the job application journey.

No rejection or no weakness is a loss anymore; get ready for the specific job role and get a personalized roadmap.

Highlight your strengths.

Polish your weaknesses.

Calculate your percentage match with the job role.

Get ready to make changes.

🛠️ Tech Stack
Frontend: Streamlit

Styling: Custom CSS (Animations, Grids, Modern UI)

AI Engine: Google Gemini API (specifically the gemini-flash-latest model for speed)

PDF Processing: PyMuPDF (fitz) for fast and accurate text extraction.

Core Language: Python 3.x

Environment Management: python-dotenv

🚀 Getting Started
Follow these simple steps to get the ATS Resume Analyzer running on your machine.

1. Get the Code

First, clone the repository to your local computer and navigate into the project folder.

git clone [https://github.com/your-username/ATS-Resume-Analyzer.git](https://github.com/your-username/ATS-Resume-Analyzer.git)
cd ATS-Resume-Analyzer

2. Set Up Your Environment

Create a virtual environment to keep all the project's packages neatly organized, then activate it.

# Create and activate the environment
python -m venv venv
venv\Scripts\activate

Next, install all the necessary libraries from the requirements.txt file.

# Install dependencies
pip install -r requirements.txt

3. Add Your API Key

You'll need a Google Gemini API key to power the AI features.

Create a new file in the main project folder named .env.

Open the file and add your key like this:

GOOGLE_API_KEY="YOUR_SECRET_API_KEY_HERE"

4. Launch the App!

You're all set. Run the command below to start the application.

streamlit run app.py

Your web browser should automatically open a new tab with the app running.

