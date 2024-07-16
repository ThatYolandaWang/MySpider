# FROM python:3.7
# LABEL org.opencontainers.image.source="https://github.com/thatyolandawang/myspider"
# WORKDIR /app
# ADD . .

# RUN pip install -r ./myspider/requirements.txt

# CMD [ "python", "./myspider/start.py"]
#ENTRYPOINT ['python3', '/app/myspider/start.py']

FROM public.ecr.aws/lambda/python:3.10

# Copy function code
COPY . ${LAMBDA_TASK_ROOT}
RUN pip install awslambdaric
RUN pip install -r ./requirements.txt
# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]