# create an image from an environment
FROM python:3.10.6-buster

WORKDIR /fit_tes_courses

# RUN run terminal command
COPY fit_tes_courses fit_tes_courses
COPY preproc_data preproc_data
COPY raw_data raw_data
COPY requirements_prod.txt requirements_prod.txt
COPY setup.py setup.py

# RUN pip install -r requirements_prod.txt
RUN pip install .

EXPOSE 8080
# CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8080"] #$PORT
CMD ["uvicorn", "fit_tes_courses.app.api:app", "--host", "0.0.0.0", "--port", "8080"]
