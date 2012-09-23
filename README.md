# EZSocksProxy - EZProxy-to-SOCKS

"EZProxy" is a link-rewriting proxy used by many libraries to allow
remote off-site access to protected resources. Because it's pervasive
and easy to integrate with, there is quite a lot of academic software
which supports EZProxy but doesn't support other proxy types.

EZSocksProxy is a small Python script that provides an EZProxy-like
interface to a SOCKS tunnel. This interface lets you do things like
forward requests from bibliography management software via SSH.

## Installation

EZSocksProxy is packaged using Python `setuptools` and can be
installed using standard procedures.

    python setup.py install

## Usage

Consider a common usage scenario: There is a SOCKS proxy provided by
SSH running on port 9090. In order to start an EZProxy on port 9091,
run:

    ezsocksproxy localhost:9090 9091
