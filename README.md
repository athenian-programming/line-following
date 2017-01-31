# OpenCV Line Following

## Package Dependencies

Install the following Python packages: 

* [gRPC](http://www.grpc.io/docs/guides/index.html) 
as described [here](http://www.athenian-robotics.org/grpc/)

* [OpenCV](http://opencv.org) 
as described [here](http://www.athenian-robotics.org/opencv/)

* [imutils](https://github.com/jrosebr1/imutils)
as described [here](http://www.athenian-robotics.org/imutils/)

* [numpy](http://www.numpy.org)
as described [here](http://www.athenian-robotics.org/numpy/)


## Line Follower

### Usage 

```bash
$ line_follower.py --bgr "[174, 56, 5]" --display 
```

### CLI Options

| Option         | Description                                        | Default |
|:---------------|----------------------------------------------------|---------|
| -b, --bgr      | BGR target value                                   |         |
| -u, --usb      | Use USB Raspi camera                               | false   |
| -w, --width    | Image width                                        | 400     |
| -f, --focus    | Focus line % from bottom                           | 10      |
| -e, --percent  | Middle percent                                     | 15      |
| -m, --min      | Minimum target pixel area                          | 100     |
| -r, --range    | HSV Range                                          | 20      |
| -l, --leds     | Enable Blinkt led feedback                         | false   |
| -d, --display  | Display image                                      | false   |
| -p, --port     | gRPC server port                                   | 50051   |
| -v, --verbose  | Include debugging info                             | false   |
| -h, --help     | Summary of options                                 |         |

### Display Keystrokes

| Keystroke  | Action                                             |
|:----------:|----------------------------------------------------|
| k          | Move fous line up                                  |
| j          | Move focus line down                               |
| -          | Decrease focus line %                              |
| +          | Increase focus line %                              |
| w          | Decrease image size                                |
| W          | Increase image size                                |
| r          | Reset focus line % and image size                  |
| s          | Save current image to disk                         |
| q          | Quit                                               |

## Relevant Links

### Hardware
* [Raspberry Pi Camera](https://www.adafruit.com/products/3099)
* [Blinkt](http://www.athenian-robotics.org/blinkt/)

### Software
* [OpenCV](http://www.athenian-robotics.org/opencv/)
* [gRPC](http://www.athenian-robotics.org/grpc/)
* [Plot.ly](http://www.athenian-robotics.org/plotly/)

Instructions on how to display Raspi OpenCV camera images on a Mac are 
[here](http://www.athenian-robotics.org/opencv/)