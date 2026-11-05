# Dataset attribution

Five real photographs from scikit-image 0.25.2, redistributed under their individual public-domain/CC0 terms, not the repository MIT license. Attribution and source links are in manifest.json. Sources were resized once; no resizing occurs during trials. Four tuning images and one fresh holdout are a small demonstration corpus, not evidence about all website images.

## astronaut

Color image of the astronaut Eileen Collins.

    Photograph of Eileen Collins, an American astronaut. She was selected
    as an astronaut in 1992 and first piloted the space shuttle STS-63 in
    1995. She retired in 2006 after spending a total of 38 days, 8 hours
    and 10 minutes in outer space.

    This image was downloaded from the NASA Great Images database
    <https://flic.kr/p/r9qvLn>`__.

    No known copyright restrictions, released into the public domain.

    Returns
    -------
    astronaut : (512, 512, 3) uint8 ndarray
        Astronaut image.
    

## coffee

Coffee cup.

    This photograph is courtesy of Pikolo Espresso Bar.
    It contains several elliptical shapes as well as varying texture (smooth
    porcelain to coarse wood grain).

    Notes
    -----
    No copyright restrictions.  CC0 by the photographer (Rachel Michetti).

    Returns
    -------
    coffee : (400, 600, 3) uint8 ndarray
        Coffee image.
    

## chelsea

Chelsea the cat.

    An example with texture, prominent edges in horizontal and diagonal
    directions, as well as features of differing scales.

    Notes
    -----
    No copyright restrictions.  CC0 by the photographer (Stefan van der Walt).

    Returns
    -------
    chelsea : (300, 451, 3) uint8 ndarray
        Chelsea image.
    

## rocket

Launch photo of DSCOVR on Falcon 9 by SpaceX.

    This is the launch photo of Falcon 9 carrying DSCOVR lifted off from
    SpaceX's Launch Complex 40 at Cape Canaveral Air Force Station, FL.

    Notes
    -----
    This image was downloaded from
    `SpaceX Photos
    <https://www.flickr.com/photos/spacexphotos/16511594820/in/photostream/>`__.

    The image was captured by SpaceX and `released in the public domain
    <http://arstechnica.com/tech-policy/2015/03/elon-musk-puts-spacex-photos-into-the-public-domain/>`_.

    Returns
    -------
    rocket : (427, 640, 3) uint8 ndarray
        Rocket image.
    

## camera

Gray-level "camera" image.

    Can be used for segmentation and denoising examples.

    Returns
    -------
    camera : (512, 512) uint8 ndarray
        Camera image.

    Notes
    -----
    No copyright restrictions. CC0 by the photographer (Lav Varshney).

    .. versionchanged:: 0.18
        This image was replaced due to copyright restrictions. For more
        information, please see [1]_.

    References
    ----------
    .. [1] https://github.com/scikit-image/scikit-image/issues/3927
    