# TODO List

## High Priority
- [ ] Increase unit test coverage (ongoing)
- [ ] Allow naming of channels not being used for grid and EVSE power selection
- [ ] Fix reporting of values to the database when only primary Shelly is used
- [ ] Test functionality that models the EVSE power when not being monitored
- [ ] Fix double running of EvseController's update function per second

## Medium Priority
- [ ] Implement support for Octopus Agile tariff
- [ ] Make the is_empty SoC configurable

## Low Priority
- [ ] Improve Docker container support and testing
- [ ] Add authentication to web interface for remote access security
- [ ] Improve accessibility features in web interface
- [ ] Migrate from pyModbusTCP to pymodbus for consistency and better maintainability
- [ ] Add support for additional EVSE devices beyond Wallbox Quasar
- [ ] Add support for power monitoring devices beyond Shelly EM

## Completed
- [x] Basic scheduling functionality
- [x] V2G and S2V capabilities
- [x] Web interface prototype
- [x] Add comprehensive API documentation (I'm considering this done because the Swagger UI is available)
- [x] Add more unit tests for edge cases
- [x] Fix schedule not being persisted
- [x] Fix log location, config location, and other files that need to be persisted
- [x] Move to new thread-based Wallbox driver which will reduce modbus errors

## Notes
- Priority levels are suggestions and may change based on user needs (please get in touch if you need something)
- Items may be moved to GitHub Issues for more detailed tracking
- See also: Roadmap section in README.md for user-facing features
