FROM mageai/mageai:0.9.66

# Note: this overwrites the requirements.txt file in your new project on first run. 
# You can delete this line for the second run :) 
COPY docker/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV PROJECT_NAME=money_diaries
ENV MAGE_CODE_PATH=/home/mage_code
ENV USER_CODE_PATH=${MAGE_CODE_PATH}/${PROJECT_NAME}

WORKDIR ${MAGE_CODE_PATH}

# Create the destination directory
RUN mkdir -p ${USER_CODE_PATH}

# Copy files from the host to the container
COPY mage_data ${USER_CODE_PATH}

