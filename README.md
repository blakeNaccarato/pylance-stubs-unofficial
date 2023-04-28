# pylance-stubs-unofficial

The Pylance extension for VSCode uses `pyright` for type checking, but its type checking results don't always match a vanilla `pyright` installation, such as the kind you might have in your CI. Differences arise from the additional type stubs used by Pylance locally, found in `~/.vscode/extensions/ms-python.vscode-pylance-<RELEASE>/dist` (where `<RELEASE>` is the version of Pylance you have installed).

Most of these differences can be resolved by keeping the contents of the `.../dist/bundled/stubs` directory in a `typings` folder in your project, which is where `pyright` looks for additional type stubs by default. This makes Pylance and vanilla `pyright` _mostly_ agree with one another, see [more detail](#more-detail) some discrepancies remain.

## Use these stubs

The following process will mostly align the behaviors of `pyright` running in CI with a local Pylance install by providing similar type stubs to your CI in the form of a submodule.

Please note that these stubs, mirrored from Pylance, inherently lag the latest stubs from upstream sources by a week or more. If you encounter a bug related to any type stubs, consider manually pulling the latest stubs from the related upstream source and checking again before opening an issue. In the case of [pandas-dev/pandas-stubs](https://github.com/pandas-dev/pandas-stubs), it is recommended that you `pip install pandas-stubs~=#.#.#` where `#.#.#` corresponds to your project's Pandas version.

### Add the submodule for the first time in a project

Add this repository as a submodule to the `typings` folder where `pyright` expects it to be.

```Shell
git submodule add https://github.com/blakeNaccarato/pylance-stubs-unofficial.git typings
```

Whichever local repo you run this on will get `pylance-stubs-unofficial` as a submodule in the `typings` directory, and record `HEAD` of `main` as the current commit.

### Check out the submodule in other local clones

Other clones of the remote will not populate their submodules by default. If you want `typings` in your local clones, you'll need to initialize and update your submdodule(s).

```Shell
git submodule update --init typings
```

This will initialize submodules and update them to the _the commit currently being tracked by your project_.

### Update submodule to track the latest commit

You will need to periodically bump your `typings` submodule whenever Pylance releases come out, assuming that I have updated this `pylance-stubs-unofficial` repo to contain the latest stubs.

```Shell
git submodule update --init --remote --merge typings
```

The `--remote` flag ensures your submodule is updated to track what is presently the `HEAD` of `main` in `pylance-stubs-unofficial`.

### Clear the submodule directory in local clones

Note that because the Pylance extension already uses its bundled stubs, it's not typically necessary to keep `typings` checked out in local clones. If you want to, you can throw away your local copy of `typings`.

```Shell
git submodule deinit typings
```

This will reduce clutter in the Source Control pane of your VSCode UI (after restarting VSCode), by not showing the `typings` repo there in addition to your main project repo.

## Use these stubs in CI

Your GitHub Actions workflow will need to have `submodules: true` or a similar configuration in order to pull the type stubs into the `typings` submodule. You can then proceed to install and run `pyright`, either via NodeJS, `nodeenv`, or the [pyright-action](https://github.com/jakebailey/pyright-action).

```YAML
...
jobs:
...
  pyright:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true
      ...
      - run: pyright
...
```

## How I update these stubs

I update these stubs from the Pylance stubs on my local machine, since I have VSCode installed and Pylance installed locally. The stubs are at `~/.vscode/extensions/ms-python.vscode-pylance<VERSION>/dist/bundled/stubs`, where `<VERSION>` corresponds to the Pylance extension version I have installed. The [script](https://github.com/blakeNaccarato/pylance-stubs-unofficial/blob/main/update.ps1) grabs these stubs and pushes them to this repo under a tag matching the `<VERSION>`, then I manually publish a release in the GitHub UI.

I try to update these stubs weekly. Eventually, I will automate this process in GitHub action so that I don't have to manually push changes. In case this repo falls behind and you need updated stubs, you can use `update.ps1` (in PowerShell) to locally bump your stubs, sourced from your very own Pylance installation. A similar thing could be accomplished in a `bash` script, which I may add if I get around to it. If you'd like to contribute these changes back upstream, feel free to submit a Pull Request (no need to open an Issue ahead of time).

```Shell
cd typings
./update.ps1
```

## More detail

There are still some stubs in `.../dist` besides the ones kept here, and it's not clear the exact fashion in which they are composed by Pylance. So there will still be a few differences that you will need to troubleshoot. This effort reduces dozens of discrepancies to just one or two in one of my repos, using the data science stack and consisting of ~10k lines. I can get CI to go green by putting `# type: ignore` on those few remaining issues as they pop up.

There is still the occasional line that fails just locally or on CI, or the other way around. Also since I use the `reportUnneccessaryTypeIgnore` check, sometimes a local (necessary!) ignore gets flagged as unnecessary in CI. My solution to that is to disable the `reportUnneccessaryTypeIgnore` check in the entire file where those weird discrepancies pop up (since you can't disable the check line-by-line).

I suspect that the remaining discrepancies lie in the particular details of stub resolution order by Pylance, regarding the other stubs in `~\.vscode\extensions\ms-python.vscode-pylance-<RELEASE>\dist\`. I only keep the `bundled/stubs` bit updated, because it's not clear how the other stub folders in `dist` are merged/layered. Pyright only has one "layer" of stub finding by default, so Pylance must be doing some magic behind the scenes to compose all the stubs.

I could get my stubs from the upstream source, as the Pylance team gets their stubs from <https://github.com/microsoft/python-type-stubs>. But there is no telling which commit over at <https://github.com/microsoft/python-type-stubs> corresponds to what is bundled in a given Pylance version, and they curate it in a certain way, so I just scrape Pylance's stubs from my local machine whenever it updates.
