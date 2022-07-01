FROM python:3

COPY . .

RUN pip install -r requirements.txt

CMD python -u ./back_end/processor.py