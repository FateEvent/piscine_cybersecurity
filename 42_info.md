To install homebrew in the goinfre folder:
`git clone https://github.com/Homebrew/brew $HOME/goinfre/.brew && echo 'export PATH=$HOME/goinfre/.brew/bin:$PATH' >> $HOME/.zshrc && source $HOME/.zshrc && brew update`

`brew install curl`

To configure curl:
* <https://stackoverflow.com/questions/58918128/compile-a-c-at-project-with-libcurl-library-on-macos>;
```
echo 'export PATH="/goinfre/faventur/.brew/opt/curl/bin:$PATH"' >> ~/.zshrc
export LDFLAGS="-L/Users/faventur/goinfre/.brew/opt/curl/lib"
export CPPFLAGS="-I/Users/faventur/goinfre/.brew/opt/curl/include"
export PKG_CONFIG_PATH="/Users/faventur/goinfre/.brew/opt/curl/lib/pkgconfig"
```

It may be used to configure the curl library for python or for c++.

To install python modules on Mac:
```
pip3 install MODULE --user
```