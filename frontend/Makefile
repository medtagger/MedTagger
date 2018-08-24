MEDTAGGER__HOST_ON_SUBDIRECTORY ?= /
DYNAMIC_ENVIRONMENT_FILE = src/environments/environment.dynamic.ts
define DYNAMIC_ENVIRONMENT_CONTENT
// WARNING! This file was dynamically created during build time!
export const environment = {
    production: true,
    API_URL: window.location.origin + '$(MEDTAGGER__HOST_ON_SUBDIRECTORY)/api/v1',
    WEBSOCKET_URL: window.location.origin,
    WEBSOCKET_PATH: '$(MEDTAGGER__HOST_ON_SUBDIRECTORY)/socket.io'
};
endef

#
# Build
#

export DYNAMIC_ENVIRONMENT_CONTENT
create_dynamic_environment_configuration:
	@echo "$$DYNAMIC_ENVIRONMENT_CONTENT" > $(DYNAMIC_ENVIRONMENT_FILE)

#
# Development
#

run_frontend:
	ng serve --host 0.0.0.0

.PHONY: create_dynamic_environment_configuration run_frontend

