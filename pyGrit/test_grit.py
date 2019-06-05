import unittest
import os
from workspace import Workspace
import pytest
import tempfile
import mock
	
# This is not testing any functionality.
def test_root_path_implementation_ok():
	root_path = os.path.abspath('.') # absolute path to current directory
	assert '/Users/andreaguiar/Desktop/usr/dev/git-building/pyGrit' == root_path

def test_workspace_list_files():
    with tempfile.TemporaryDirectory(dir='.') as tmp_dir:
        dir_list = []
        file = tempfile.mkstemp(prefix='___test_file_', dir=tmp_dir)[1]
        workspace = Workspace(tmp_dir)
        tmp_filename = workspace.list_files()[0]
        

    assert tmp_filename.startswith('___test_file_')

@mock.patch("os.listdir")
def test_workspace_ignored_files(mock_listdir):
    """ 
    Asserts list_files method ignores folders: '.', '..' and '.git' 
    """
    with tempfile.TemporaryDirectory(dir='.') as tmp_dir:
        
        mock_listdir.return_value = [".", "There", "..", "should", "__pycache__", "only", ".git", "have", "words", "here","not", "dots"]

        workspace = Workspace(tmp_dir)
        assert sorted(["There", "should", "only", "have", "words", "here","not", "dots"]) == sorted(workspace.list_files())

