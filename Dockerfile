FROM public.ecr.aws/lambda/python:3.9

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv && pipenv install --system

COPY hello_world ./

CMD ["app.lambda_handler"]
