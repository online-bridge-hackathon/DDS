# Coding Style

# Issues

# Pull Request

## Managing Submodule

If your changes require libdds changes to be include then there are a few
extra steps to follow. You have to make sure required libdds changes have been
merged to [http:://github.com/online-bridge-hackathon/libdds](http:://github.com/online-bridge-hackathon/libdds).

Merging commits to libdds doesn't automatically include merges to the library
used by service build process. The library version used by service is based on
the commit attached to the submodule. To update the commit you need to first
checkout the new commit into your submodule working tree. Then the change needs
to be staged and committed like source code changes. The following example shows
steps to update the submodule to the latest commit in the master branch.

```
cd libdds
git checkout origin/master
cd ..
git add libdds
git commit
```

Submodule update can be included in a commit with service code changes for an
atomic update.
