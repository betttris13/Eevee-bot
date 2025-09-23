
# Change Log

## [pr0.2.0] - 2025-09-23
 
### Added
 - Added "/Eevee bot" command that returns version and basic help info.
 - Added "/role remove - all" command to remove all available roles.
 - Added "/role current" command to list all roles a user has.
 - Added help msg on join.
 - Added update message when bot first starts in a new version on a server.
 - Added /emoji get command that sends custom emojis in message responded to, to user.
 - Added /emoji help command.

### Changed
 - Changed commands to not be case sensitive.
 - Changed logging to output all roles in one message.
 - Moved /role command logic into commands.py
 - Changed is_registered() to return None of server not initialised.
 - Changed /role help command to be dynamically generated.
 - Changed bot info msg to include emoji help.

### Fixed
 - Fixed small role embed text.
 - Help command gen
 - Fixed /role help logging and responding permission denied when checking permissions.


## [pr0.1.3] - 2025-09-12
 
### Added
 - Added error logging.
 - Added version variable in util.py.

### Changed
 - Improved error handling logic.
 - Changed message formatting to use embeds when appropriate.

### Fixed
 - Fixed parsing of roles containing commas. "" can now be used around role to ignore commas.
 - Removed unused imports.


## [pr0.1.2] - 2025-09-09
 
### Added
 - Added basic error logging.

### Changed
 - Moved bot directory and logging file to .env file.

### Fixed
- Removed unused imports.
- Code commenting in initialisation.py.
- Code commenting in help.py.
- Code commenting in initialisation.py.
- Code commenting in registration.py.
- Code commenting in roles.py.
- Code commenting in small.py.
- Code commenting in util.py.


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