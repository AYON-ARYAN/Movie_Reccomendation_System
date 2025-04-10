📦 Movie Recommendation Web App Setup Guide
-------------------------------------------

👨‍💻 Created By: Ayon Aryan

🛠️ Requirements:
---------------
This app uses:
- Flask for backend & routing
- Streamlit for UI (optional)
- Scikit-learn for cosine similarity & TF-IDF
- Pandas, Numpy for data handling
- SQLAlchemy for database interactions
- YAML for config files
- streamlit-authenticator for user login
- Werkzeug for password hashing

📂 Project Setup:
-----------------

1. 🔧 Create a virtual environment (recommended):

   Windows:
   > python -m venv venv
   > venv\Scripts\activate

   macOS/Linux:
   $ python3 -m venv venv
   $ source venv/bin/activate

2. 📦 Install all dependencies:

   > pip install -r requirements.txt

3. 🚀 Run your Flask app:

   > python app.py

4. (Optional) Run your Streamlit interface:

   > streamlit run app.py

📝 Notes:
--------
- Make sure your `recommender.py` file exists and is in the correct folder.
- Keep your `.yaml` file (for authentication) in the root or update the path accordingly.
- Use `pip freeze > requirements.txt` after changes to keep dependencies up to date.

💬 Any issues? Debug with:
> pip list
> python --version
> streamlit --version

---

Enjoy building something awesome 🚀
