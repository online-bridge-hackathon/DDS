
# Change the build configuring of the C++ library

You can modify the build configuration after building the library. There is
cmake GUI tools which can help modify configuration variables. Example uses
curses GUI.

```
ccmake -S libdds -B libdds/.build
```

# Run the test of the C++ library

You can verify the C++ library works by running the test of the C++ library.

```
make libdds-build
make -C libdds/.build check
```
