#!/bin/bash

# Configuration
HOST="192.168.30.79"
PORT=4004
PID_FILE="server.pid"
LOG_FILE="server.log"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "=== Kakuro Website Restart Script ==="

# 1. Stop existing process
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Stopping existing process (PID: $PID)..."
        kill "$PID"
        # Wait for it to die
        sleep 1
        # Force kill if still running
        if ps -p "$PID" > /dev/null 2>&1; then
             kill -9 "$PID"
        fi
        echo "Process stopped."
    else
        echo "Found PID file but process $PID is not running."
    fi
    rm "$PID_FILE"
else
    # Fallback: Check for any process using the port
    echo "No PID file found. Checking port $PORT..."
    if command_exists fuser; then
        fuser -k -n tcp $PORT > /dev/null 2>&1
    elif command_exists lsof; then
        PIDS=$(lsof -t -i:$PORT)
        if [ -n "$PIDS" ]; then
            kill $PIDS
        fi
    fi
fi

# 2. Rebuild the application
echo "Building the application..."
if npm run build; then
    echo "Build successful."
else
    echo "Build failed! Aborting restart."
    exit 1
fi

# 3. Start the server
echo "Starting server on $HOST:$PORT..."
nohup npx serve -s dist --listen tcp://$HOST:$PORT > "$LOG_FILE" 2>&1 &
NEW_PID=$!

# 4. Save PID and verify
echo $NEW_PID > "$PID_FILE"
sleep 2

if ps -p "$NEW_PID" > /dev/null 2>&1; then
    echo "✅ Server started successfully!"
    echo "   PID: $NEW_PID"
    echo "   Address: http://$HOST:$PORT"
    echo "   Logs: $LOG_FILE"
else
    echo "❌ Server failed to start. Check $LOG_FILE for details."
    exit 1
fi
