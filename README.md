# Fundies-Assignment-Downloader
A hacked-together script to download all the homework a tutor has to grade.

To install all of the dependencies, install the following:

```
Google Chrome (it uses it by default, you can change it to Firefox or whatever but it's untested)
python2
selenium (python bindings, you can find it in pip)
```

To install selenium, just run this on the commandline (If running OSX/Linux and have pip installed):

```bash
pip install selenium
```

To run it, you simple call this from the command line:

```bash
python2 DownloadAssignments names.txt 4
```

In this case, the program will grab all the names in names.txt, and grab all of their completed Problem Set 4 assignments

names.txt can be any text file, the only condition is that it only contain full student names, with first and last separated by a space, and each complete name separated by a new line. For example:

```
  Foo Bar
  John Smith
  Jenny Weasely
```

There NEEDs to be a file called creds.txt that contains your husky id and your husky password, separated each by a newline. Like so:


```
  HUSKY-ID
  HUSKY-PASSWORD
```

I haven't test this on any other computer, so tell me if there is any problems!
