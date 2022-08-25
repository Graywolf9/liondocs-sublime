import os, subprocess
import re
# from pathlib import Path

import sublime
import sublime_plugin

try:
    # I hate Python import system xd
    import sys
    sys.path.append(os.path.dirname(os.path.realpath(__file__)))
    from .api import Shaman
except Exception:
    from api import Shaman

CONTENT_PATH = None
TRANSLATED_CONTENT_PATH = None
LANG_CODE = None
ALERTS = None

# cpath = str(Path("\\content"))
# tcpath = str(Path("\\translated-content"))
# uspath = str(Path("\\en-us"))

valid_exts = ('.md', '.html')
exts_dict = {'.md': '.html', '.html': '.md'}


def plugin_loaded():
    global CONTENT_PATH
    global TRANSLATED_CONTENT_PATH
    global LANG_CODE
    global ALERTS

    settings = sublime.load_settings('LionDocs.sublime-settings')
    CONTENT_PATH = settings.get('paths').get('content')
    TRANSLATED_CONTENT_PATH = settings.get('paths').get('translated-content')
    LANG_CODE = settings.get('lang_code')
    ALERTS = settings.get('alerts')


def alert(message):
    if ALERTS:
        sublime.message_dialog(message)


class getshaCommand(sublime_plugin.TextCommand):
    def __insert_in_cursor(self, edit, string):
        """
        Insert given string in current cursor position
        """
        self.view.insert(edit, self.view.sel()[0].begin(), string)

    def run(self, edit, mode):
        cfile = self.view.window().active_view().file_name()
        slash = (('/','\\')[os.name == 'nt'])
        #ofile = cfile.replace('/translated-content/','/content/').replace('/es/','/en-us/')
        ofile = CONTENT_PATH + '/files/en-us/' + cfile.split(slash + LANG_CODE + slash)[1]
        if os.name == 'nt':
          ofile = ofile.replace('/','\\')
        os.chdir(CONTENT_PATH)
        print('Getting sha from: ' + ofile)
        command = "git log -1 --pretty=%H " + ofile
        last_commit = subprocess.check_output(command, shell=True)
        last_commit = last_commit.decode().strip()
        print('Sha: ' + last_commit)
        print('Sha copied to clipboard: ' + last_commit)
        sublime.set_clipboard(last_commit)
        print('Putting sha in cursor position...')
        print('File: ' + cfile)
        base = "l10n:\n  sourceCommit: {0}".format(last_commit)
        self.__insert_in_cursor(edit, base)


class transferCommand(sublime_plugin.TextCommand):
    def run(self, edit, mode):
        file_to_transfer = Path(self.view.file_name())  # file in content

        # replace content with translated-content
        temp = str(file_to_transfer).replace(cpath, tcpath)

        # replace en-us with target language
        lang = str(Path("\\" + LANG_CODE))
        final_file_path = temp.replace(uspath, lang)

        # get final file dir tree
        dir_tree = str(Path(final_file_path).parent)

        # create dir tree if not exist
        if not os.path.exists(dir_tree):
            os.mkdir(dir_tree)

        # open original and destiny file at same time
        with open(str(file_to_transfer), 'r') as original_file, open(final_file_path, 'w') as final_file:
            original_content = original_file.read()

            if mode == 'same_file':
                final_file.write(original_content)

                alert("File transfered successfully!")

            elif mode == 'with_sha':
                shaman = Shaman(file_to_transfer, CONTENT_PATH)
                meta = shaman.get_file_sha(returnas='meta')

                sep_index = [i.start() for i in re.finditer('---', original_content)][1]  # get separator index
                final_content = original_content[:sep_index] + meta + "\n" + original_content[sep_index:]
                final_file.write(final_content)

                alert("File with sourceCommit transfered successfully!")
