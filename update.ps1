function Update-PylanceStubs {
    <#.SYNOPSIS
    Update stubs in pylance-stubs-unofficial with the latest from Pylance.
    #>
    $__ = @{
        Path   = '~/.vscode/extensions'
        Filter = 'ms-python.vscode-pylance*'
    }
    $source = "$((Get-ChildItem @__)[-1])/dist/bundled/stubs"
    $destination = '~/Code/mine/pylance-stubs-unofficial'
    Get-ChildItem $destination -Exclude README.md,update.ps1 | Remove-Item -Recurse
    Get-ChildItem $source | Copy-Item -Recurse -Destination $destination
}

Update-PylanceStubs
