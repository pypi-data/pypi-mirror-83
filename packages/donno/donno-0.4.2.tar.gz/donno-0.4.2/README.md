# Donno

A simple note-take CLI application.

## Install

`pip install donno`

## Usage

```
don add        # create a new note
don list       # list existing notes
don search nim thunder    # search notes contains "nim" and "thunder"
don edit 3     # edit note #3 in note list or searching results
don delete 3   # delete note #3 in note list or searching results
don backup     # backup notes to remote repository
don restore    # restore notes from remote repository
don preview 3  # preview note #3 in console editor
don phtml 3    # preview note #3 in browser
don ads -n nim -t config -c compile  # search notes which "nim" in its title, "config" in tags and "compile" in contents
don ads -r "[nim|thunder]"  # search notes contains "nim" or "thunder"
don publish    # publish notes to blog
```

Note: `phtml` command depends on pandoc and a browser.

## Configuration

File path: ~/.config/donno/config.json

### Configuration Items

#### General

* app_home: root folder of donno data files. Default: ~/.donno
* repo: folder to save all note files and resource files. Default: $app_home/repo
* editor: which application to use to create/update note. Default: `nvim`
* viewer: which application to use to view notes in console. Default: `nvim -R`
* default_notebook: default notebook name for a new note. Default: `/Diary`
* editor_envs: environment variables of the editor. For example,
  env `XDG_CONFIG_HOME` is used by neovim to load config/plugins to parse markdown files.
  Default: `~/.config`

#### Blog

* url: blog url
* publish_cmd: command to publish notes to blog

### Manage Configurations

```
don conf get                # list all current configurations
don conf get edtior         # get which editor to use
don conf set editor nvim    # set the editor, make sure you've installed it
don conf set default_notebook /Diary/2020

# set nested attribute:
don conf set editor_envs.XDG_CONFIG_HOME $HOME/Documents/sources/vimrcs/text

# restore default values of configurations:
don conf restore
```

## Update and uninstall

```
pip install --upgrade donno
pip uninstall donno
```

## Some notes

### Install in virtual environment

For those who don't want install apps in global environment,
install it in a virtual environment:
```
mkdir ~/apps/donno
cd ~/apps/donno
python -m venv env
. env/bin/activate
pip install donno

cat << EOF >> ~/.zshrc
function dn() {
  source $HOME/apps/donno/env/bin/activate
  don $@
  deactivate
}
EOF
```

Now the command is `dn` instead of `don`.

## Roadmap

1. Basic note-taking functions: add, delete, list, search, view, update notes

1. Configuration module: see [Configuration](#configuration);

1. Support adding attachments into notes, espeicially images

1. Preview: render markdown notes to HTML and previewed in browser

1. Synchronize notes between hosts (based on VCS, such as git)

1. Import/Export from/to other open source note-taking apps, such as [Joplin]()

1. Advanced search function: search by title, tag, notebook and content

1. Search with regular expression;

1. Basic publishing module: publish to blog, such as github.io

1. Advanced publishing function: publish specific note, or notes in specific notebook

