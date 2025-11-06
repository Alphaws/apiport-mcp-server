# Changelog

All notable changes to the ApiPort MCP Server will be documented in this file.

## [0.1.0] - 2025-11-06

### Added
- Initial release of ApiPort MCP Server
- Complete MCP protocol implementation
- JWT authentication with automatic token refresh
- 15 tools for task manager operations:
  - Project management (list, get)
  - Sprint management (list, get, create, activate, close)
  - Work item management (list, get, create, update)
  - Backlog management (get, bulk assign)
  - Sprint members (add)
  - Sprint reporting (generate report with statistics)
- Resource endpoints for projects, sprints, and backlogs
- Comprehensive documentation (README, INSTALL, examples)
- Example Claude Desktop configuration
- Python 3.10+ support
- Async/await API using httpx
- Automatic SSL handling (with disable option for development)
- Environment variable configuration
- Example .env file
- Installation via pip or uv

### Features
- **Auto-reconnect**: Automatically refreshes JWT tokens when expired
- **SSL Flexibility**: Can disable SSL verification for development
- **Rich Responses**: Formatted text responses with emoji indicators
- **Error Handling**: Comprehensive error messages and logging
- **Type Safety**: Full type hints throughout the codebase
- **Lazy Initialization**: Client initialized only when needed

### Tested
- ✅ Authentication endpoint
- ✅ List projects
- ✅ List sprints
- ✅ Create sprint (Sprint 2 created successfully)
- ✅ Token refresh logic
- ✅ Error handling

### Documentation
- README with comprehensive usage examples
- INSTALL guide with step-by-step instructions
- API client documentation
- Claude Desktop configuration examples
- Troubleshooting section

### Known Issues
- None at this time

### Security
- Credentials stored in environment variables
- SSL verification enabled by default
- Tokens cached securely in memory
- 1-hour token expiration with 5-minute refresh buffer

[0.1.0]: https://github.com/Alphaws/apiport-mcp-server/releases/tag/v0.1.0
