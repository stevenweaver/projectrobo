# Introduction #

Assuming everyone is using windows, this guide is for windows only.

We are going to try out using svn for most of our documents. This will ensure that our documents are easily maintained and under version control. Despite an initial(albeit small) learning curve, rest assured it will be worth our endeavor. If not for anything else other than becoming acquainted with what most companies use who deal with even the slightest amount of code. This goes without mentioning the large amounts of aspirin saved from preventing headaches associated with ill organization.

The program we're using is **TortoiseSVN**

Well, let's carry on then shall we?

# Details #

## Installation ##

Go here: http://tortoisesvn.net/downloads

In case you can't find the installer on the page(32-bit install):

http://downloads.sourceforge.net/tortoisesvn/TortoiseSVN-1.6.7.18415-win32-svn-1.6.9.msi?download


## Check Out ##

### Variables ###
  * username and password
  * url for repository = https://projectrobo.googlecode.com/svn/trunk


### Routine ###
  * Open 'My Documents'
  * Create a new folder called 'projectrobo' (or whatever else your heart desires)
  * Right click on 'projectrobo' and select 'SVN Checkout'
  * Enter the url to your repository
  * Enter C:\My Documents\projectrobo for 'Checkout directory'
  * Select 'HEAD revision' for 'Revision'
  * Click 'OK'


## Working with SVN ##
If you right click on the folder under version control, you will see a lot of options available to you. These are the ones that you have to worry about.

### Add ###
You need to add a file first before committing. An unadded file will have a green question mark

### Remove ###
Mark for removal. The file will have a red exclamation mark until you commit

### Update ###
Get other people's updates(do this everytime before you start working and before you commit)

### Commit ###
Commit all of your changes. Do this as often as you possibly can.

## Conclusion ##
This so far has been written from memory. If there's any questions or concerns regarding the process please feel free to contact me. I feel bad for potentially consternating some of you, but I reiterate that this is something worth learning.