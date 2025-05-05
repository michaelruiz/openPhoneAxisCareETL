FROM node:20

WORKDIR /app

# Install dependencies
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Copy source
COPY frontend/ .

# Run dev server (for development use)
CMD ["npm", "run", "dev"]
