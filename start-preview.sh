#!/bin/bash
# Math Blast Preview Server
# Starts local HTTP server + Cloudflare tunnel for review
# Usage: ./start-preview.sh

PROJECTS_DIR="/Users/leohiem/.openclaw/workspace/projects/math-blast"
PORT=3000

echo "🚀 Starting Math Blast preview server..."

# Kill any existing instances
pkill -f "http.server $PORT" 2>/dev/null
pkill -f "cloudflared tunnel" 2>/dev/null
sleep 1

# Start local server
cd "$PROJECTS_DIR"
python3 -m http.server $PORT &
SERVER_PID=$!
echo "✅ Local server running on http://localhost:$PORT (PID: $SERVER_PID)"

# Start cloudflare tunnel and capture URL
cloudflared tunnel --url http://localhost:$PORT 2>&1 | grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' | head -1 &
TUNNEL_PID=$!

echo "⏳ Tunnel starting... (takes ~5 seconds)"
sleep 6

# Extract tunnel URL from cloudflared logs
TUNNEL_URL=$(cloudflared tunnel --url http://localhost:$PORT 2>&1 | grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' | head -1)

echo ""
echo "======================================"
echo "🌐 Preview URLs:"
echo "   Local:  http://localhost:$PORT"
echo "   Public: check cloudflared output above"
echo "======================================"
echo ""
echo "Press Ctrl+C to stop"
wait
