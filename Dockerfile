FROM python:3.9
WORKDIR /workspace
RUN pip install flask sqlalchemy flasgger
ADD project /workspace
RUN python init_db.py
CMD ["python","app.py"]