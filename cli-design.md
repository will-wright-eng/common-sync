# Design Decisions

## Summary

This document will give the reader an understanding of the design decisions made in creating the `csdf` command line tool

## Problem Statement

The issue arose out of a solution, that is, I was able to compartmentalize a set of operations within a `Makefile` that allowed for an ease of development around GCP Dataflow Flex Templates, specific to Wayfair restrictions. While infinitely useful in the short-term, it quickly became obvious that the ridgid structure of make and more generally bash scripts would ultimately create a ceiling for the speed of dev cycles.

## Where to start?

The best design is one where the user can intuit the usage, typically based on experience with other tools of the same category. This gives rise to the question: How are other command line tools designed?

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

This -- found using `man cd` or any number of arguments for the General Commands Manual -- providing a list of the core command line characters and operations.

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
