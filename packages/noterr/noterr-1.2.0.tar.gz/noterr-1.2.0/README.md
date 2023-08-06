# noterr

A command line application to store all of your notes in a neat and clean manner

# Installation

You can install noterr through pip with the following command:

```bash
pip install noterr
```

Also, you can also install noterr through curl

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Japroz-Saini/noterr/master/install.sh)"
```

# Usage

Noterr is used to keep track of all your notes
We suggest you begin by typing the following:

```bash
noterr
```

You would see no output. That is because you have not created any folders. Try creating one with the following command:

```bash
noterr create-folder codes
```

Next if yout type the command:

```bash
noterr folder codes
```

You would see no output again.This because you have not added any notes to the codes folder. Try adding one with the following command:

```bash
noterr folder codes add 'This is a note'
```

Now if you type

```bash
noterr folder codes
```

You would see the notes in that folder. Currently, that note is uncomplete. If you have completed the note you can type the command

```bash
noterr folder codes done 'This is a note'
```

Now you would see that the note has changes its color. This is for you to be able to distinguish between done and undone done.

# Deleting

You can delete a folder with the following command:

```bash
noterr delete-folder codes
```

Which will delete the folder codes

You can also delete an item from a folder with the following command:

```bash
noterr folder codes del 'This is a note'
```

# Hidden

Noterr has various hidden commands which do various things in the teriminal.
One of them is `noterr tictac` which starts a multiplayer tic-tac-toe game. Discover commands and create the issue with the command and what it does to be featured on the documentation!
