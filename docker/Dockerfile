FROM ubuntu:24.04

SHELL ["/bin/bash", "-exo", "pipefail", "-c"]
ENV DEBIAN_FRONTEND=noninteractive
# Override with --build-arg URVC_ACCELERATOR=cpu for CPU-only deployments.
ARG URVC_ACCELERATOR=cuda
ENV URVC_ACCELERATOR=${URVC_ACCELERATOR}

WORKDIR /app
COPY . .

RUN --mount=type=tmpfs,target=/var/lib/apt/lists \
	--mount=type=tmpfs,target=/var/cache/apt/archives \
	apt-get update && \
	apt-get install -y --no-install-recommends sudo wget curl && \
	./urvc docker-bootstrap

ENTRYPOINT ["./urvc", "cli"]
CMD ["--help"]
