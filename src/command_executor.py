import subprocess
import time

def run_command(command, timeout=60):
    try:
        start_time = time.time()
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while process.poll() is None:
            if time.time() - start_time > timeout:
                process.kill()
                return f"Error: Command timed out after {timeout} seconds"
            time.sleep(0.1)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            return f"Error: {stderr}"
        return stdout
    except Exception as e:
        return f"Error: {str(e)}"
