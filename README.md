# Field-to-Model

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
