function Update-PylanceStubs {
    <#.SYNOPSIS
    Update stubs in pylance-stubs-unofficial with the latest from Pylance.
    #>
    $__ = @{
        Path   = '~/.vscode/extensions'
        Filter = 'ms-python.vscode-pylance*'
    }
    $latest_pylance = (Get-ChildItem @__)[-1]
    $version = (($latest_pylance | Split-Path -Leaf) -Split '-')[-1]
    $source = "$latest_pylance/dist/bundled/stubs"
    $destination = '~/Code/mine/pylance-stubs-unofficial'
    Get-ChildItem $destination -Exclude README.md, update.ps1 | Remove-Item -Recurse
    Get-ChildItem $source | Copy-Item -Recurse -Destination $destination
    git add -A
    git commit -m $version
    git tag $version
    git push
    git push --tags
}

Update-PylanceStubs
