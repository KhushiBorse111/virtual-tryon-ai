FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the React app
RUN npm run build

# Use a simple server to serve the files
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Command to run the application
CMD ["nginx", "-g", "daemon off;"]