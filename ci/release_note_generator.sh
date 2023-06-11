#!/bin/bash

# Generate a release note for the current release
# Use git diff from previous tag to HEAD to generate the release note
# echo it all out to stdout

PREV_TAG=$(git describe --abbrev=0 --tags $(git rev-list --tags --skip=1 --max-count=1))
CURRENT_TAG=$(git describe --abbrev=0 --tags)

RELEASE_NOTE=$(git log --pretty=format:"%h - %s (%an)" $PREV_TAG..$CURRENT_TAG)
# Echo it out
echo $RELEASE_NOTE