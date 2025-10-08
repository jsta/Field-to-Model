# Field-to-Model

## temporary instructions - move to wiki:
1) `git clone --recurse-submodules https://github.com/NGEE-Arctic/field-to-model`
2) `cd field-to-model`
3) To run model container: `docker run -it -v $pwd:/home/modex_user yuanfornl/model-test:main-latest`
(Note: still needs volume mounts for input/output data)
4) To run visualization container: `docker run -it -v $(pwd):/home/modex_user yuanfornl/vis-test:main-latest`
