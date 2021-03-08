import os
import sys

import git


class GitHandler:
    def __init__(self):
        self.print_statements = []
        self.config_dict = {
            'auto_commit': False,
            'commit_message': "..."
        }
        self._git_repo = None
        self._git_commit = None
        self._git_changed_files = None
        self._git_untracked_files = None

    def update_config(self, config):
        self.config_dict = config

    def get_project_information(self):
        self.print_statements = []  # reset
        ''' Check Git '''
        self._get_git_repo()
        self._commit_working_directory_to_git()

        ''' Log first information '''
        self._get_executed_file_info()
        self._get_git_infos()
        self._log_global_switches()

        return self.print_statements

    def _get_executed_file_info(self):
        if hasattr(sys.modules['__main__'], '__file__'):
            main_file_name = os.path.basename(sys.modules['__main__'].__file__)
            main_file_path = os.path.abspath(sys.modules['__main__'].__file__)
            self.print_statements.append('Started running: %s (%s)' % (main_file_name, main_file_path))
        else:
            self.print_statements.append('Started running unknown file')

    def _get_git_repo(self):
        try:
            self._git_repo = git.Repo(search_parent_directories=True)
        except:
            self.print_statements.append('No git repository found!')
            self._git_repo = None
            pass

    def _commit_working_directory_to_git(self):
        if self.config_dict['auto_commit']:
            if self._git_repo is not None:
                self._git_repo.git.add(update=True)
                self._git_repo.git.commit(m='______Automatic Commit: %s' % self.config_dict['commit_message'])

    def _get_git_infos(self):
        if self._git_repo is not None:
            try:
                self._git_commit = self._git_repo.head.object.hexsha
                self._git_untracked_files = self._git_repo.untracked_files
                self._git_changed_files = [item.a_path for item in self._git_repo.index.diff(None)]
            except:
                self.print_statements.append('Failed retrieving Git repo information.')
            self._log_git_infos()

    def _log_git_infos(self):
        self.print_statements.append('Current Git Commit: %s' % self._git_commit)
        self.print_statements.append('Current Changed Files: %s' % self._git_changed_files)
        self.print_statements.append('Current Untracked Files: %s' % self._git_untracked_files)

    def _log_global_switches(self):
        """
        Print global switches
        """
        self.print_statements.append('Git Config: ' + str(self.config_dict))
