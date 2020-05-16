# qtile-config

## Description

A place to separate my qtile config from my [dotfiles](https://github.com/CyberGsus/dotfiles), 
in a way such that it is completely independent from all of the other config
files and gives the option to choose what you need without bloating the system.

## Installation

To get this configuration up and running, make sure you have the following packages:

- `alacritty` (terminal)
- `dmenu` (run system)

Now just clone the repository into your `~/.config`:
```
git clone https://github.com/CyberGsus/qtile-config ~/.config/qtile
```
or, if you are doing your own dotfiles repository I recommend using `submodule`
so you have the same independency from the rest of your repo:

```
git submodule add https://github.com/CyberGsus/qtile-config ~/.config/qtile
```
## More stuff

On my [TODO](./TODO.md) list I have put everything I have to do in order
to get this repository even more independent.
