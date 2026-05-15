const { spawn } = require('child_process');

const isWindows = process.platform === 'win32';
const pythonPath = isWindows ? 'venv\\Scripts\\python' : './venv/bin/python';
const command = `cd ../Winky_code && ${pythonPath} agent.py dev`;

const child = spawn(command, { stdio: 'inherit', shell: true });

child.on('exit', (code) => {
  process.exit(code);
});