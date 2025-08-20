# Changelog

## [0.13.0](https://github.com/looztra/yamkix/compare/v0.12.0...v0.13.0) (2025-08-20)


### Features

* **quotes:** provide the option `--enforce-double-quotes` to use double quotes when cleaning up quotes with `--no-preserve-quotes` ([#271](https://github.com/looztra/yamkix/issues/271)) ([6ee1a00](https://github.com/looztra/yamkix/commit/6ee1a00116b41e50f9f36208ba9784f1d8999cd4))
* **stdin/stdout:** ignore case when specifying explicit STDIN/STDOUT ([#272](https://github.com/looztra/yamkix/issues/272)) ([aca3262](https://github.com/looztra/yamkix/commit/aca3262986fd78a1396ada30d8cf446ea52d520c))


### Bug Fixes

* **docs:** remove extra back tick in usage.md that prevent code block display ([#267](https://github.com/looztra/yamkix/issues/267)) ([eb39654](https://github.com/looztra/yamkix/commit/eb39654a6d5915e64bf0b76d84dab77b61e3e583))


### Documentation

* **cli:** add some extra docs regarding stdin/stdout usage ([#264](https://github.com/looztra/yamkix/issues/264)) ([c572ccc](https://github.com/looztra/yamkix/commit/c572cccce02e25f769da8845773cf394283918f3))

## [0.12.0](https://github.com/looztra/yamkix/compare/v0.11.1...v0.12.0) (2025-08-18)


### Features

* **inputs:** support formatting multiple files at once ([c16ffb7](https://github.com/looztra/yamkix/commit/c16ffb79447d831bf3961346b4f2863e33c3cbce))
* **pre-commit:** you can now use yamkix as a pre-commit hook ([c16ffb7](https://github.com/looztra/yamkix/commit/c16ffb79447d831bf3961346b4f2863e33c3cbce))


### Bug Fixes

* **inputs:** explicit STDIN input now works as documented ([c16ffb7](https://github.com/looztra/yamkix/commit/c16ffb79447d831bf3961346b4f2863e33c3cbce))


### Documentation

* **cli:** document the usage as a cli and as a pre-commit hook ([c16ffb7](https://github.com/looztra/yamkix/commit/c16ffb79447d831bf3961346b4f2863e33c3cbce))

## [0.11.1](https://github.com/looztra/yamkix/compare/v0.11.0...v0.11.1) (2025-08-13)


### Bug Fixes

* **docs:** use the correct path to changelog url in README.md that is also pushed to PyPi ([#251](https://github.com/looztra/yamkix/issues/251)) ([06d88a5](https://github.com/looztra/yamkix/commit/06d88a50c7a79378a794e9baa8c0ede19ea7cd38))

## [0.11.0](https://github.com/looztra/yamkix/compare/v0.10.0...v0.11.0) (2025-08-13)


### Features

* **api:** clarify API by exporting an explicit list of features in the root __init__ module ([e4ad750](https://github.com/looztra/yamkix/commit/e4ad75064be09e38a8b3793f291c4a8cbc0a23ef))
* **ci:** make Release Please generated CHANGELOG in mkdocs folder ([#245](https://github.com/looztra/yamkix/issues/245)) ([7b4c143](https://github.com/looztra/yamkix/commit/7b4c143927d952a7202538ba51a7b9c469d6dcb7))
* **refactor:** switch from argparse to Typer ([e4ad750](https://github.com/looztra/yamkix/commit/e4ad75064be09e38a8b3793f291c4a8cbc0a23ef))
* **silent-mode:** provide a silent mode that doesn't print config when processing file(s) ([e4ad750](https://github.com/looztra/yamkix/commit/e4ad75064be09e38a8b3793f291c4a8cbc0a23ef))


### Bug Fixes

* **ci:** adjust conditions for github artifact upload ([#241](https://github.com/looztra/yamkix/issues/241)) ([ec32bae](https://github.com/looztra/yamkix/commit/ec32bae054b6fc47cfad7476432915d0032a2903))
* **ci:** deploy pre-release when on a Release Please PR ([#240](https://github.com/looztra/yamkix/issues/240)) ([2bfc4b2](https://github.com/looztra/yamkix/commit/2bfc4b25029327b0a82dba2ed8f7c1a525fdb313))
* correctly pass APP_VERSION ([#136](https://github.com/looztra/yamkix/issues/136)) ([6cabac5](https://github.com/looztra/yamkix/commit/6cabac5af20c21c66a85be87bc7b4aea3ab8f900))
* **lint:** make ruff and pyright run without errors ([#147](https://github.com/looztra/yamkix/issues/147)) ([b878120](https://github.com/looztra/yamkix/commit/b87812041094b58ae546278846b4dd76108443a1))
* update ec config ([#137](https://github.com/looztra/yamkix/issues/137)) ([bbfe2ea](https://github.com/looztra/yamkix/commit/bbfe2ea4823d0bb339ccde5a1a54466eb86471a1))


### Documentation

* **mkdocs:** add search bar, tune theme and display ([#243](https://github.com/looztra/yamkix/issues/243)) ([5a9405a](https://github.com/looztra/yamkix/commit/5a9405a4c98216d6e8fc0825f2ab02ae7d85e246))
* **mkdocs:** init docs managed by mkdocs ([e4ad750](https://github.com/looztra/yamkix/commit/e4ad75064be09e38a8b3793f291c4a8cbc0a23ef))


### Code Refactoring

* **config:** use dataclasses for a better config management ([#156](https://github.com/looztra/yamkix/issues/156)) ([9e12d3d](https://github.com/looztra/yamkix/commit/9e12d3db0612e8ddb17fe466d4c61e4a80b38ac3))


### Continuous Integration

* **checks:** use a single finalizer required check ([#248](https://github.com/looztra/yamkix/issues/248)) ([0229d1f](https://github.com/looztra/yamkix/commit/0229d1f56258a20c3eb917da479730432b39e528))
* **lint pr title:** setup lint pr title workflow ([#145](https://github.com/looztra/yamkix/issues/145)) ([f26738e](https://github.com/looztra/yamkix/commit/f26738e842072b879d21b60572572fdc4f5eb481))
* **publish:** push to testpypi on Release Please pr and not on push to main ([e4ad750](https://github.com/looztra/yamkix/commit/e4ad75064be09e38a8b3793f291c4a8cbc0a23ef))
* **release:** setup release please workflow ([#159](https://github.com/looztra/yamkix/issues/159)) ([c215e34](https://github.com/looztra/yamkix/commit/c215e3499df7e2d8d0c58eb84d0cc6ef2dd5c8be))
* **release:** upload artifact if we need to release ([#141](https://github.com/looztra/yamkix/issues/141)) ([1ea5257](https://github.com/looztra/yamkix/commit/1ea525775d3c61dd1d1e5b7bbc60ada26ac76e6e))
