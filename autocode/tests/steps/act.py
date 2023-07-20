import os
import pytest

from autocode.steps.act import (
    create_handler,
    create_new_file_handler,
    insert_code_handler,
    remove_code_handler,
    replace_code_handler,
    write_complete_script_handler,
)


def setup_function():
    if not os.path.exists("test_dir"):
        os.makedirs("test_dir")


def teardown_function():
    if os.path.exists("test_dir"):
        for root, dirs, files in os.walk("test_dir", topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))


def test_create_handler():
    setup_function()
    context = {"project_dir": "test_dir"}
    arguments = {
        "reasoning": "Testing create handler",
        "code": "print('Hello, World!')",
        "packages": ["numpy", "pandas"],
        "test": "def test_main(): assert True",
    }
    create_handler(arguments, context)

    assert os.path.isfile("test_dir/main.py")
    assert os.path.isfile("test_dir/main_test.py")
    assert os.path.isfile("test_dir/requirements.txt")
    teardown_function()


def test_write_complete_script_handler():
    setup_function()
    context = {"project_dir": "test_dir"}
    arguments = {
        "reasoning": "Testing write complete script handler",
        "code": "print('Hello, World!')",
        "filepath": "main.py",
        "packages": ["numpy", "pandas"],
    }
    write_complete_script_handler(arguments, context)

    assert os.path.isfile("test_dir/main.py")
    teardown_function()


def test_insert_code_handler():
    setup_function()
    context = {"project_dir": "test_dir"}
    arguments = {
        "reasoning": "Testing insert code handler",
        "code": "\nprint('Inserted line')",
        "line_number": 0,
        "filepath": "main.py",
        "packages": ["numpy", "pandas"],
    }
    write_complete_script_handler(
        arguments, context
    )  # First, create a file to insert into
    insert_code_handler(arguments, context)

    with open("test_dir/main.py", "r") as f:
        lines = f.readlines()
    assert "Inserted line" in lines[0]
    teardown_function()


def test_replace_code_handler():
    setup_function()
    context = {"project_dir": "test_dir"}
    arguments = {
        "reasoning": "Testing replace code handler",
        "code": "print('New line')",
        "start_line": 1,
        "end_line": 1,
        "filepath": "main.py",
        "packages": ["numpy", "pandas"],
    }
    write_complete_script_handler(arguments, context)  # First, create a file to replace
    replace_code_handler(arguments, context)

    with open("test_dir/main.py", "r") as f:
        lines = f.readlines()
    assert "New line" in lines[0]
    teardown_function()


def test_remove_code_handler():
    setup_function()
    context = {"project_dir": "test_dir"}
    arguments = {
        "reasoning": "Testing remove code handler",
        "start_line": 1,
        "end_line": 1,
        "filepath": "main.py",
    }
    write_complete_script_handler(
        arguments, context
    )  # First, create a file to remove from
    remove_code_handler(arguments, context)

    with open("test_dir/main.py", "r") as f:
        lines = f.readlines()
    assert "New line" not in lines
    teardown_function()


def test_create_new_file_handler():
    setup_function()
    context = {"project_dir": "test_dir"}
    arguments = {
        "reasoning": "Testing create new file handler",
        "filepath": "new_file.py",
        "code": "print('Hello, New File!')",
        "packages": ["numpy", "pandas"],
        "test": "def test_new_file(): assert True",
    }
    create_new_file_handler(arguments, context)

    assert os.path.isfile("test_dir/new_file.py")
    assert os.path.isfile("test_dir/new_file_test.py")
    teardown_function()
