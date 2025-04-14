from dotenv import load_dotenv
import os

os.environ.clear()
load_dotenv(".env")
ENV = os.getenv("ENV")

print("ENV RUNNING:", ENV)
