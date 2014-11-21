# git-open, saving you a few seconds


It will open your github/bitbucket project page from your terminal

## Install

Instructions for Linux, OS X users should make the necessary substitutions, if any, I know nothing about OS X.

Create `~/bin`

```shell
mkdir -p "$HOME/bin"
```

Add the directory to the beginning of the `PATH` variable inside `.bashrc`

```shell
echo 'PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
```

This way, every new instance of Bash will now check for executable scripts in your bin directory.

Now you save the file `git-open` inside the `~/bin` directory and make the file executable with:

```shell
chmod +x git-open
```

## Usage

You can do this to open Github/Bitbucket on the current branch

    $ git open

or specify the branch

    $ git open remote_branch

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-awesome-feature`)
3. Commit your changes (`git commit -am 'Making it better'`)
4. Push to the branch (`git push origin my-awesome-feature`)
5. Create new Pull Request
6. Wait for me :smile:

## Power to you my friend!
