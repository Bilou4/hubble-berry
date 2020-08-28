# Contributing


## Where do I go from here?

If you've noticed a bug or have a feature request, [make one][new issue]! It's
generally best if you get confirmation of your bug or approval for your feature
request this way before starting to code.


## Fork & create a branch

If this is something you think you can fix, then [fork Hubble-Berry] and create
a branch with a descriptive name.

A good branch name would be:

```sh
git checkout -b add-japanese-translations
```

## Implement your fix or feature

You can make all the changes you want, as long as it improves the project or user experience! 
Feel free to ask for help; everyone is a beginner at first.

## View your changes

Hubble-Berry is meant to be used by humans. So make sure to take
a look at your changes in a browser.


## Get the style right

<!-- TODO -->

## Make a Pull Request

At this point, you should switch back to your master branch and make sure it's
up to date with Hubble-Berry's master branch:

```sh
git remote add upstream git@github.com:Bilou4/hubble-berry.git
git checkout master
git pull upstream master
```

Then update your feature branch from your local copy of master, and push it!

```sh
git checkout add-japanese-translations
git rebase master
git push --set-upstream origin add-japanese-translations
```

Finally, go to GitHub and [make a Pull Request][]



## Keeping your Pull Request updated

If a maintainer asks you to "rebase" your PR, they're saying that a lot of code
has changed, and that you need to update your branch so it's easier to merge.

To learn more about rebasing in Git, there are a lot of [good][git rebasing]
[resources][interactive rebase] but here's the suggested workflow:

```sh
git checkout add-japanese-translations
git pull --rebase upstream master
git push --force-with-lease add-japanese-translations
```

## Merging a PR (maintainers only)

A PR can only be merged into master by a maintainer if:

* It is passing CI (none at this time).
* It has been approved by <!-- at least two --> maintainers. If it was a maintainer who
  opened the PR, only one extra approval is needed.
* It has no requested changes.
* It is up to date with current master.

Any maintainer is allowed to merge a PR if all of these conditions are
met.

## Attribution

This CONTRIBUTING is adapted from [Active Admin].


[new issue]:https://github.com/Bilou4/hubble-berry/issues/new
[fork Hubble-Berry]: https://help.github.com/articles/fork-a-repo
[make a pull request]: https://help.github.com/articles/creating-a-pull-request
[git rebasing]: http://git-scm.com/book/en/Git-Branching-Rebasing
[interactive rebase]: https://help.github.com/en/github/using-git/about-git-rebase
[Active Admin]: https://github.com/activeadmin/activeadmin