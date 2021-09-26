# devops-netologyOn branch main
$ git status
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean

$ git diff
diff --git a/README.md b/README.md
index 647b370..e57076a 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,4 @@
-# devops-netology
\ No newline at end of file
+# devops-netologyOn branch main
+Your branch is up to date with 'origin/main'.
+
+nothing to commit, working tree clean

$ git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean

git add .gitignore
git diff --staged

Newdiff --git a/.gitignore b/.gitignore
new file mode 100644
index 0000000..e69de29

/terraform/.gitignore
1. Будут проигнорированы локальные директории '.terraform'
2. файлы .tfstate содержащие в имени .tfstate либо в конце либо в середике названия.
3. фалы переменных содержащие вароли, закрытые ключи и т.п. - *.tfvars
4. файлы переопределения 
5. конфигурационные файлы CLI

Add fix

PyCharm

Fix two

'''
git cat README.md
git commit a -m "Добавление bb + gitlab"
git commit -a -m "Добавление bb + gitlab"
git tag v0.0
git push origin main 
git push -u bitbucket main
git push -u gitlab main
git tag 
git push origin main --tags 
git push -u bitbucket main --tags 
git push -u gitlab main --tags 
git tag -a v0.1 -m "annotation for tag"
git tag 
git show v0.1 
git status 
git push origin main --tags 
git push -u bitbucket main --tags 
git push -u gitlab main --tags 
git log  
git checkout 38e69dcc482d711fd3be3008edc32d81feaf3189
git log 
git switch -c fix
git push -u origin fix
git commit -a -m "Fix"
git push -u origin
git log 
'''

