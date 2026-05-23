#!/usr/bin/env python3
import http.server
import json
import os
import sys
import socketserver

# Add scripts directory to path so we can import them
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, "scripts"))

try:
    import fetch_all_tasks
    import build_tree
    import generate_html
except ImportError as e:
    print(f"Error importing automation scripts: {e}")
    sys.exit(1)

PORT = 5001

class DashboardRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers so we can access from file:// or other origins
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/refresh' or self.path.startswith('/api/refresh?'):
            self.handle_refresh()
        else:
            # Map default root paths to the generated HTML file
            if self.path == '/' or self.path == '/index.html':
                self.path = '/ux_redesign_tasks.html'
            
            # Custom file serving logic to serve from dashboard folder
            target_path = self.path.lstrip('/')
            # Sanitize path to prevent directory traversal
            clean_name = os.path.basename(target_path)
            full_path = os.path.join(script_dir, clean_name)
            
            if clean_name == "ux_redesign_tasks.html" and os.path.exists(full_path):
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(full_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, f"File {clean_name} not found")

    def do_POST(self):
        if self.path == '/api/refresh':
            self.handle_refresh()
        else:
            self.send_error(404, "Not Found")

    def handle_refresh(self):
        try:
            print("\n==============================================")
            print("🔄 LIVE UPDATE REQUEST RECEIVED FROM DASHBOARD")
            print("==============================================")
            
            # Dynamically reload modules on every request to bypass python import cache
            import importlib
            importlib.reload(fetch_all_tasks)
            importlib.reload(build_tree)
            importlib.reload(generate_html)
            
            # Step 1: Fetch all tasks from ClickUp
            print("📥 Step 1/3: Fetching all latest tasks from ClickUp...")
            fetch_all_tasks.main()
            
            # Step 2: Compile fresh tasks tree hierarchy
            print("🌲 Step 2/3: Rebuilding relational tasks tree...")
            build_tree.main()
            
            # Step 3: Generate the static dashboard page
            print("🎨 Step 3/3: Regenerating premium HTML dashboard...")
            generate_html.main()
            
            print("✅ SUCCESS: Workspace synchronization complete!")
            print("==============================================\n")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "success", 
                "message": "ClickUp workspace data has been synchronized and refreshed successfully!"
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print("\n❌ ERROR during synchronization:")
            print(tb)
            print("==============================================\n")
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "error", 
                "message": f"Synchronization failed: {str(e)}"
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))

def main():
    # Make sure we run in the server directory
    os.chdir(script_dir)
    
    # Enable address reuse so restarting doesn't block the port
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), DashboardRequestHandler) as httpd:
        print("\n" + "="*60)
        print(f"🚀 FPV ClickUp Sync Server is active at: http://localhost:{PORT}")
        print("  - To view the dashboard, visit: http://localhost:5000")
        print("  - Supports live synchronization with ClickUp workspace.")
        print("  - Press Ctrl+C to terminate the server.")
        print("="*60 + "\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server shut down gracefully.")
            sys.exit(0)

if __name__ == "__main__":
    main()
