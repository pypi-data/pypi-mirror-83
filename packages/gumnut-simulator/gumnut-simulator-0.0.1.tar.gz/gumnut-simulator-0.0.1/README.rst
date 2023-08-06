Gumnut Simulator
################

This projects contains several components which all revolve around Peter Ashenden's 8-bit soft-core
called *Gumnut*. For more information refer to *The Designers Guide to VHDL*
https://www.sciencedirect.com/book/9780120887859/the-designers-guide-to-vhdl

This repository was forked from my very first implementation created at the laboratory for digital
engineering at the University of Applied Sciences Augsburg back in 2015.



Documentation
*************

Please refer to https://gumnut-simulator.readthedocs.org



Changelog
*********



0.0.1
=====

Added
-----

-  Documentation (still in progress, though)
-  Introduced ``tox`` for handling testing, build, and publishing tasks
-  Introduced Github Actions for automated testing

Changed
-------

-  Replaced ``nosetest`` with ``pytest`` as the choice for unit and
   integration testing
-  Updated the existing tests for ``pytest``

Fixed
-----

-  Module imports were fixed
-  Enforced flake8 and (to some extend) pylint linting
