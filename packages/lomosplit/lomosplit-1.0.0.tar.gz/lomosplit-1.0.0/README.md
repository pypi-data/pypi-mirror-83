# LomoSplit

Utility for splitting [LomoKino](https://shop.lomography.com/en/lomokino) film scans.

![Example of work](https://storage.yandexcloud.net/meownoid-pro-static/external/github/lomosplit/example.jpg)

### Installation
```shell script
pip install lomosplit
```

### Usage

To use lomosplit with default parameters just pass as only parameter image name or
path to directory with images.

```shell script
python -m lomosplit scan.jpeg
```

```shell script
python -m lomosplit path/to/scans
```

You can also specify advanced options. List of all advanced options with their descriptions
is available by calling the `python -m lomosplit --help`.

```shell script
python -m lomosplit \
     -o output \
     --quiet \
     --template "picture_{idx:05d}" \
     --format png \
     --rotate-image left \
     --rotate-frame right \
     --frame-min-height 500 \
     --frame-max-height 900 \
     --adjust-to-max-height \
...
```
