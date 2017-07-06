# UtilityFunctionWebapp
I have no idea what im doing but i did it

Use the function utilityCompiler with -pyfile interface.py:
python utilityCompiler -pyfile interface.py

and you will produce something like manfiest_of_interface.py.txt.
You can edit that file to eventually change the display settings

An additional benifit is that lots of text will be printed to the screen, and that is good (and will be fixed later to be more useful)

More comments and clearer varible names will be added later.

I'm currently working on a problem with documentation such as:
--FAR FAR             To be used with the --search-type=allsky argument.
                        This controls the number of background trials/jobs
as the regular expression cataches that as two different results

The logic seems to be working well... but it will not have complete functionality, there may be cases such as nested mutually exclusive arguments that need to be manually inputed like: (--ZooID | (Unique ID | Gravity ID)) would not be processed correctly. 
