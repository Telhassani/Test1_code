import streamlit_authenticator as stauth
import pickle
from pathlib import Path

names = ["Chaiema Benour"]
usernames = ["C.Benour"]
passwords = ["1234"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
