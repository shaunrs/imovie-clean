iMovie Clean
============

A small script which fixes the problem of iMovie 'copying' videos into its own directory, creating duplicates and unneccesarily using a lot of disk space.

It does this by removing the actual files, and replacing them with symbolic links to the original video file's location.


Usage
=====

The best way to use iMovie clean is to add it into crontab - perhaps hourly.

Once it has run once, it will only change new projects that have not already been optimised - and should you be using iMovie at runtime, it will simply exit without touching a thing.

To do so, open Terminal.app:

```bash
  crontab -e
  45 * * * * ~/imovie-clean.py &> ~/imovie-clean.log
```

  Then hit 'ESC' key, and type:

```
  :wq
```

  This will save and exit the crontab edit mode.


Authors
=======

iMovie Clean was created by [Shaun Smith](https://github.com/tuux1598g)


FAQ
===

## Does iMovie support symlinks?

Yes. In fact, when you first import a movie file to iMovie - it creates symlinks to each file so that you have 'immediate' access to those videos in iMovie. Otherwise you would need to wait for a long time to import before getting to work.

It then copies the original video file into your iMovie library, removes the symlink and moves the file into place.

## Why symlinks, and not hard links?

Hard links would have obvious advantages, such as source file rename not affecting iMovie - however they also have their disadvantages - primarily that Time Machine would treat both hard links as seperate files, and thus whilst saving space on your main drive, you would use double the space (for each file) on your time machine backup.

This may be acceptable, but for my use case I wanted to keep it simple.