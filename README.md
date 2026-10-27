# git-open, saving you a few seconds

Open a GitHub, Bitbucket, GitLab, or Codeberg branch or file from your terminal.

## Install/Uninstall

```shell
sudo make install
# To remove it:
sudo make uninstall
```

## Usage

Open the current branch:

    $ git open

or specify the branch

    $ git open remote_branch

and also the file

    $ git open remote_branch file_path

File paths are relative to the repository root. Quote paths containing spaces.
The command uses `origin` and checks locally cached remote branches; run
`git fetch origin` if a branch is missing. In detached HEAD mode, specify a branch.

HTTPS, HTTP, scp-style SSH, and `ssh://` remotes are supported. Self-hosted
GitLab and GitHub hosts named `gitlab.*` and `github.*` retain their original host.

Use `git open --help` for usage.

## Dependency

Bash and Git are required. Linux also requires `xdg-utils`; macOS uses `open`.

## Tests

Run `make test` with Python 3 installed. Tests use temporary Git repositories and
a mocked browser opener.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-awesome-feature`)
3. Commit your changes (`git commit -m 'Making it better'`)
4. Push to the branch (`git push origin my-awesome-feature`)
5. Create new Pull Request
6. Wait for me :smile:

## Power to you my friend!
