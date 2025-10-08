"""
Tool execution for agentic workflow

This module executes tools requested by Claude agents via the API.
"""

import subprocess
from pathlib import Path


def execute_bash(command: str, description: str = None) -> dict:
    """Execute a bash command and return result

    Args:
        command: Bash command to execute
        description: Optional description of what command does

    Returns:
        dict with stdout, stderr, return_code
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120,
            cwd="."
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "success": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Command timed out after 120 seconds",
            "return_code": -1,
            "success": False
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "return_code": -1,
            "success": False
        }


def execute_read(file_path: str) -> dict:
    """Read a file and return contents

    Args:
        file_path: Path to file to read

    Returns:
        dict with content or error
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return {
                "content": None,
                "error": f"File not found: {file_path}",
                "success": False
            }

        content = path.read_text()
        return {
            "content": content,
            "error": None,
            "success": True
        }
    except Exception as e:
        return {
            "content": None,
            "error": str(e),
            "success": False
        }


def execute_write(file_path: str, content: str) -> dict:
    """Write content to a file

    Args:
        file_path: Path to file to write
        content: Content to write

    Returns:
        dict with success status
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return {
            "success": True,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def execute_edit(file_path: str, old_string: str, new_string: str) -> dict:
    """Edit a file by replacing old_string with new_string

    Args:
        file_path: Path to file to edit
        old_string: String to find and replace
        new_string: Replacement string

    Returns:
        dict with success status
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }

        content = path.read_text()

        if old_string not in content:
            return {
                "success": False,
                "error": f"String not found in file: {old_string[:100]}..."
            }

        new_content = content.replace(old_string, new_string, 1)
        path.write_text(new_content)

        return {
            "success": True,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Tool definitions for Anthropic API
TOOL_DEFINITIONS = [
    {
        "name": "bash",
        "description": "Execute a bash command and return the output. Use this for running shell commands, file operations, git commands, etc.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute"
                },
                "description": {
                    "type": "string",
                    "description": "A short description of what this command does"
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "read_file",
        "description": "Read the contents of a file. Returns the full file content.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file. Creates the file if it doesn't exist, overwrites if it does.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file"
                }
            },
            "required": ["file_path", "content"]
        }
    },
    {
        "name": "edit_file",
        "description": "Edit a file by replacing a specific string with a new string. Only replaces the first occurrence.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to edit"
                },
                "old_string": {
                    "type": "string",
                    "description": "The exact string to find and replace"
                },
                "new_string": {
                    "type": "string",
                    "description": "The replacement string"
                }
            },
            "required": ["file_path", "old_string", "new_string"]
        }
    }
]


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Execute a tool and return result as string

    Args:
        tool_name: Name of tool to execute
        tool_input: Tool input parameters

    Returns:
        Result as formatted string
    """
    if tool_name == "bash":
        result = execute_bash(
            tool_input["command"],
            tool_input.get("description")
        )
        if result["success"]:
            output = result["stdout"] if result["stdout"] else "(no output)"
            return f"Command executed successfully:\n{output}"
        else:
            return f"Command failed (code {result['return_code']}):\n{result['stderr']}"

    elif tool_name == "read_file":
        result = execute_read(tool_input["file_path"])
        if result["success"]:
            return f"File contents:\n{result['content']}"
        else:
            return f"Error: {result['error']}"

    elif tool_name == "write_file":
        result = execute_write(tool_input["file_path"], tool_input["content"])
        if result["success"]:
            return f"File written successfully: {tool_input['file_path']}"
        else:
            return f"Error: {result['error']}"

    elif tool_name == "edit_file":
        result = execute_edit(
            tool_input["file_path"],
            tool_input["old_string"],
            tool_input["new_string"]
        )
        if result["success"]:
            return f"File edited successfully: {tool_input['file_path']}"
        else:
            return f"Error: {result['error']}"

    else:
        return f"Error: Unknown tool '{tool_name}'"
