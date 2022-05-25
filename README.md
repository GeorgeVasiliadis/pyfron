# pyfron
An OpenDR-based face recognition CLI app

## Why pyfron
Because it has a cool name that combines the terms **Python** and **Face Recognition** into an anagram. Also, because 
pyfron provides an easy-to-use methodology for:

- Creating OpenDR face recognizers
- Manipulating several image databases with environments
- Reporting the overall performance of recognizers in beautiful markdowns

## Installation
1. Manually [install OpenDR](https://github.com/opendr-eu/opendr#installing-opendr-toolkit)
2. Run `pip install pyfron`

## Usage

You can invoke pyfron by running either `pyfron [options]` or `python -m pyfron [options]`. Although the first way is 
more elegant, the latter one is considered to be more stable. For more information about options, run `pyfron --help`.

## Directory Structures

In order to facilitate the process of image discovery and ease the confusion that comes with directory schemas, pyfron 
introduces two basic concepts, the ImageDir and the ImageBase.

### ImageDir

An ImageDir is a directory that contains only images of supported type (currently only IMAGE/JPEG). Semantically, 
an ImageDir should only contain pictures of the same person. A valid ImageDir would look like this:
 ```
i_am_an_image_dir/
|--- image1.jpg
|--- image2.jpg
|--- arbitrary_name.jpg
|--- ...
|--- imageN.jpg
```

### ImageBase
An ImageBase is simply a directory that stores many ImageDirs. Semantically, those ImageDirs are ment to represent one 
person each. One valid example of an ImageBase is LFW itself. Generally, an ImageBase should look like this:

 ```
i_am_an_image_base/
|--- and_i_am_an_image_dir/
|    |--- 1.jpg
|    |--- ...
|    |--- N.jpg
|--- image_dir_2/
|--- ...
|--- last_image_dir/
```

## Quick Start

### Set up your workspace

Say that you have downloaded the LFW dataset from the [official but slow site](http://vis-www.cs.umass.edu/lfw/) or 
from this [faster mirror](https://drive.google.com/file/d/1JIgAXYqXrH-RbUvcsB3B6LXctLU9ijBA/view). Also, in your 
Desktop directory, you have gathered three "stalking" subdirectories. Each one of them includes images of a 
different celebrity. Finally, you have your own directory under Pictures, which contains photos of you. To sum up, 
your workstation consists of something like this:

1. `~/Downloads/lfw/`
    - `~/Downloads/lfw/Aaron_Eckhart/`
    - `~/Downloads/lfw/Aaron_Guiel/`
    - `...`
    - `~/Downloads/lfw/Zydrunas_Ilgauskas/`
2. `~/Desktop/Stalking/`
    - `~/Desktop/Stalking/Bradley Cooper/`
    - `~/Desktop/Stalking/Jennifer Lawrence/`
    - `~/Desktop/Stalking/Jim Carrey/`
3. `~/Pictures/Me/`

### Experiment 1

Now, say that you want to ensure that your personal data haven't been leaked. Let's start by checking if your face can 
be identified in the LFW database.

The reference ImageBase should contain the whole LFW ImageBase. You can create a new environment and append the desired 
images to its reference ImageBase.

> The **reference ImageBase** refers to the pictures that will be known to a recognizer after it has been trained.
> On the other hand, the **test ImageBase** refers to the pictures that are going to be used as input to the trained 
> recognizer.

You can achieve this by running:

```commandline
$ pyfron --env am_i_in_lfw populate-reference --from-dir ~/Downloads/lfw
```

This should copy the LFW images in a special location in the new environment. Then, you may configure the test 
ImageBase. In this scenario, test ImageBase should just contain pictures of yourself.

```commandline
$ pyfron --env am_i_in_lfw populate-test --from-dir ~/Pictures/Me
```

> Note that, although the source of reference ImageBase is a valid *ImageBase* (because it contains many ImageDirs), the 
> source of test ImageBase is in fact an *ImageDir*. However, pyfron is smart enough to understand your intentions, and 
> it will automatically handle the given path as expected.

With the new environment ready-to-go, you may now test your input images and report the results.

*Since LFW consists of 5749 ImageDirs, this step is expected to, practically, take forever. Removing manually a 
considerably large amount of ImageDirs from reference ImageBase is quite a reasonable move. For example, in this 
scenario only 300 ImageDirs from LFW were kept and used.*

You may run:

```commandline
$ pyfron --env am_i_in_lfw run
```

This command loads every image found in test ImageBase and compares it against reference ImageBase. The generated 
markdown summarizes the images that have the maximum confidence of similarity in decreasing order.  Thus, just by 
examining the markdown report, you may see that luckily there are no images of yourself in this database.

### Experiment 2

Now, say that you want to see how similar to LFW faces each of your favorite celebrities is.

You could create a new environment and train a new model, but since the reference ImageBase will be the same, there is 
no need to do so. Instead, you can simply append the celebrities' images in the test ImageBase:

```commandline
$ pyfron --env am_i_in_lfw populate-test --from-dir ~/Desktop/Stalking
```

Then, run the testing procedure by executing:

```commandline
$ pyfron --env am_i_in_lfw run
```

### Experiment 3

What if you wanted to run the previous experiment with a different recognizer configuration? This can actually be done 
pretty effortlessly.

Begin by querying pyfron which models are already known to it:

```commandline
$ pyfron --list-models
```

This will display a json-like representation of registered models, along with the file that can be edited to register 
your custom models. You can then choose the desired one by specifying the `--model` option. This would look like:

```commandline
$ pyfron --env am_i_in_lfw populate-test --from-dir ~/Desktop/Stalking --model ir_50
```

Here, the model `ir_50` is a built-in model, and you can use it as is. Although batteries **are** included, you are 
encouraged to explore how you can create your custom models in OpenDR 's [docs](https://github.com/opendr-eu/opendr/blob/master/docs/reference/face-recognition.md#facerecognitionlearner-constructor).

## Future Features - Help needed :D
- [ ] More control over environments (delete, clone, reuse models, utilize symlinks for shared files)
- [ ] Refined CLI options. The `argparse` module is used too naively
- [ ] Random selection/ exception options for populate commands (e.g. `--keep-max N` to keep the first `N` objects 
while populating)
- [ ] Support for creating and training full models (backbone + head)
