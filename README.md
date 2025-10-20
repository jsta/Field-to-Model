# Field-to-Model

> temporary instructions - move to wiki:

## Setup

```shell
# # data
git clone --recurse-submodules https://github.com/NGEE-Arctic/field-to-model
cd field-to-model
docker volume create workshop_data

# # to build model container
# # (this will take a while, please open an issue for any build failures)
docker build -t model-container -f Docker/Dockerfile-models . 

# # to build visualization container
docker build -t vis-container -f Docker/Dockerfile-vis .

# # to run before CI is finalized:
# # Model container:
docker run -it -v $(pwd):/home/modex_user -v workshop_data:/home/modex_user/data yuanfornl/model-test:main-latest

# # Vis container (@jsta this will need some work) - a) launch jupyter lab with same folder mounts; b) connect over localhost

# # When CI is up/more robust:
# # To run model container:
docker run -it -v $(pwd):/home/modex_user yuanfornl/ngee-modex-models:main-latest

# # (Note: still needs volume mounts for input/output data)
# # To run visualization container: 
docker run -it -v $(pwd):/home/modex_user yuanfornl/ngee-modex-visualization:main-latest
```

## Usage

```shell
# # model image

# # visualization image
docker pull yuanfornl/vis-test:main-latest

docker run -it --init \
    --mount type=bind,source=$(pwd),target=/home/joyvan/workdir -w /home/joyvan/workdir -p 9999:9999 \
    yuanfornl/vis-test:main-latest

docker run -it --init \
    --mount type=bind,source=$(pwd),target=/home/joyvan/workdir -w /home/joyvan/workdir -p 8888:8888 \
    vis-test
```


## TEM Minimal Running Example

### Build Images

Ultimately this will be done by CI but this is the command I was using for dev.
Note the means of getting the version ID from TEM repo. This gets injected into
the compiled binary.

```shell
docker build -t model-container -f Docker/Dockerfile-models .  
```

### Start Container

Start the container but mount the folder with the example test in it.

```shell
docker run -it --rm \
    -v $(pwd)/model_examples:/home/modex_user/model_examples \
    model-container:latest
```

### Demo run

Proof of concept that the installation and compilation worked assuming 
volume mounted as above.

```shell
modex_user@be4136f0600d:~$ ./model_examples/TEM/test.sh 
```


## E3SM Demo Runs

1) Create volumes:
```shell
docker volume create inputdata
docker volume create workshop_output
```

2) Get input data
```shell
docker run -v inputdata:/home/modex_user/inputdata -v $(pwd)/tools:/home/modex_user/tools /home/modex_user/tools/scripts/get_inputdata.sh
```


