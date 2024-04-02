#!/bin/bash
git add .
commitMessage=${1-:"Automated commit"}
git commit -m "$commitMessage"
git push

