FROM minasonbol/moneydiaries:magedlt

ENV PROJECT_NAME=money_diaries
ENV MAGE_CODE_PATH=/home/mage_code
ENV USER_CODE_PATH=${MAGE_CODE_PATH}/${PROJECT_NAME}

WORKDIR ${MAGE_CODE_PATH}

# Create the destination directory
RUN mkdir -p ${USER_CODE_PATH}

# Copy files from the host to the container
COPY mage_data ${USER_CODE_PATH}