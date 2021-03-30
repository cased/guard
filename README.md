`cased`
==========================================

**Guard your team's critical command line infrastructure with Cased**

Overview
-----------

`cased` is the command-line tool for configuring and running [Cased CLI](https://cased.com/guard).
It works via simple _shims_ that wrap your other command-line programs.
It handles the hard parts of configuring these shims, and keeps itself up-to-date
with changes and additions to your remote Cased configuration.


Requirements & Install
-----------------------

The only requirement to run `cased` is Python 3.5 or better. There are several easy ways to install
the program.

You can install using Homebrew via our [tap](https://github.com/cased/homebrew-tap):

```
brew install cased/tap/cased
```

You can install the `cased` program system-wide (or into a `virtualenv`) with pip:

```
python3 -m pip install cased
```

Note that this creates two programs, `cased` and `cased-init`, which will then be
available on your `PATH`.

Alternatively, you can clone this repo and run:

```
./install
```


Quick Setup
-----------------------

Now _initialize_ the tool. You need to make sure `cased-init` (a single-purpose `init` script)
runs every time a shell starts. To do that, just add this line to your `~/.bashrc`, `~/.zshrc`,
or similar file:

```
eval "$(cased-init -)"
```

Next, configure Cased with your unique user token. This will also sync your local client
with your Cased remote settings.

```
cased configure <your-user-token>
```

You can also just run:

```
cased configure
```

and follow the web-based connect instructions.

Lastly, start a new shell for the environment changes to take effect.

You can confirm the entire installation with:

```
cased verify
```

If you encounter any installation issues, please check our
[Troubleshooting support page](https://docs.cased.com/docs/troubleshooting).

Usage
------

After you've installed `cased` and configured it, you're all set.
Just run your programs as usual, and any that have been configured by
your Cased server will run under `cased`.

We recommend you periodically (and automatically)
run `cased sync` to keep your local guarded programs up-to-date
with your remote configuration. However, even if  you don't do this,
the `cased` client will still check its remote server for
updates whenever it is invoked.

Configuration
---------------

The Cased remote server defaults to `api.cased.com`. To change that
url, just set with:

```
cased url <your-remote-server>
```

You can also reset the URL to use the default:

```
cased url --reset
```

Cased CLI supports experimental recording of session output. To enable the functionality, 
set the `CASED_RECORDING_ENABLED` like this:

```
export CASED_RECORDING_ENABLED=1
```


Internal commands
------------------

Although not needed for regular use, `cased` does expose some low-level
plumbing commands:

**List available local shims**

To see all currently installed shims:

```
cased local-shims
```

**List available remote shims**

To see all remote  shims:

```
cased remote-shims
```

Uninstalling
---------------------

Since the Cased client is so lightweight, you can simply
remove the ` eval "$(cased-init -)"` from your shell startup script,
and open a new shell. Programs will no longer be guarded.

To _completely_ remove a Cased install, you can `rm`
the `~/.cguard/` directory, where the client stores data, although
this isn't strictly necessary. You can also remove the
`cased` and `cased-init` programs, which are likely
in `/usr/local/bin/` or a similar location (try `which cased`
and `which cased-init` to find their location.)
