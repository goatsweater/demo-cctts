FROM python:3-slim

# Update the base image
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y upgrade \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade --no-cache-dir --disable-pip-version-check setuptools==65.5.1

# Create a space to work in
WORKDIR /app

RUN addgroup --gid 1001 --system app && \
    adduser --shell /bin/false --disabled-password --uid 1001 --system --group app && \
    chown -R app:app /app

USER app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the scripts into the container
COPY src/*.py .

CMD [ "python" ]