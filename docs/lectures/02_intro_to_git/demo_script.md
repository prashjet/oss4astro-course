# Demo: Git & GitHub

- create a repo `sequence` (not to clash with the real `sequences` example that will be used for the rest of the lecture)
- all file changes referenced below should just be README edits.

## Basics (via command line)

- sign in to GitHub
- create a new repository:
    - visibility: public
    - no template
    - add a README - explain
    - default `.gitignore` - e
- clone the repository
- make a change
- git add 
- git commit -m 'commit message' (note: here we are merging to main, as it's the only branch)
- git push

Now with branches:

- git branch new_feature
- git checkout new_feature
- make a change, add, commit and push (explain photo book analogy: add = arranging photos, commit = gluing them down)
- raise and merge the PR in GitHub

## Using VSCode Git integration

Repeat the branch, change, commit, PR, merge example via VSCode Git integration.

## Provoke a merge conflict

- create two new branches off of main:
    - branch 1: change, commit, PR, merge
    - branch 2: change to provoke a conflict, resolve in browser via GitHub


