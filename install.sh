#!/bin/bash

# Enhanced installation script for Nuxt + Python project
# With password prompt and database initialization

set -e  # Exit on any error

echo "🚀 Starting installation process..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to handle errors gracefully
handle_error() {
    echo "❌ Error occurred in installation"
    exit 1
}

# Set trap for error handling
trap handle_error ERR

# 1. Enable and update all submodules
echo "📦 Updating Git submodules..."
if git submodule status | grep -q "^[+-]"; then
    echo "Found untracked submodules, initializing..."
    git submodule init
fi

git submodule update --recursive --remote

echo "✅ Submodules updated successfully"

# 2. Install JavaScript packages in client directory
echo "🔧 Installing JavaScript dependencies..."

cd client

if [ -f "package.json" ]; then
    echo "npm install..."
    npm install --verbose --include=dev
else
    echo "⚠️  No package.json found in client"
fi

# Return to project root
cd ../..

# 3. Install Python packages in server directory
echo "🐍 Installing Python dependencies..."

cd server

# Check if poetry is available
if command_exists "poetry"; then
    echo "Poetry found, installing with Poetry..."
    if [ -f "pyproject.toml" ]; then
        poetry install --with dev
    else
        echo "⚠️  No pyproject.toml found in server"
    fi
elif command_exists "pip"; then
    echo "Poetry not found, checking for requirements..."
    if [ -f "requirements.txt" ]; then
        echo "Installing from requirements.txt..."
        pip install -r requirements.txt
    elif [ -f "setup.py" ]; then
        echo "Installing from setup.py..."
        pip install .
    else
        echo "⚠️  No requirements.txt or setup.py found in server"
    fi
else
    echo "⚠️  Neither Poetry nor pip found. Please ensure Python dependencies are installed manually."
fi

# Return to project root
cd ..

echo "✅ Python dependencies installed successfully"

# 4. Prompt for first user password and initialize database
echo ""
echo "🔐 First User Setup"
echo "=================="
echo "For the first user, you'll need to set a password for the admin account."
echo "The admin user will be created as: admin@admin.com"
echo ""
read -s -p "Enter password for admin user (will not be shown): " admin_password
echo ""
read -s -p "Confirm password: " confirm_password
echo ""

# Verify passwords match
if [ "$admin_password" != "$confirm_password" ]; then
    echo "❌ Passwords do not match!"
    exit 1
fi

echo ""
echo "✅ Password confirmed. Setting up database..."

# 5. Run database initialization with the password
echo "🚀 Initializing database with admin user..."
cd server

# Run the database initialization command
echo "Running: poetry run python main.py db init -p \"$admin_password\""
poetry run python main.py db init -p "<password>"

# Check if command was successful
if [ $? -eq 0 ]; then
    echo "✅ Database initialized successfully!"
    echo ""
    echo "🎉 Setup Complete!"
    echo ""
    echo "👤 Admin User Information:"
    echo "   Email: admin@admin.com"
    echo "   Password: [set during installation]"
    echo ""
    echo "🚀 Next steps:"
    echo "   - Run './install.sh' to install dependencies"
    echo "   - Run './dev.sh' to start development servers"
    echo "   - Visit http://localhost:3000 to access the application"
else
    echo "❌ Database initialization failed!"
    exit 1
fi

# Return to project root
cd ..

echo "✅ Installation completed successfully!"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "# Environment variables for the project" > .env
    echo "NODE_ENV=development" >> .env
    echo "PORT=3000" >> .env
    echo "# Add your environment variables here" >> .env
fi

echo "✅ Setup complete!"
echo ""
echo "💡 Next steps:"
echo "  - Run 'sh run.sh' to start development servers"
echo "  - Make sure your Python environment is properly configured"

# Create a simple run script
cat > run.sh << 'EOF'
#!/bin/bash
# Run script to start both frontend and backend

echo "🚀 Starting development environment..."

# Start frontend
echo "Starting Nuxt.js frontend..."
cd client/app
npm run dev &
FRONTEND_PID=$!

# Start backend (adjust as needed)
echo "Starting Python backend..."
cd ../..
cd server
# Add your actual backend start command here:
# python3 app/main.py &
# BACKEND_PID=$!

echo "✅ Development environment started!"
echo "Frontend: http://localhost:3000"
echo "Backend: Adjust as needed"

# Wait for processes (optional)
# wait $FRONTEND_PID $BACKEND_PID
EOF

chmod +x run.sh

echo ""
echo "🎉 Installation and database setup completed successfully!"
echo ""
echo "📝 Admin User Credentials:"
echo "   Email: admin@admin.com"
echo "   Password: [set during installation]"
