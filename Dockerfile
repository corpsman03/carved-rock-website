# Build stage: install Hugo and generate the static site
FROM alpine:3.18 AS builder

# Set Hugo version and arch to match the target platform
ARG HUGO_VERSION=0.120.4
ARG HUGO_ARCH=Linux-ARM64

# Install dependencies needed to download and extract Hugo
RUN apk add --no-cache curl tar xz dpkg

WORKDIR /src

# Download and extract the Hugo binary for the current architecture
RUN curl -fsSL "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_${HUGO_ARCH}.deb" -o /tmp/hugo.deb \
  && dpkg -x /tmp/hugo.deb /tmp/hugo \
  && mv /tmp/hugo/usr/local/bin/hugo /usr/local/bin/hugo \
  && chmod +x /usr/local/bin/hugo

# Copy source and build
COPY . .
RUN hugo mod get && hugo

# Final stage: serve the generated site using a small web server
FROM nginx:1.25-alpine

COPY --from=builder /src/public /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
