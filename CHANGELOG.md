# Changelog

All notable changes to Guitar Engine will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Version scheme moved from CalVer `2026.1.0` to SemVer `1.0.0`, per the
  standard.
- Brought to the standard in `C:\dev\Design\fusion`: module docstring and the
  seven metadata dunders, bare `except:` converted to `except Exception`, and
  the supporting files (LICENSE, CHANGELOG, .gitignore) added.

## [1.0.0] - 2026-02-26

### Added

- Parametric guitar generation: fretboard, blanks, strings, pickups and dimensions, with settings persisted in design attributes.
