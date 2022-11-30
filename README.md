# pylance-stubs-unofficial

The Pylance extension for VSCode uses `pyright` for type checking, but its type checking results don't always match a vanilla `pyright` installation, such as the kind you might have in your CI. Differences arise from the additional type stubs used by Pylance locally, found in `~/.vscode/extensions/ms-python.vscode-pylance-<RELEASE>/dist` (where `<RELEASE>` is the version of Pylance you have installed).

Most of these differences can be resolved by keeping the contents of the `.../dist/bundled/stubs` directory in a `typings` folder in your project, which is where `pyright` looks for additional type stubs by default. This makes Pylance and vanilla `pyright` *mostly* agree with one another. However, there are still some stubs in `.../dist` besides the ones kept here, and it's not clear the exact fashion in which they are composed by Pylance. So there will still be a few differences that you will need to troubleshoot.

## Using

Add this repository as a submodule to the `typings` folder where `pyright` expects it to be.

```Shell
git submodule add https://github.com/blakeNaccarato/pylance-stubs-unofficial.git typings
```

When Pylance updates, new differences may arise between local/CI type checking due to outdated stubs. If this repo has been updated to the latest stubs, pull its changes in.

```Shell
git submodule update --init --remote --merge
```

## Using in CI

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

## Updating stubs yourself, in a pinch

I try to update these stubs weekly. Eventually, I will automate this process in GitHub action so that I don't have to manually push changes. In case this repo falls behind and you need updated stubs, you can use `update.ps1` (in PowerShell) to locally bump your stubs, sourced from your very own Pylance installation. A similar thing could be accomplished in a `bash` script, which I may add if I get around to it. If you'd like to contribute these changes back upstream, feel free to submit a Pull Request (no need to open an Issue ahead of time).

```Shell
cd typings
./update.ps1
```

## More detail

This effort reduces dozens of discrepancies to just one or two in one of my repos, using the data science stack and consisting of ~10k lines. I can get CI to go green by putting `# type: ignore` on those few remaining issues as they pop up.

There is still the occasional line that fails just locally or on CI, or the other way around. Also since I use the `reportUnneccessaryTypeIgnore` check, sometimes a local (necessary!) ignore gets flagged as unnecessary in CI. My solution to that is to disable the `reportUnneccessaryTypeIgnore` check in the entire file where those weird discrepancies pop up (since you can't disable the check line-by-line).

I suspect that the remaining discrepancies lie in the particular details of stub resolution order by Pylance, regarding the other stubs in `~\.vscode\extensions\ms-python.vscode-pylance-<RELEASE>\dist\`. I only keep the `bundled/stubs` bit updated, because it's not clear how the other stub folders in `dist` are merged/layered. Pyright only has one "layer" of stub finding by default, so Pylance must be doing some magic behind the scenes to compose all the stubs.
