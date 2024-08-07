# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [3.6.1](https://github.com/WuLiFang/cgtwq/compare/v3.6.0...v3.6.1) (2021-12-15)

### Bug Fixes

- should import configparser from six 8fe8afc

## [3.6.0](https://github.com/WuLiFang/cgtwq/compare/v3.5.4...v3.6.0) (2021-11-09)

### Features

- read desktop client ws port from config file f9a298e

## [3.5.4](https://github.com/WuLiFang/cgtwq/compare/v3.5.3...v3.5.4) (2021-10-11)

### Bug Fixes

- wrong image upload result 3e2cc4b

## [3.5.3](https://github.com/WuLiFang/cgtwq/compare/v3.5.2...v3.5.3) (2021-10-11)

### Bug Fixes

- makedirs error in python2.7 62cd8ff

## [3.5.2](https://github.com/WuLiFang/cgtwq/compare/v3.5.1...v3.5.2) (2021-10-11)

### Bug Fixes

- error when flow.submit to cgteamwork v6.1 729f404

## [3.5.1](https://github.com/WuLiFang/cgtwq/compare/v3.5.0...v3.5.1) (2021-10-10)

### Bug Fixes

- cannot get desktop client v6.1 executable path 4e49c2b
- flow.submit not work 7565edb
- handle psutil.AccessDenied 335757a

## [3.5.0](https://github.com/WuLiFang/cgtwq/compare/v3.4.1...v3.5.0) (2021-09-24)

### Features

- rename link.link to link.add, link.unlink to link.remove 6d6909d

### Bug Fixes

- invalid syntax for python2 3860864
- selection link.add not work in cgteamwork6.1 86b3d24
- selection link.remove not work in cgteamwork6.1 a09e4cc

## [3.4.1](https://github.com/WuLiFang/cgtwq/compare/v3.4.0...v3.4.1) (2021-09-24)

### Bug Fixes

- filebox.from_id error when using cgteamwork6.1 63028a5

## [3.4.0](https://github.com/WuLiFang/cgtwq/compare/v3.3.2...v3.4.0) (2021-09-24)

### Features

- add flow.list_submit_file b6320a2

### Bug Fixes

- **build:** should not include tests as package ff2c270

## [3.3.2](https://github.com/WuLiFang/cgtwq/compare/v3.3.1...v3.3.2) (2021-09-24)

### Bug Fixes

- helper.wlf.get_entry_by_file using old field name d44d041

## [3.3.1](https://github.com/WuLiFang/cgtwq/compare/v3.3.0...v3.3.1) (2021-09-24)

### Bug Fixes

- missing packages when install from archive eb5f943

## [3.3.0](https://github.com/WuLiFang/cgtwq/compare/v3.2.3...v3.3.0) (2021-09-23)

### Features

- support cgteamwork6.1 fde078b

## [3.2.3](https://github.com/WuLiFang/cgtwq/compare/v3.2.2...v3.2.3) (2021-06-24)

### Bug Fixes

- wrong id from other module returned by filter b2ca9ed

## [3.2.2](https://github.com/WuLiFang/cgtwq/compare/v3.2.1...v3.2.2) (2021-06-23)

### Bug Fixes

- follow link api change 66fef10

## [3.2.1](https://github.com/WuLiFang/cgtwq/compare/v3.2.0...v3.2.1) (2021-06-18)

### Bug Fixes

- error when filter on asset module c37b6cd
- error when send http request c881fb7
- wrong link data 7afb5c6

## [3.2.0](https://github.com/WuLiFang/cgtwq/compare/v3.1.1...v3.2.0) (2021-04-02)

### Features

- read filename prefix from field aab02d1

## [3.1.1](https://github.com/WuLiFang/cgtwq/compare/v3.1.0...v3.1.1) (2021-03-19)

## [3.1.0](https://github.com/WuLiFang/cgtwq/compare/v3.0.3...v3.1.0) (2021-03-19)

### Features

- add type hints 1007dd7

## [3.0.3](https://github.com/WuLiFang/cgtwq/compare/v3.0.2...v3.0.3) (2021-03-19)

- replace package `wlf`

  with `pathlib2-unicode` + `deprecated` + `cast-unknown` fc2d5ed

## [3.0.2](https://github.com/WuLiFang/cgtwq/compare/v3.0.1...v3.0.2) (2021-03-11)

### Bug Fixes

- wrong handling for desktop client True result cfce99b

## [3.0.1](https://github.com/WuLiFang/cgtwq/compare/v3.0.0...v3.0.1) (2021-03-11)

### Bug Fixes

- wrong requires version specifier 63884c6

## [3.0.0](https://github.com/WuLiFang/cgtwq/compare/v3.0.0-beta.4...v3.0.0) (2021-03-11)

### Features

- use better error message 2540a03

### Bug Fixes

- correct logger name for server.http 4da2d7b
- handle desktop client returns True when not logged in a9ae762
- wrong order when get filename_prefix map e4cdfaf
- wrong reverse sort a2c1a70

## [3.0.0-beta.4](https://github.com/WuLiFang/cgtwq/compare/v3.0.0-beta.3...v3.0.0-beta.4) (2020-11-13)

## [3.0.0-beta.3](https://github.com/WuLiFang/cgtwq/compare/v3.0.0-beta.2...v3.0.0-beta.3) (2020-11-13)

## [3.0.0-beta.2](https://github.com/WuLiFang/cgtwq/compare/v3.0.0-beta.1...v3.0.0-beta.2) (2020-06-24)

## [3.0.0-beta.1](https://github.com/WuLiFang/cgtwq/compare/v3.0.0-beta.0...v3.0.0-beta.1) (2020-06-24)

### Features

- add helper.wlf.get_entry_by_file 687ff42
- export dummy client when is not on windows 9b13ac2
- raise `EmptySelection` 434455a

### Bug Fixes

- correct EmptySelection message b354efe
- EmptySelection backward compatibility ed028e8
- plugin argument payload serialization 9b9c50c
- WebSocketTimeoutException when no client installed af9fc01
- **helper.wlf:** filename match should use exact match first 79a0717

## 3.0.0-beta.0 (2019-06-28)

### Features

- add `EmptySelection` exception. ([2d91ed6](https://github.com/WuLiFang/cgtwq/commit/2d91ed6))

### Tests

- fix broken test ([f60fabf](https://github.com/WuLiFang/cgtwq/commit/f60fabf))

## 3.0.0-alpha.8 (2019-01-11)

## 3.0.0-alpha.7 (2018-12-15)

## 3.0.0-alpha.6 (2018-11-15)

## 3.0.0-alpha.5 (2018-11-06)

## 3.0.0-alpha.4 (2018-09-28)

## 3.0.0-alpha.3 (2018-09-27)

## 3.0.0-alpha.2 (2018-09-27)

## 3.0.0-alpha.1 (2018-09-27)

## 3.0.0-alpha.0 (2018-09-26)

## 2.5.0 (2018-08-31)

### 2.4.2 (2018-08-13)

### 2.4.1 (2018-08-07)

## 2.4.0 (2018-08-07)

## 2.3.0 (2018-07-27)

### 2.2.1 (2018-07-23)

## 2.2.0 (2018-07-23)

### 2.1.1 (2018-07-23)

## 2.1.0 (2018-07-23)

### 2.0.1 (2018-07-20)

## 2.0.0 (2018-07-20)

## 1.4.0 (2018-06-25)

### 1.3.2 (2018-05-22)

### 1.3.1 (2018-05-21)

## 1.3.0 (2018-05-21)

### 1.2.1 (2018-04-13)

## 1.2.0 (2018-04-10)

## 1.1.0 (2018-03-30)

### 1.0.3 (2018-03-30)

### 1.0.2 (2018-03-28)

### 1.0.1 (2018-03-28)

## 1.0.0 (2018-03-28)
