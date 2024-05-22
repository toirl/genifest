FROM debian:bullseye-slim as base

WORKDIR /app
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install python3-pip
RUN pip install setuptools --upgrade

FROM base as develop
# Make sure we are installing the same versions
COPY docker/requirements.txt .
RUN pip install -r requirements.txt

FROM develop as build
# Build package
RUN apt-get install --no-install-recommends --assume-yes make
COPY . .
RUN make dist

FROM base as prod
COPY --from=build /app/dist/*.tar.gz ./
RUN pip install *.tar.gz

# Run the CLI as default entrypoint
ENTRYPOINT ["genifest"]
# Use CMD for default parameters of the client.
CMD []
