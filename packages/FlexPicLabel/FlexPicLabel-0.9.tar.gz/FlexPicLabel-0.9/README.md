Compound widget to work around some shortcomings in Qt image display.

    - Animated GIFs will animate, like in a browser, by transparently switching
      between QImage and QMovie internally depending on the number of frames
      detected by QImageReader.
    - Content will scale up or down to fit the widget while preserving its
      aspect ratio and will do so without imposing a minimum size of 100%.
    - Letterbox/pillarbox borders will default to black.
      (It's a bit of a toss-up whether an application will want this or the
       default window background colour, so this defaults to the choice that
       provides an example of how to accomplish it.)

    Note that QImageReader doesn't have an equivalent to GdkPixbufLoader's
    `area-prepared` and `area-updated` signals, so incremental display for
    for high-speed scanning (ie. hitting "next" based on a partially loaded
    images) isn't really possible. The closest one can get is to experiment
    with QImageReader's support for loading just part of a JPEG file to see if
    it can be done without significantly adding to the whole-image load time.
    (https://wiki.qt.io/Loading_Large_Images)