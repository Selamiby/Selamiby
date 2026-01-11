@{
    # Use Severity when you want to limit messages from a scaling in terms of severity
    Severity     = 'Error'

    # Use IncludeRules when you want to run only a subset of rules
    # IncludeRules = @('PSAvoidDefaultValueSwitchParameter', 'PSMissingModuleManifestField', 'PSReservedCmdletChar', 'PSReservedParams')

    # Use ExcludeRules when you want to run all rules except for a few
    ExcludeRules = @(
        'PSUseDeclaredVars',
        'PSAvoidUsingPlainTextForPassword',
        'PSAvoidUsingComputerNameHardcoded'
    )
}
