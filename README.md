secret_mp
=========

Private repository for research project on secret message passing on complex networks.


####Now What?####
=================
(I'm assuming you're running Linux.  Windows probably is not much more complicated but I don't know off the top of my head )

Install git `sudo apt-get install git` or similar.

Navigate to a directory in which you would like to create the directory for this repo, then run:

`git clone https://github.com/mmdanziger/secret_mp.git`

Edit the files in your regular editor.  When you have finished making a set of changes that constitute some sort of cohesive unit run

`git commit -m "I added an explanation where it was needed"`
 
You can append a filename to the command in which case only that file will be committed or you can leave it blank and all of the files that you modified will be committed.   When you're ready to share them with the group run

`git push` 

From now on, before making changes run 

`git pull`

`git merge`

This ensures that you are editing the most up-to-date version of the files.

I'm not a super git ninja (most of my experience is with mercurial) but I think that this is enough to get you started.

####Tips####
============

* When editing the LaTeX source, make sure not to allow lines that are too long.  The reason is that when the merge algorithm runs, it works on a line-by-line comparison.  Therefore if there is a very long line, even though you have only changed one or two words, the merge algorithm is liable to choke and you'll have to go through the whole thing manually.

* You can edit the files directly online if you'd prefer.
* I highly recommend switching from HTTPS to SSH.  Just copy your public key into the designated box in your account settings and switch from https to ssh as detailed at https://help.github.com/articles/changing-a-remote-s-url . This way you never have to type in authentication information.
