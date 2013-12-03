function _opengit_open()
{
  local open_cmd='huh?'
  if [ -n `echo $MACHTYPE | grep darwin` ]; then
    open_cmd='open'
  else
    open_cmd='xdg-open'
  fi
  $open_cmd $1
}

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
    _opengit_open $url
  fi
else
  echo "Crap, ain't no git repo"
fi;