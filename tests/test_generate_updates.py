import csv
import json
import tempfile
import unittest
from pathlib import Path

from generate_updates import commands_from_inventory, generate_script, parse_ssh_command


class GenerateUpdatesTests(unittest.TestCase):
    def test_preserves_complete_ssh_command_and_options(self):
        value = "sshg -oHostKeyAlgorithms=+ssh-rsa ubuntu@192.0.2.10"
        self.assertEqual(parse_ssh_command(value), "sshg -t -oHostKeyAlgorithms=+ssh-rsa ubuntu@192.0.2.10")

    def test_tag_filter_and_payload_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "inventory.csv"
            with path.open("w", encoding="utf-8", newline="") as output:
                writer = csv.DictWriter(output, fieldnames=["table", "id", "payload"])
                writer.writeheader()
                writer.writerow({"table": "record", "id": "1", "payload": json.dumps({"tagIds": [6], "ssh1String": "sshg user@host1"})})
                writer.writerow({"table": "record", "id": "2", "payload": json.dumps({"tagIds": [5], "ssh1String": "sshg user@host2"})})
                writer.writerow({"table": "record", "id": "3", "payload": json.dumps({"tagIds": [6], "ssh1String": "sshg user@host1"})})
            self.assertEqual(commands_from_inventory(path), (["sshg -t user@host1"], 0))

    def test_missing_destination_is_counted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "inventory.csv"
            path.write_text('tagIds,ssh1String\n"[6]",\n', encoding="utf-8")
            self.assertEqual(commands_from_inventory(path), ([], 1))

    def test_generated_script_quotes_remote_path_and_is_not_run(self):
        command = "sudo apt update ; sudo apt install -y nano"
        script = generate_script(["sshg -t -oOption=value user@example.org"], command)
        self.assertIn("sshg -t -oOption=value user@example.org 'sudo apt update ; sudo apt install -y nano'", script)
        self.assertTrue(script.startswith("#!/usr/bin/env bash\n"))
        self.assertIn("set -Eeuo pipefail", script)
        self.assertIn("set -x", script)
        self.assertIn("trap 'status=$?;", script)
        self.assertIn("shopt -s expand_aliases", script)
        self.assertIn('alias sshg=\'ssh -A -o SendEnv="GIT*"\'', script)
        self.assertNotIn("password", script.lower())


if __name__ == "__main__":
    unittest.main()
