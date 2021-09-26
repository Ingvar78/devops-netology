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
