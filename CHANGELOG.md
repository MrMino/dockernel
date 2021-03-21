# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Nothing yet

### Changed
- Nothing yet

## [1.0.2] - 2021-03-21
### Changed
- Fixed `AttributeError` when "dockernel" command was used without any
  subcommand.
- (Windows) Fixed wrong kernelspec directory path being used with "dockernel
  install".
- (Windows) Fixed kernelspecs using `/usr/bin/env python` instead of just
  `python`.
- Changed network mode to bridge and explicitly mapped the ports. 

## [1.0.1] - 2021-01-17
### Changed
- Default interrupt mode will now be set to "message" when installing a kernel.
  This helps with container stopping unexpectedly or not closing after shutting
  the notebook.

## [1.0.0] - 2020-07-09
### Added
- First working version of `dockernel install` and `dockernel start`.

[unreleased]: https://github.com/mrmino/dockernel/v1.0.2...HEAD
[1.0.2]: https://github.com/mrmino/dockernel/releases/tag/v1.0.2
[1.0.1]: https://github.com/mrmino/dockernel/releases/tag/v1.0.1
[1.0.0]: https://github.com/mrmino/dockernel/releases/tag/v1.0.0
