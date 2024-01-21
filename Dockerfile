FROM pytorch/pytorch:latest

ENV TZ=Europe/London \
    DEBIAN_FRONTEND=noninteractive

ENV PIP_DEFAULT_TIMEOUT=180

RUN apt-get update
RUN pip install --upgrade pip

RUN pip install --retries 10 sentence-transformers
RUN python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('intfloat/multilingual-e5-large')"

RUN pip install --retries 10 numpy
RUN pip install --retries 10 scikit-learn==1.3.2

RUN mkdir /app
WORKDIR /app
COPY server.py .
COPY run.sh .
COPY svm_model.joblib .

#ENTRYPOINT ["/bin/bash"]
ENTRYPOINT ["/bin/bash", "run.sh"]

