import os
import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Использование: python check.py почта [d]")
        return

    email = sys.argv[1]
    mode = "d" if (len(sys.argv) > 2 and sys.argv[2] == "d") else ""

    base_dir = os.path.dirname(os.path.abspath(__file__))
    run_script = os.path.join(base_dir, "run.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = base_dir

    cmd = [sys.executable, run_script, email]
    if mode:
        cmd.append(mode)

    subprocess.run(cmd, env=env)

if __name__ == "__main__":
    main()