# Design Decisions

## Summary

This document will give the reader an understanding of the design decisions made in creating the `cli-abbreviation` command line tool

> Note: I tend to use interface & tool interchangably. My point of view is that a command line tool is a subset of a command line interface, where one could use multiple tools to accomplish some end (eg pipe chained commands)

## Problem Statement

The issue arose out of a solution, that is, I was able to compartmentalize a set of operations within a `Makefile` that allowed for an ease of development around (insert complex managed service), specific to Wayfair restrictions. While infinitely useful in the short-term, it quickly became obvious that the ridgid structure of make and more generally bash scripts would ultimately create a ceiling for the speed of dev cycles.

## Where to start?

The best design is one where the user can intuit the usage, typically based on experience with other tools of the same category. This gives rise to the question: How are other command line tools designed?

## System Design

One method of categorization is to look at the components necessary for the function of said command line tool. More specifically, there appears to be a pattern in where components are stored. Some tools operate exclusivly within the working directory, only "seeing" files, directories, variables, and operations within the local file system.

> This all gets rather abstract, talking what a [directory] or [file system] is in a way that is true to all compute systems, so I'll try to refrain from wading too much out of my depth...

[directory]: https://en.wikipedia.org/wiki/Directory_(computing)
[file system]: https://en.wikipedia.org/wiki/File_system

I've found that more modern tools will invoke a credentials and/or config file(s) present in a dot directory in the root of the user file system first and foremost. Their flexability is to anchor all operations in this root directory in addition to working directory operations. Older tools tend towards a more atomic way of operating, where they will either only operate on the files present within the current working directory OR at an operating system level. Rarely ever both.

So we have:
1. the source code that dictates the tool, compiled into a binary within the local filesystem or within the operating system shared resources (ie usr = Unix System Resources)
```bash
where python3
#/usr/local/bin/python3
#/usr/bin/python3
```
2. the local setup files that are acessed anywhere in the file system
```bash
aws configure list
#      Name                    Value             Type    Location
#      ----                    -----             ----    --------
#   profile                <not set>             None    None
#access_key     ****************BLH5 shared-credentials-file
#secret_key     ****************ddqy shared-credentials-file
#    region                us-west-1      config-file    ~/.aws/config

tree ~/.aws -a
#/Users/willcasswrig/.aws
#├── config
#└── credentials
#
#0 directories, 2 files
```
3. and assets within the filesystem of the current working directory
```bash
ls -lah
#total 328
#drwxr-xr-x  21 willcasswrig  staff   672B Dec  9 01:41 .
#drwxr-xr-x  20 willcasswrig  staff   640B Dec  4 01:18 ..
#-rw-r--r--   1 willcasswrig  staff   424B Dec  1 23:30 .editorconfig
#drwxr-xr-x  15 willcasswrig  staff   480B Dec  9 02:05 .git
#drwxr-xr-x   7 willcasswrig  staff   224B Dec  7 00:09 .github
#-rw-r--r--   1 willcasswrig  staff    10K Dec  8 02:59 .gitignore
#-rw-r--r--   1 willcasswrig  staff   782B Dec  8 02:59 .pre-commit-config.yaml
#-rw-r--r--   1 willcasswrig  staff    19B Dec  2 01:07 CODEOWNERS
#-rw-r--r--   1 willcasswrig  staff    32K Dec  1 23:30 LICENSE
#-rw-r--r--   1 willcasswrig  staff   3.2K Dec  2 01:07 Makefile
#-rw-r--r--   1 willcasswrig  staff    14K Dec  8 02:59 README.md
#drwxr-xr-x   8 willcasswrig  staff   256B Dec  8 02:59 common_sync
#-rw-r--r--   1 willcasswrig  staff   379B Dec  1 23:30 cookiecutter-config-file.yml
#drwxr-xr-x   3 willcasswrig  staff    96B Dec  9 01:41 docs
#-rw-r--r--   1 willcasswrig  staff    65K Dec  8 02:59 poetry.lock
#-rw-r--r--   1 willcasswrig  staff   3.6K Dec  8 02:59 pyproject.toml
#-rw-r--r--   1 willcasswrig  staff   697B Dec  8 01:00 requirements.txt
#drwxr-xr-x   7 willcasswrig  staff   224B Dec  8 02:59 scripts
#-rw-r--r--   1 willcasswrig  staff   100B Dec  1 23:30 setup.cfg
```

In some sense these are the "agents" modes of operating -- the strict scope of HOW it can operating is defined by the source code, file system is the subject that it can operate on/over, and the configuration is an abstraction layer that sits between the scope and context. It's middleware! Kinda, not really... middle-data?

## Linux Builtins

If you've ever been curious about some of the basic terminal commands on Linux systems, it's likely you've found yourself on this page:

```txt
BUILTIN(1)                                General Commands Manual

NAME
     builtin, !, %, ., :, @, [, {, }, alias, alloc, bg, bind, bindkey, break, breaksw, builtins, case, cd, chdir, command, complete, continue, default, dirs, do, done, echo, echotc, elif, else, end, endif, endsw, esac, eval, exec, exit, export, false, fc, fg, filetest, fi, for, foreach, getopts, glob, goto, hash, hashstat, history, hup, if, jobid, jobs, kill, limit, local, log, login, logout, ls-F, nice, nohup, notify, onintr, popd, printenv, printf, pushd, pwd, read, readonly, rehash, repeat, return, sched, set, setenv, settc, setty, setvar, shift, source, stop, suspend, switch, telltc, test, then, time, times, trap, true, type, ulimit, umask, unalias, uncomplete, unhash, unlimit, unset, unsetenv, until, wait, where, which, while – shell built-in commands

SYNOPSIS
     See the built-in command description in the appropriate shell manual page.

DESCRIPTION
	 Shell builtin commands are commands that can be executed within the running shell's process.  Note that, in the case of csh(1) builtin commands, the command is executed in a subshell if it occurs as any component of a pipeline except the last.

...
```

This -- found using `man cd`, or any number of arguments for the General Commands Manual -- providing a list of the core command line characters and operations.

I mention this because this set of CLI are shaped around the [Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) of design that perscribes a minimalist and modular approach to software development

## Modern Interfaces

A few of my favorite examples of modern CLI:

### AWS CLI

source code: [aws/aws-cli](https://github.com/aws/aws-cli)
core dependency: [pallets/click](https://github.com/pallets/click)
language: python

The original cloud compute interface, the AWS CLI paved the way for modern interfaces and abstractions around managed resource services (aka "the cloud")

### Bat

source code: [aws/aws-cli](https://github.com/aws/aws-cli)
core dependency: [clap-rs/clap](https://github.com/clap-rs/clap)
language: rust

A cat(1) clone with wings

### TheFuck

source code: [nvbn/thefuck](https://github.com/nvbn/thefuck)
core dependency: [pallets/click](https://github.com/pallets/click)
language: python

Magnificent app which corrects your previous console command
