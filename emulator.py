import os
import tarfile
import csv
import xml.etree.ElementTree as ET

class ShellEmulator:
    def __init__(self, config_file):
        self.load_config(config_file)
        self.current_dir = "/"
        self.extract_virtual_fs()
        self.setup_log_file()

    def load_config(self, config_file):
        try:
            with open(config_file, 'r') as file:
                reader = csv.DictReader(file)
                config = next(reader)
                self.username = config.get('username', 'unknown_user')
                self.fs_path = config.get('fs_path')
                self.log_path = config.get('log_path')
                if not self.fs_path or not self.log_path:
                    raise KeyError("Missing required fields in config file.")
        except FileNotFoundError:
            print(f"Error: Config file '{config_file}' not found.")
            exit(1)
        except KeyError as e:
            print(f"Error: {e}")
            exit(1)
        except StopIteration:
            print("Error: Config file is empty or invalid.")
            exit(1)

    def extract_virtual_fs(self):
        if os.path.exists('virtual_fs'):
            os.system('rm -rf virtual_fs')
        os.makedirs('virtual_fs', exist_ok=True)
        with tarfile.open(self.fs_path, 'r:gz') as tar:
            tar.extractall('virtual_fs')

    def create_virtual_fs_archive(self):
        with tarfile.open(self.fs_path, 'w:gz') as tar:
            tar.add('virtual_fs', arcname='')

    def setup_log_file(self):
        root = ET.Element("log")
        tree = ET.ElementTree(root)
        tree.write(self.log_path)

    def log_action(self, action):
        tree = ET.parse(self.log_path)
        root = tree.getroot()
        entry = ET.SubElement(root, "entry")
        ET.SubElement(entry, "user").text = self.username
        ET.SubElement(entry, "action").text = action
        tree.write(self.log_path)

    def run(self):
        print(f"Welcome, {self.username}! Type 'exit' to quit.")
        while True:
            try:
                command = input(f"{self.username}:{self.current_dir}$ ").strip()
                if command.lower() == "exit":
                    self.log_action("exit")
                    break
                elif command.startswith("ls"):
                    self.ls()
                elif command.startswith("cd"):
                    self.cd(command)
                elif command.startswith("touch"):
                    self.touch(command)
                elif command.startswith("rmdir"):
                    self.rmdir(command)
                elif command.startswith("rev"):
                    self.rev(command)
                else:
                    print("Command not found.")
            except KeyboardInterrupt:
                print("\nExiting...")
                self.log_action("exit")
                break

    def ls(self):
        path = os.path.join('virtual_fs', self.current_dir.strip('/'))
        try:
            entries = os.listdir(path)
            if entries:
                print("\n".join(entries))
            else:
                print("No files or directories found.")
        except FileNotFoundError:
            print("Directory not found.")
        self.log_action("ls")

    def cd(self, command):
        args = command.split()
        if len(args) < 2:
            print("Usage: cd <directory>")
            return

        new_dir = args[1]
        if new_dir == "..":
            self.current_dir = "/".join(self.current_dir.rstrip("/").split("/")[:-1]) or "/"
        else:
            potential_dir = os.path.join(self.current_dir, new_dir).strip('/')
            if os.path.isdir(os.path.join('virtual_fs', potential_dir)):
                self.current_dir = f"/{potential_dir}".strip("/")
            else:
                print("Directory not found.")
                return

        self.log_action(f"cd {new_dir}")

    def touch(self, command):
        args = command.split()
        if len(args) < 2:
            print("Usage: touch <file_name>")
            return

        file_name = args[1]
        file_path = os.path.join('virtual_fs', self.current_dir.strip('/'), file_name)
        try:
            with open(file_path, 'w') as file:
                pass
            print(f"File '{file_name}' created.")
            self.log_action(f"touch {file_name}")
        except Exception as e:
            print(f"Error creating file: {e}")

    def rmdir(self, command):
        args = command.split()
        if len(args) < 2:
            print("Usage: rmdir <directory>")
            return

        dir_name = args[1]
        dir_path = os.path.join('virtual_fs', self.current_dir.strip('/'), dir_name)
        if os.path.isdir(dir_path):
            if not os.listdir(dir_path):  # Check if directory is empty
                os.rmdir(dir_path)
                print(f"Directory '{dir_name}' removed.")
                self.log_action(f"rmdir {dir_name}")
            else:
                print("Error: Directory is not empty.")
        else:
            print("Error: Directory not found.")

    def rev(self, command):
        args = command.split()
        if len(args) < 2:
            print("Usage: rev <file_path>")
            return

        file_name = args[1]
        file_path = os.path.join('virtual_fs', self.current_dir.strip('/'), file_name)
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                print("\nReversed content:\n")
                print(content[::-1])
                self.log_action(f"rev {file_name}")
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")

if __name__ == "__main__":
    emulator = ShellEmulator("config.csv")
    emulator.run()
    emulator.create_virtual_fs_archive()