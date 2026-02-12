# IACR LaTeX repository

This contains three major components:

1. the `metacapture.sty` package for metadata capture.
2. the `iacrj.cls` document class that can be used to produce journal articles
   for the three journals:
   * IACR Transactions on Cryptographic Hardware and Embedded Systems
   * IACR Transactions on Symmetric Cryptology
   * IACR Communications on Cryptology
3. the `iacrcc.cls` document class for the [IACR Communications in Cryptology](https://cic.iacr.org/)
   that has now been replaced by the `iacrj.cls` document class.

Note that this depends upon cryptobib as a git submodule. Submodules
are tricky. If you want to pull in the latest version of the
submodule, use

```
git submodule init
git submodule update

```



