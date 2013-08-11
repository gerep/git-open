# opengit, saving you a few seconds


Open your github or bitbucket project page from your terminal

You have that `.sh` file but you can use it as a function on your, let's say, `.bash_profile`.

```bash
function opengit() {
  if [ -d .git ]; then
    if [ -z "$(git remote -v)" ]; then
      echo "Hum....there are no remotes here"
    else
      where="https://github.com/" # default location to github
      remotes=$(git remote -v | awk -F'git@github.com:' '{print $2}' | cut -d" " -f1)
      if [ -z "$remotes" ]; then
        remotes=$(git remote -v | awk -F'https://github.com/' '{print $2}' | cut -d" " -f1)
      fi

      if [ -z "$remotes" ]; then
        remotes=$(git remote -v | awk -F'git@bitbucket.org/' '{print $2}' | cut -d" " -f1)
        where="https://bitbucket.org/"
      fi

      if [ -z "$1" ];then
        url="$where$(echo $remotes | cut -d" " -f1 | cut -d"." -f1)"
      else
        url="$where$(echo $remotes | cut -d" " -f1 | cut -d"." -f1)/tree/${1}"
      fi
      xdg-open $url
    fi
  else
    echo "Crap, ain't no git repo"
  fi;
}
```

and `. ~/.bash_profile` to load the change. Now you can `opengit` on your terminal and your favorite browser will open your project page.

## Usage

You can

    $ opengit
    
or

    $ opengit remote_branch

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-awesome-feature`)
3. Commit your changes (`git commit -am 'Making it better'`)
4. Push to the branch (`git push origin my-awesome-feature`)
5. Create new Pull Request
6. Wait for me :smile:

## I love you

[I](http://gerep.blogspot.com.br/) made this. Ping me on Twitter —
[@danielgerep](http://twitter.com/danielgerep) — so we can be friends.

Power to you!
