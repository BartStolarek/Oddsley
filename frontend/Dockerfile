# Use an official Node runtime as the base image
FROM node:18-alpine

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

# Expose port 3000
EXPOSE 3000

# Run the application
CMD ["npm", "run", "dev"]

