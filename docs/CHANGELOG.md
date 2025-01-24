# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [V1.1.0]

### Added

- Added dynamic page meta titles
- auto_archive receiver added to jobs signals.py, to auto archive jobs on user login, based on user settings.

### Changed

- Changed board cards detail to provide more info
- Put jobs app onto single nav-link in base authenticated navigation
- Separated interviews into separate app

### Fixed

- Fixed edit job button on list view
- Fixed add job button on list view, to point to correct modal

## [V1.0.3]

### Added

- Added script to export default data
- Added script to import default data

### Changed

- Moved JobFunction model to core app
- Moved LocationPolicy model to core app
- Moved WorkContract model to core app
- Moved PayRate model to core app

### Fixed

- Jobs list filter modal Job Functions selection
- Jobs list filter modal Countries selection

## [V1.0.2]

### Added

- Service scripts to ease deployment
- Target app to separate functionality from accounts
- Tasks app to separate functionality

### Changed

- Moved target and streak functionality in Target app
- Moved tasks models into tasks app

## [V1.0.1]

### Added

- Input options on deploy.yml

### Changed

- Made unauthenticated.html navbar responsive
- Made index.html hero text responsive
- Made index.html hero banner height responsive

## [V1.0.0]

### Added

- tasks_cards page
- calendar page
- dashboard page
- Task models
- Interview Models
- Target model
- Add interview modal
- Update interview modal
- Alerts modal
- Tasks modal

### Changed

- Layout of add-job modal
- Layout of update-job modal
- Layout of delete-job modal

### Removed

- Unnecessary locations model and forms
