# Pointers

## ruamel.yaml

`Yamkix` relies on the awesome [ruamel.yaml](https://yaml.dev/doc/ruamel.yaml/) package.

## kubesplit

- [kubesplit](https://github.com/looztra/kubesplit) (from the same author as `yamkix`) uses `yamkix` under the hood to format the yaml descriptors that it generates.
- We try to make sure `kubesplit` compatible with `yamkix`. Please create issues in either [yamkix github repo](https://github.com/looztra/yamkix/issues) or [kubesplit github repo](https://github.com/looztra/kubesplit/issues) if you think we broke something.

## Using `yamkix` API

- In the future, we will try to not generate breaking changes in the functions and classes that we consider `public`, i.e. the ones declared in the `yamkix` root [__init__.py](https://github.com/looztra/yamkix/blob/main/src/yamkix/__init__.py).
  - if you think we did break the API contract, please [raise an issue](https://github.com/looztra/yamkix/issues).
  - if you are using something else that what is declared in the root package, please get in touch so that we know about it and see what we can do for you.
