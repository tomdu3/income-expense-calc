#!/usr/bin/env python
import sys

print(sys.executable)

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
