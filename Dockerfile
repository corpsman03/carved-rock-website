# Use an official Hugo image as the base image
FROM klakegg/hugo:0.92.1-ext-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Hugo site source code to the container
COPY . .

# Build the Hugo site
RUN hugo

# Expose port 1313, which is the default Hugo server port
EXPOSE 1313

# Command to run the Hugo server
CMD ["hugo", "server", "--bind", "0.0.0.0"]
