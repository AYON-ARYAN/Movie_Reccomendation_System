import streamlit_authenticator as stauth

hashed_pw = stauth.Hasher(['moodix123']).generate()
print(hashed_pw)
