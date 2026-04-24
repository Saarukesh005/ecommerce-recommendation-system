from pyngrok import ngrok
import os

public_url = ngrok.connect(8501)
print(public_url)

os.system("streamlit run app.py")