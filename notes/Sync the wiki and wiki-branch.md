## Sync the wiki and wiki-branch

### wiki branch allows for reviewing
The github-wiki doesn't allow PRs, which means changes can't be reviewed.
To work around this, we duplicate the [github-wiki](https://github.com/techartorg/bqt/wiki) in the [wiki branch](https://github.com/techartorg/bqt/tree/wiki) 
Now anyone can submit a [PR](https://github.com/techartorg/bqt/pulls) to the wiki branch, which can be reviewed.

When a change is merged in the wiki branch, it needs to be merged back to the github-wiki. 

### sync branch and wiki
To do so, you can add a new remote to your bqt repo.
```bash
git remote add githubwiki https://github.com/techartorg/bqt.wiki.git
```

And push the wiki branch to the github-wiki repo. (Wiki editors or admins only)