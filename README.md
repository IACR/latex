# latex

There are current three main pieces here:

1. the `iacrcc.cls` document class for the [IACR Communications in Cryptology](https://cic.iacr.org/).
2. A newer document class called `iacrj.cls` that can be used for the three IACR journals Communications
in Cryptology, TCHES, and ToSC.
3. the `iacrj.cls` depends upon a package `metacapture.sty` that provides the metadata capture of `iacrj.cls`.

Note that this depends upon cryptobib as a git submodule. Submodules are tricky. If
you want to pull in the latest version of the submodule, use

```
git submodule init
git submodule update

```



