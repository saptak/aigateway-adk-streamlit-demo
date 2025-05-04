FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit app
COPY ./streamlit_app /app

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
