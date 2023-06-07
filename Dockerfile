FROM public.ecr.aws/lambda/python:3.9

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv && pipenv install --system

COPY screenshot_api ./
#RUN mkdir tmp

CMD ["app.lambda_handler"]
