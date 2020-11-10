Run the following command in command line to create a virtualenv for the the application.

python3 -m virtualenv <name_of_virtual_environment>
Note: Make sure path to scripts and python3 is already set in system environment of the system.

Now activate the virtualenv by running commond:

On windows machine-
<name_of_virtual_environment>\Scripts\activate

On Linux machine-
source <name_of_virtual_environment>/bin/activate

Goto the application directory.In this case-
cd BuzzFeed

Run the following command in the command prompt/terminal to install all required moduls.

pip install -r requirments.txt
