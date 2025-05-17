FROM node:18

# Create app directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# App runs on port 3000
EXPOSE 3000

# Start the app
CMD ["node", "app.js"]
