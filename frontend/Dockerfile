# Use an official Node runtime as the base image
FROM node:18-alpine

# Install necessary dependencies
RUN apk add --no-cache libc6-compat

# Create a non-root user
RUN adduser -D myuser

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

# Build the app
RUN npm run build

# Change ownership of the app directory to the non-root user
RUN chown -R myuser:myuser /app

# Switch to the non-root user
USER myuser

# Expose port 3000
EXPOSE 3000


