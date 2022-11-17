function Update-PylanceStubs {
    <#.SYNOPSIS
    Update stubs in pylance-stubs-unofficial with the latest from Pylance.
    #>

    # Remove existing stubs
    Get-ChildItem -Exclude ('README.md', 'update.ps1') | Remove-Item -Recurse

    # Get the latest release
    $__ = @{
        Path   = '~/.vscode/extensions'
        Filter = 'ms-python.vscode-pylance*'
    }
    $latest_pylance = (Get-ChildItem @__)[-1]

    # Copy the stubs
    $source = "$latest_pylance/dist/bundled/stubs"
    Get-ChildItem $source | Copy-Item -Recurse -Destination $destination

    # Commit, tag, and push
    $version = (($latest_pylance | Split-Path -Leaf) -Split '-')[-1]
    git add -A
    git commit -m $version
    git tag $version
    git push
    git push --tags
}

Update-PylanceStubs
