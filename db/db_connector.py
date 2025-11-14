from google.cloud import firestore
import os

def get_db():
    project_id = os.get("FIREBASE_PROJECT_ID")
    return firestore.client(project=project_id)