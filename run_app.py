"""
Annadata Saathi - AI Agricultural Assistant
State-Level Buildathon MVP

This script initializes and starts the Flask application.
"""

import os
import sys
from pathlib import Path

def main():
    print("\n" + "="*50)
    print("  🌾 Annadata Saathi")
    print("  AI Agricultural Assistant for Indian Farmers")
    print("="*50 + "\n")
    
    
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    print("✅ Initializing application...")
    print(f"📁 Working directory: {Path.cwd()}")
    
    
    db_path = Path('annadata_saathi.db')
    if not db_path.exists():
        print("🔄 Database not found. Initializing...")
        import subprocess
        subprocess.run([sys.executable, 'database/init_db.py'])
    else:
        print("✅ Database found")
    
    print("\n🚀 Starting Flask Application...")
    print("=" * 50)
    print("📍 Server: http://localhost:5000")
    print("🔐 Debug: Enabled")
    print("=" * 50)
    print("\n💡 Tips:")
    print("  - Open http://localhost:5000 in your browser")
    print("  - Press Ctrl+C to stop the server")
    print("  - Check console for debug messages")
    print("\n")
    
    from app import app, init_db
    
    
    if not db_path.exists():
        init_db()
    
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True,
        use_debugger=True
    )

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n Error: {e}")
        sys.exit(1)
