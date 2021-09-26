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

git log 
commit b7d5074ceaa9992019e2c06c5f94a264beb377f7
Author: Igor Vishenkov <igor@********.ru>
Date:   Mon Sep 20 23:36:25 2021 +0300

    Moved and deleted

commit 38e69dcc482d711fd3be3008edc32d81feaf3189
Author: Igor Vishenkov <igor@********.ru>
Date:   Mon Sep 20 23:33:19 2021 +0300

    Prepare to delete and move

commit 5d148920d8c809b89c184d47615c2e0e7ad20166
Author: Igor Vishenkov <igor@********.ru>
Date:   Mon Sep 20 23:31:14 2021 +0300

    Added gitignore

commit af020a031807466c4f88232ec1ab7b5167bc8efd
Author: Igor Vishenkov <igor@********.ru>
Date:   Mon Sep 20 23:15:29 2021 +0300

    Second commit

commit 95777d49679b31524cd5a60f344e6606ec8debf4
Author: Igor Vishenkov <igor@********.ru>
Date:   Mon Sep 20 23:14:08 2021 +0300

    First commit

commit a7257aa17bd34ac2e9b7cab636cfc8379c923865
Author: Igor V <igor@*****.pro>
Date:   Mon Sep 20 19:50:58 2021 +0300

    Initial commit

Перед последним коммитом был изменён user.email:
git config --global user.email

1. Будут проигнорированы локальные директории '.terraform'
2. файлы .tfstate содержащие в имени .tfstate либо в конце либо в середике названия.
3. фалы переменных содержащие пароли, закрытые ключи и т.п. - *.tfvars
4. файлы переопределения 
5. конфигурационные файлы CLI

git remote -v
```
bitbucket	https://Ingvar78@bitbucket.org/Ingvar78/devops-netology.git (fetch)
bitbucket	https://Ingvar78@bitbucket.org/Ingvar78/devops-netology.git (push)
gitlab	https://gitlab.com/Ingvar78/devops-netology.git (fetch)
gitlab	https://gitlab.com/Ingvar78/devops-netology.git (push)
origin	https://github.com/Ingvar78/devops-netology.git (fetch)
origin	https://github.com/Ingvar78/devops-netology.git (push)
```
