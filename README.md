# devops-netology 


### Домашнее задание к занятию «2.4. Инструменты Git»
Для выполнения заданий в этом разделе давайте склонируем репозиторий с исходным кодом терраформа https://github.com/hashicorp/terraform

В виде результата напишите текстом ответы на вопросы и каким образом эти ответы были получены.

1. Найдите полный хеш и комментарий коммита, хеш которого начинается на aefea.

<pre>~/Documents/terraform (main)$ git log aefea 
<font color="#C4A000">commit aefead2207ef7e2aa5dc81a34aedf0cad4c32545</font>
Author: Alisdair McDiarmid &lt;alisdair@users.noreply.github.com&gt;
Date:   Thu Jun 18 10:29:58 2020 -0400

    Update CHANGELOG.md
</pre>


2. Какому тегу соответствует коммит 85024d3?

<pre>~/Documents/terraform (main)$ git show 85024d3
<font color="#C4A000">commit 85024d3100126de36331c6982bfaac02cdab9e76 (</font><font color="#FCE94F"><b>tag: v0.12.23</b></font><font color="#C4A000">)</font>
Author: tf-release-bot &lt;terraform@hashicorp.com&gt;
Date:   Thu Mar 5 20:56:10 2020 +0000

    v0.12.23

</pre>

3. Сколько родителей у коммита b8d720? Напишите их хеши.

<pre>~/Documents/terraform (main)$ git show --oneline b8d720^ 
<font color="#C4A000">56cd7859e</font> Merge pull request #23857 from hashicorp/cgriggs01-stable
</pre>


<cut>

<pre>~/Documents/terraform (main)$ git log b8d720 --graph 
*   <font color="#C4A000">commit b8d720f8340221f2146e4e4870bf2ee0bc48f2d5</font>
<font color="#CC0000">|</font><font color="#4E9A06">\</font>  Merge: 56cd7859e 9ea88f22f
<font color="#CC0000">|</font> <font color="#4E9A06">|</font> Author: Chris Griggs &lt;cgriggs@hashicorp.com&gt;
<font color="#CC0000">|</font> <font color="#4E9A06">|</font> Date:   Tue Jan 21 17:45:48 2020 -0800
<font color="#CC0000">|</font> <font color="#4E9A06">|</font> 
<font color="#CC0000">|</font> <font color="#4E9A06">|</font>     Merge pull request #23916 from hashicorp/cgriggs01-stable
<font color="#CC0000">|</font> <font color="#4E9A06">|</font>     
<font color="#CC0000">|</font> <font color="#4E9A06">|</font>     [Cherrypick] community links
<font color="#CC0000">|</font> <font color="#4E9A06">|</font> 
<font color="#CC0000">|</font> * <font color="#C4A000">commit 9ea88f22fc6269854151c571162c5bcf958bee2b</font>
<font color="#CC0000">|/</font>  Author: Chris Griggs &lt;cgriggs@hashicorp.com&gt;
<font color="#CC0000">|</font>   Date:   Tue Jan 21 17:08:06 2020 -0800
<font color="#CC0000">|</font>   
</pre>
</cut>

>2 родителя:


56cd7859e 9ea88f22f

9ea88f22fc6269854151c571162c5bcf958bee2b
56cd7859e05c36c06b56d013b55a252d0bb7e158


<pre>~/Documents/terraform (main)$ git show b8d720^
<font color="#C4A000">commit 56cd7859e05c36c06b56d013b55a252d0bb7e158</font>
Merge: 58dcac4b7 ffbcf5581
Author: Chris Griggs &lt;cgriggs@hashicorp.com&gt;
Date:   Mon Jan 13 13:19:09 2020 -0800

    Merge pull request #23857 from hashicorp/cgriggs01-stable
    
    [cherry-pick]add checkpoint links

</pre>

<cut>
<pre>~/Documents/terraform (main)$ git show b8d720^2
<font color="#C4A000">commit 9ea88f22fc6269854151c571162c5bcf958bee2b</font>
Author: Chris Griggs &lt;cgriggs@hashicorp.com&gt;
Date:   Tue Jan 21 17:08:06 2020 -0800

    add/update community provider listings

</pre>

</cut>



4. Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами v0.12.23 и v0.12.24.

<cut>

<pre>~/Documents/terraform (main)$ git log --oneline v0.12.23..v0.12.24
<font color="#C4A000">33ff1c03b (</font><font color="#FCE94F"><b>tag: v0.12.24</b></font><font color="#C4A000">)</font> v0.12.24
<font color="#C4A000">b14b74c49</font> [Website] vmc provider links
<font color="#C4A000">3f235065b</font> Update CHANGELOG.md
<font color="#C4A000">6ae64e247</font> registry: Fix panic when server is unreachable
<font color="#C4A000">5c619ca1b</font> website: Remove links to the getting started guide&apos;s old location
<font color="#C4A000">06275647e</font> Update CHANGELOG.md
<font color="#C4A000">d5f9411f5</font> command: Fix bug when using terraform login on Windows
<font color="#C4A000">4b6d06cc5</font> Update CHANGELOG.md
<font color="#C4A000">dd01a3507</font> Update CHANGELOG.md
<font color="#C4A000">225466bc3</font> Cleanup after v0.12.23 release
</pre>

</cut>

5. Найдите коммит в котором была создана функция func providerSource, ее определение в коде выглядит так func providerSource(...) (вместо троеточего перечислены аргументы).
6. Найдите все коммиты в которых была изменена функция globalPluginDirs.
7. Кто автор функции synchronizedWriters?
