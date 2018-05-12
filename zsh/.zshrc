#------------------------------
# Prompt
#------------------------------
autoload -U colors zsh/terminfo
colors

setopt prompt_subst
autoload -Uz vcs_info
zstyle ':vcs_info:*' actionformats \
    '%F{5}(%f%s%F{5})%F{3}-%F{5}[%F{2}%b%F{3}|%F{1}%a%F{5}]%f '
zstyle ':vcs_info:*' formats       \
    '%F{5}(%f%s%F{5})%F{3}-%F{5}[%F{2}%b%F{5}]%f '
zstyle ':vcs_info:(sv[nk]|bzr):*' branchformat '%b%F{1}:%F{3}%r'

zstyle ':vcs_info:*' enable git cvs svn

setprompt() {
  setopt prompt_subst

  if [[ -n "$SSH_CLIENT"  ||  -n "$SSH2_CLIENT" ]]; then
    p_host='
    %F{cyan}[%f
    %(!.%F{red}%n%f.%F{green}%n%f)
    %F{cyan}@%f
    %F{yellow}%M%f
    %F{cyan}]
    '
  else
    p_host=''
  fi

  if [ -n "$VIRTUAL_ENV" ]; then
    if [ -f "$VIRTUAL_ENV/name" ]; then
      v_name=cat $VIRTUAL_ENV/__name__
    elif [ basename $VIRTUAL_ENV = "__" ]; then
      v_name=$(basename $(dirname $VIRTUAL_ENV))
    else
      v_name=$(basename $VIRTUAL_ENV)
    fi
  fi

  vcs_info_wrapper() {
    vcs_info
    if [ -n "$vcs_info_msg_0_" ]; then
      echo "%{$fg[grey]%}${vcs_info_msg_0_}%{$reset_color%}$del"
    fi
  }

PS1=${(j::Q)${(Z:Cn:):-$'
    (${v_name})
    ${p_host}
    [%f
    %F{blue}%~%f
    %F{cyan}]%f
    %(!.%F{red}%#%f.%F{green}%f)
    " "
  '}}

  PS2=$'%_>'
  RPROMPT=$'$(vcs_info_wrapper)'
}
setprompt


[[ -n "${key[PageUp]}"   ]]  && bindkey  "${key[PageUp]}"    history-beginning-search-backward
[[ -n "${key[PageDown]}" ]]  && bindkey  "${key[PageDown]}"  history-beginning-search-forward


# virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/vwrapperhome
source /usr/local/bin/virtualenvwrapper.sh


# pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
