# Use the lightweight alpine image
FROM python:3.8-alpine

# Installing needed packages
RUN pip install flask waitress requests

# Defining the working directory
WORKDIR /usr/src/app

# Adding needed files
COPY car_inventory.py ./

# Exposing the port used to communicate
EXPOSE 8081

# Command to run when executed
CMD ["python","car_inventory.py"]

