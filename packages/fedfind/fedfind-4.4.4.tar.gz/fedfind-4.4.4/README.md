# fedfind

Fedora Finder finds Fedoras. It provides a CLI and Python module that find and providing identifying information about Fedora images and release trees. Try it out:

    fedfind images --release 26
    fedfind images --release 27 --milestone Beta
    fedfind images --release 27 --milestone Beta --compose 1 --respin 1
    fedfind images --dist Fedora-Atomic --compose 20180116
    fedfind images --compose 20180118
    fedfind images --composeid Fedora-27-20171110.n.1
    fedfind images --release 27 --label Beta-1.1
    fedfind images --release 5 --arch x86_64,ppc
    fedfind images --release 15 --search desk

Fedora has stable releases, archive releases, really old archive releases, 'milestone' releases (Alpha / Beta), release validation 'candidate' composes, unstable nightly composes, and post-release nightly composes, all in different places, with several different layouts. There is no canonical database of the locations and contents of all the various composes/releases. We in Fedora QA found we had several tools that needed to know where to find various images from various different types of releases, and little bits of knowledge about the locations and layouts of various releases/composes had been added to different tools. fedfind was written to consolidate all this esoteric knowledge in a single codebase with a consistent interface.

fedfind lets you specify a release/compose using five values: 'dist', 'release', 'milestone', 'compose', and 'respin'. It can then find the location for that compose, tell you whether it exists, and give you the locations of all the images that are part of the release and what each image actually contains. As an alternative to this versioning concept, you can also find releases by their Pungi 4 / productmd 'compose ID' or 'compose label' (see examples above).

fedfind runs on Python versions 2.7 and later (including 3.x).

## Installation and use

fedfind is packaged in the official Fedora and EPEL repositories: to install on Fedora run `dnf install fedfind`, on RHEL / CentOS with EPEL enabled, run `yum install fedfind`. You may need to enable the *updates-testing* repository to get the latest version.

You can visit [the fedfind project page on Pagure][1], and clone with `git clone https://pagure.io/fedora-qa/fedfind.git`. Tarballs are released through [PyPI][2].

You can use the fedfind CLI from the tarball without installing it, as `./fedfind.py` from the root of the tarball (you will need `cached_property` and `six`). You can of course copy the Python module anywhere you like and use it in place. To install both CLI and module systemwide, run `python setup.py install`.

## Bugs, pull requests etc.

You can file issues and pull requests on [Pagure][1]. Pull requests must be signed off (use the `-s` git argument). By signing off your pull request you are agreeing to the [Developer's Certificate of Origin][3]:

    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the best
        of my knowledge, is covered under an appropriate open source
        license and I have the right under that license to submit that
        work with modifications, whether created in whole or in part
        by me, under the same open source license (unless I am
        permitted to submit under a different license), as indicated
        in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including all
        personal information I submit with it, including my sign-off) is
        maintained indefinitely and may be redistributed consistent with
        this project or the open source license(s) involved.

## Release identification

Some usage of fedfind relies on understanding the 'dist', 'release', 'milestone', 'compose', 'respin' versioning concept, so here is a quick primer. Note that if you intend to use fedfind solely with compose IDs or URLs for modern Pungi 4-generated composes, this section will be of less interest to you and you can probably skip it.

In this section we will write release, milestone, compose, dist quints as (release, milestone, compose, respin, dist) with '' indicating an omitted value, e.g. (22, Beta, TC3, '', 'Fedora') or (22, '', '', '', 'Fedora'). Note 'dist' is usually 'Fedora', and this is its default value, used when it is not explicitly specified. Conceptually, 'dist' should come at the front, but in fact fedfind functions which accept these values tend to place it after the others, for historical reasons (it did not exist when fedfind's versioning scheme was created).

* **Dist** is the term fedfind uses for what pungi and productmd refer to as the *shortname*; when fedfind was created this didn't really exist, but now the Fedora project produces many more composes than it used to, some with different *dists* / *shortnames*. In the compose with compose ID 'Fedora-Rawhide-20160301.n.0', the *dist* / *shortname* is *Fedora*; in a compose with compose ID 'Fedora-Modular-Rawhide-20170816.n.0', the dist / shortname is *Fedora-Modular*. *Fedora* is the **dist** for all mainline composes, and this is the default value. *Fedora-Atomic* is the **dist** for the nightly 'two week Atomic' composes, produced once a day for each of the current stable releases, which at present are found only in their initial location as output by release engineering, and not in their mirrored locations. Similarly, *Fedora-Docker* and *Fedora-Cloud* are the **dists** for the nightly Docker and Cloud composes for the current stable releases. So e.g. (27, '', 20180111, 0, 'Fedora-Atomic') will find the (first) 2018-01-11 nightly two-week Atomic compose for Fedora 27. *Fedora-Modular* was the **dist** for modular composes during the Fedora 27 cycle; at the time, Modularity was under development, and for technical reasons, required a separate stream of composes. *FedoraRespin* is the **dist** for the current post-release live respin compose in the `live-respins` directory; there is only ever one of these at a time (and note that these are only semi-official builds, provided by volunteers as a courtesy, they do not have the status of official composes). Any **release** or **compose** passed with the **dist** *FedoraRespin* is used as a *check*: if the existing contents of the `live-respins` directory don't match the expected release (number) or compose (date), fedfind will raise an exception instead of returning the `RespinRelease` instance.

* **Release** is usually a Fedora release number, e.g. 27, 15 or 1. The only non-integer value that is accepted is 'Rawhide', for Rawhide nightly composes. These do not, properly speaking, have a definite release number associated with them: Rawhide is a perpetually rolling tree. The canonical versioning for Rawhide nightly composes is (Rawhide, '', YYYYMMDD, N) (where N is the respin number). Note that [python-wikitcms][4] uses almost the same versioning concept as fedfind, but Wikitcms 'validation events' for Rawhide nightly composes **do** have a release number: this is a property of the *validation event*, not of the *compose*. Thus there may be a Wikitcms *validation event* (24, Rawhide, 20151012, 1, 'Fedora') for the fedfind *compose* (Rawhide, '', 20151012, 1). fedfind and python-wikitcms both recognize this case and will attempt to convert each other's values for convenience.

* **Milestone** indicates the milestone or the type of nightly compose. Valid milestones for current releases are *Beta*, *RC* (or *Final*, which means the same), *Branched*, and *Production*. The *Alpha* milestone existed until Fedora 25, but Fedora 26 and later releases have no Alpha; no Alpha releases can be found any more, as the Fedora 25 and earlier Alphas are now removed. fedfind will accept *Rawhide* as a milestone and convert it to the release - so ('', Rawhide, YYYYMMDD, N, 'Fedora') is not exactly *valid* but will be handled by the CLI and the `get_release` function and converted to (Rawhide, '', YYYYMMDD, N, 'Fedora'). Stable releases do not have a milestone; (23, RC, '', '', 'Fedora') will be accepted by `get_release` and the CLI but is treated internally as (23, '', '', '', 'Fedora'). The *Production* milestone indicates a so-called 'production' compose, which will usually also be an Alpha, Beta or Final 'candidate' compose - you may be able to find the same compose in two different places, for instance, with the *Production* milestone and a date-based **compose** and **respin**, or with the *Alpha*, *Beta* or *Final* milestone and a numeric **compose** and **respin**. It is approximately the same as the difference between searching for a production compose by compose ID and searching for it by compose label. See more on this in the *fedfind / Wikitcms vs. Pungi / productmd versioning* section below. Currently, the milestone value has no meaning for **dists** other than *Fedora* and *Fedora-Modular*; in future we may use it to distinguish between nightly and released two-week Atomic composes.

The values *Atomic*, *Docker*, *Cloud* and *Respin* are accepted for backwards compatibility purposes; they will be translated into a **dist** value of *Fedora-Atomic*, *Fedora-Docker*, *Fedora-Cloud* or *FedoraRespin* respectively, and a blank **milestone** value. Versions of fedfind before 4.0 overloaded the **milestone** concept to handle these **dist** values, rather than properly handling them as **dists**. This functionality may be removed in a future major release.

* **Compose** is the precise compose identifier (in cases where one is needed). For candidate composes it is always 1. For nightly composes it is a date in YYYYMMDD format. Stable releases and milestone releases do not have a compose.

* **Respin** is an integer that's bumped any time a compose which would otherwise have the same version is repeated. The concept is taken from Pungi. If we attempt to build two Rawhide nightly composes on 2016-03-01, for instance, in fedfind's versioning they are (Rawhide, '', 20160301, 0) and (Rawhide, '', 20160301, 1). The corresponding Pungi / productmd 'compose ID'-style versioning is Fedora-Rawhide-20160301.n.0 and Fedora-Rawhide-20160301.n.1.

Note that, as a convenience, fedfind will attempt to detect when a 'compose' value is in fact a combined compose and respin, and split it up - so you can specify the compose as `1.7` (for compose `1`, respin `7`) or `20160330.0` or `20160330.n.0` (both of which will be treated as compose `20160330`, respin `0`).

Some examples:

* Stable release: (23, '', '', '', 'Fedora')
* Alpha release: (24, Alpha, '', '', 'Fedora')
* Candidate: (24, Alpha, 1, 7, 'Fedora')
* Branched nightly: (24, Branched, 20160330, 0, 'Fedora')
* Branched modular nightly: (24, Branched, 20160330, 0, 'Fedora-Modular')
* Rawhide nightly: (Rawhide, '', 20160330, 1, 'Fedora')
* Rawhide modular nightly: (Rawhide, '', 20160330, 1, 'Fedora-Modular')
* Two-week Atomic nightly: (25, 20160330, 2, 'Fedora-Atomic')

The test suite contains a bunch of tests for `get_release()` which incidentally may function as further examples of accepted usage. The fedfind CLI and `get_release()` are designed to guess omitted values in many cases, primarily to aid unattended usage, so e.g. a script can simply specify ('', Branched, '', '', 'Fedora') to run on the date's latest branched compose, without having to know what the current Branched release number is. More detailed information on various cases can be found in the `get_release()` function's docstring.

### fedfind / Wikitcms vs. Pungi / productmd versioning

The fedfind / Wikitcms versioning system was developed prior to the use of Pungi 4 for Fedora composes. The 'respin' concept from Pungi / productmd was then stuffed into the fedfind / Wikitcms versioning concept quite hastily to keep stuff working, and the productmd 'short' concept was also added to fedfind (usually under the name 'dist', which more closely describes its function in Fedora's context).

For now, fedfind attempts to remain compatible with its legacy versioning approach as well as possible, while also supporting release identification using productmd versioning concepts. For instance, non-Pungi 4 composes have a sloppily-faked up *cid* attribute that at least will produce the correct release number when parsed like a 'compose ID', and `get_release()` can parse *most* (we aim for 'all', but we're also realists!) compose IDs, compose URLs and compose labels and return appropriate Release instances.

Pungi has several version-ish concepts. The two most important to fedfind are the 'compose ID' and 'label'. All Pungi composes have a 'compose ID'. Not all have a label - only 'production' composes do (not 'nightly' or 'test' composes).

A compose ID looks like `Fedora-24-20160301.n.0` (nightly), or `Fedora-Rawhide-20160302.t.1` (test), or `Fedora-24-20160303.0` (production). The release number, date and type of compose are always indicated somehow. For Fedora purposes the respin value should always be present. There is no kind of 'milestone' indicator.

A label looks like `Alpha-1.2`, or `Beta-13.16`. There's a list of supported milestones (including Fedora's Alpha and Beta, but not Final - productmd uses RC instead). The first number is a public release number (RHEL has numbered milestone releases, unlike Fedora); the second is the respin value, which is considered more of a private/internal property. The system around which the scheme was designed appears to be that multiple "Alpha 1" respins are produced and tested and the final one is released as the public "Alpha 1" - thus the 'respin' concept covers approximately the same ground as Fedora's "TC" and "RC" composes used to.

Mainline Fedora nightly composes are built just as you'd expect: the short name is 'Fedora', the release number is 'Rawhide' or the actual release number, the type is nightly, and the respin value is incremented if multiple composes are run on the same date (usually only if the first fails and we want to fix it before the next day). So Fedora nightly compose IDs look like `Fedora-Rawhide-20180119.n.0`, for instance.

For milestone releases, Fedora builds 'production' composes with the label `release` number always set as 1, and the `respin` number incremented each time a compose is run. Thus for Fedora 24 Alpha validation testing we built `Alpha-1.1`, `Alpha-1.2`, `Alpha-1.3` and so on, until `Alpha-1.7` was ultimately released as the public Alpha release. Each of these composes also had a compose ID in `Fedora-24-20160323.0` format.

The post-release nightly composes for Atomic, Cloud and Docker images are built almost as you'd expect, but with their type as 'production', not 'nightly'. So their compose IDs look like `Fedora-Atomic-27-20180119.0` or `Fedora-Docker-26-20171215.1`. Their labels are always `RC-(date).(respin)`, e.g. `RC-20180119.0`.

Current fedfind should be capable in almost all cases of finding any findable Fedora compose by its compose ID or its label. The Fedora 'production' composes initially land in one location (on *kojipkgs*, alongside the nightly Branched and Rawhide composes, in directory names based on the compose ID) and are then mirrored to another location (on *alt*, in directory names based on the compose label). When you search for a given production / candidate compose whether you find its *kojipkgs* location or its *alt* location depends to some extent on how you search for it. Searching by compose label, or with something like *milestone* Alpha, *compose* 1, *respin* 7, will usually find its *alt* location (as a `Compose` class instance). Searching by compose ID, or with something like *milestone* Production, *compose* 20160323, *respin* 0, will usually find its *kojipkgs* location (as a `Production` class instance). However, you can set the `get_fedora_release` argument `promote` to `True` when searching by compose ID-ish values, and fedfind will attempt to find the `Compose` class (*alt* location) if it can. All fedfind release instances for Pungi 4 composes that actually exist should have the compose's compose ID as their `cid` attribute. If the compose has a label, it should be available as the `label` attribute.

## CLI

The `fedfind` CLI command gives you URLs for a release's images. For instance, `fedfind images -r 25` will print the URLs to all Fedora 25 images. You can filter the results in various ways. For more information, use `fedfind -h` and `fedfind images -h`.

## Python module

The Python module provides access to all fedfind's capabilities.

### Example usage

    import fedfind.release
    
    comp = fedfind.release.get_release(release=27)
    print comp.location
    for img in comp.all_images:
        print(img['url'])

### Module design and API

The main part of fedfind is the `Release` class, in `fedfind.release`. The primary entry point is `fedfind.release.get_release()` - in almost all cases you would start by getting a release using that function, which takes the `release`, `milestone`, `compose`, `respin`, and `dist` values that identify a release as its arguments and returns an instance of a `Release` subclass. You may also pass `url` (which is expected to be the `/compose` directory of a Pungi 4 compose, or as a special case, `https://dl.fedoraproject.org/pub/alt/live-respins/` for the semi-official post-release live respins which live there), `cid` (a Pungi 4 compose ID), or `label` (a Pungi 4 compose label) as an alternative to release/milestone/compose/respin. If you pass a `url` or `cid`, fedfind will run a cross-check to ensure the URL or CID of the discovered compose actually matches what you requested, and raise an exception if it does not.

Anyone who used fedfind 1.x may remember the `Image` class for describing images and the `Query` class for doing searches. Both of those were removed from fedfind 2.x in favour of productmd-style metadata. All `Release` instances have a `metadata` dict which, if the release exists, will contain an `images` item which is itself a dict containing image metadata in the format of the productmd `images.json` file. For Pungi 4 releases this is read straight in from `images.json`; for pre-Pungi 4 releases fedfind synthesizes metadata in approximately the same format.

You can also use the `all_images` convenience property; this is basically a flattened form of the images metadata. It's a list of image dicts, with each image dict in the same basic form as a productmd image dict, but with a `variant` entry added to indicate its variant (in the original productmd layout, the image dicts are grouped by variant and then by arch, which is kind of a pain to parse for many use cases). Note that since fedfind 3.1.0, from Fedora 9 onwards, `boot.iso` files are not included in `all_images`(or the lower-level `all_paths`).

Since fedfind 3.3.0, image dicts also have `url` and `direct_url` entries added which provide full HTTPS URLs for the image files (so fedfind consumers no longer have to worry about constructing URLs by combining the release `location` or `alt_location` and the image `path`). `url` may go through the https://download.fedoraproject.org mirror redirector, which tries to spread load between mirrors. `direct_url` will always be a direct link. If the image is in the public mirror system, it will use the https://dl.fedoraproject.org mirror. Please use `url` unless you have a strong reason to use `direct_url`, to avoid excessive load on the server.

You're expected to roll your own queries as appropriate for your use case. The reason fedfind 1.x had a dedicated query interface was primarily to try and speed things up for nightly composes by avoiding Koji queries where possible and tailoring them where not; since fedfind no longer ever has to perform slow Koji queries to find images, the need for the `Query` class is no longer there, you can always just operate on the data in `metadata['images']` or `all_images`. Note the image `subvariant` property is extremely useful for identifying images; you may also want to use the `identify_image` function from `productmd` for this purpose.

All methods and functions in fedfind are documented directly: please do refer to the docstrings for information on their purposes. Attributes are documented with comments wherever their purpose is not immediately obvious.

All methods, functions, attributes and properties not prefixed with a `_` are considered 'public'. Public method and function signatures and all public data types will only change in major releases. fedfind has no control over the form or content of the productmd metadata, so when and how that changes is out of our hands; I will make a best effort to keep the synthesized metadata for old composes broadly in line with whatever current Pungi produces, though it is not perfect now and likely never will be (it's kinda tailored to the information I actually need from it).

#### Useful things fedfind can do

fedfind can do some useful stuff that isn't just querying images for releases:

* `Release.check_expected()` sees if all 'expected' images for the release are present.
* `Release.previous_release()` takes a cut at figuring out what the 'previous' release was, though this is difficult and may not always work or return what you expect.
* `helpers.get_current_release()` tells you what the current Fedora release is.

## How it works (roughly)

fedfind has a bunch of knowledge about where Fedora keeps various composes wired in. For Pungi 4 compose types, finding the compose is about all fedfind has to do; it reads all the information about what images are in the compose out from the metadata and exposes it.

For non-Pungi 4 composes (old stable releases) and Pungi 4 composes that are modified and have their metadata stripped (current stable and milestone releases), fedfind uses the `imagelist` files present on dl.fedoraproject.org, which contain lists of every image file in the entire tree. It finds the images for the specific compose being queried, then produces a path relative to the top of the mirror tree from the result. It can then combine that with a known prefix to produce an HTTPS URL.

For metadata, fedfind first tries to see if the compose was originally produced with Pungi 4 and its metadata is available from PDC. It tries to guess the compose label from the image file names, and then a compose ID from the compose label, and then query PDC for metadata for that compose. If it is successful, it tries to match each image discovered from the `imagelist` file with an image dict from the original metadata, and combine the two so that the path information is correct but all other information for the image is taken from the original metadata, rather than synthesized by fedfind.

For any discovered image no matching original image dict is found for, and for composes where no original metadata is available at all, fedfind synthesizes productmd-style metadata by analyzing the file path, guessing the properties that can be guessed and omitting others.

In all cases, the result is that metadata and derived properties like `all_images` are as similar as possible for the different types of compose, so fedfind consumers can interact with non-Pungi 4 composes in the same way as Pungi 4 ones (to the extent of the metadata discovery and synthesis implementations, some stuff just isn't covered by the synthesis).

## Caveats

### Speed and resource use

With the use of small metadata files (for metadata composes) and still-quite-small image list files that are cached locally (for non-metadata composes), fedfind is much faster than it used to be. It can still take a few seconds to do all its parsing and analysis, though.

When used as a module it caches properties and image lists for the lifetime of the release instance. The image list files are cached (in `~/.cache/fedfind`) based on the 'last modified time' provided by the server they come from: for each new release instance, fedfind will hit the server to retrieve the last modified time header, but if the cached copy matches that time, it will not re-download the file. These files are also quite small so will not take long to download in any case. If the download fails for some reason, but we do have a cached copy of the necessary lists, fedfind will work but log a warning that it's using cached data which may be outdated.

Certain PDC queries, whose results are never expected to change, are also cached (again in `~/.cache/fedfind`), to speed up repeated searches and reduce load on PDC.

If `~/.cache/fedfind` is not writeable for the user running fedfind, we fall back to using a temporary cache location that is only valid for the life of the process (and deleted on exit). This at least ensures fedfind will work in this case, but results in it being slower and doing more round trips.

It shouldn't use too much bandwidth (though I haven't really measured), but obviously the server admins won't be happy with me if the servers get inundated with fedfind requests, so don't go *completely* crazy with it - if you want to do something script-y, please at least use the module and re-use release instances so the queries get cached.

### Can't find what ain't there

All releases other than stable releases disappear. fedfind can find stable releases all the way back to Fedora Core 1, but it is not going to find Fedora 14 Alpha, Fedora 19 Beta TC3, or nightlies from more than 2-3 weeks ago. This isn't a bug in fedfind - those images literally are not publicly available any more. Nightlies only stick around for a few weeks, candidate composes for a given milestone usually disappear once we've moved on another couple of milestones, and pre-releases (Alphas and Betas) usually disappear some time after the release in question goes stable. fedfind will only find what's actually there.

Also note that fedfind is not designed to find even *notional* locations for old non-stable releases. Due to their ephemeral nature, the patterns it uses for nightly builds and candidate composes only reflect current practice, and will simply be updated any time that practice changes. It doesn't have a big store of knowledge of what exact naming conventions we used for old composes. If you do `comp = fedfind.release.Compose(12, 'Final', 'TC4')` and read out `comp.location` or something what you get is almost certainly *not* the location where Fedora 12 Final TC4 actually lived when it was around.

### No secondary arches

fedfind does not, for the present, handle secondary arches at all. It *will* find PPC images for releases where PPC was a primary arch and i686 images for releases where i686 was a primary arch, though.

## Credits

This is pretty much all my fault. Note that aside from its external deps, older versions of fedfind (up to 1.1.2) included a copy of the `cached_property` implementation maintained [here][5] by Daniel Greenfield. The bundled copy was dropped with version 1.1.3.

## Licensing

Fedora Finder is available under the GPL, version 3 or any later version. A copy is included as COPYING.

[1]: https://pagure.io/fedora-qa/fedfind
[2]: https://pypi.python.org/pypi/fedfind
[3]: https://developercertificate.org/
[4]: https://pagure.io/fedora-qa/python-wikitcms
[5]: https://github.com/pydanny
