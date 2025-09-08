
# Change Log

## [pr0.1.1] - 2025-09-08
 
### Added
 - Added various checks for server initialisation.

### Changed
 - Moved small code to small.py.
 - Moved permission logging and feedback into is_registered() in util.py rather then handling locally and added a variable to control not to log (allowing for local logging if needed). This significantly improves code readability.
 - Moved pk and logging control to util.py.
 
### Fixed
 - Spelling errors.
 - Code commenting in eevee_bot.py.

## [pr0.1.0] - 2025-09-08
 
### Added
- Initialise commands to initialise a guild.
- Reinitialise commands to reinitialise a guild and fully reset config.
- Registration commands to register a user or role as having bot permissions.
- Deregistration commands to deregister a user or role as having bot permission.
- Blacklist mode commands to control use of white or blacklist.
- Blacklist commands to add and remove role from blacklist.
- Whitelist commands to add and remove role from whitelist.
- Pk mode commands to control if bot should wait for pk before responding.
- Small commands to give user a set small role and remove it after timer including setting timer value.
- Role commands to add or remove roles from user.
- Basic help command for non-privileged users.
- Logging commands to set log channel for server.
- List role command.

### Changed
 
### Fixed