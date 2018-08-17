### STAGE 1: Build ###

# We label our stage as 'builder'
FROM node:8-alpine as builder

RUN apk add --no-cache make

COPY package.json package-lock.json ./

RUN npm set progress=false && npm config set depth 0 && npm cache clean --force

## Storing node modules on a separate layer will prevent unnecessary npm installs at each build
RUN npm install -g npm-install-retry
RUN npm-install-retry && mkdir /ng-app && cp -R ./node_modules ./ng-app

WORKDIR /ng-app

COPY . .

## Build the angular app in given mode and store the artifacts in dist folder
ARG PRODUCTION
ARG SUBDIRECTORY
RUN MEDTAGGER__HOST_ON_SUBDIRECTORY=$SUBDIRECTORY make create_dynamic_environment_configuration
RUN if [ "$PRODUCTION" = "1" ]; then $(npm bin)/ng build --prod --configuration=dynamic --base-href "$SUBDIRECTORY/"; else $(npm bin)/ng build --base-href "$SUBDIRECTORY/" --configuration=dynamic; fi


### STAGE 2: Setup ###

FROM nginx:1.13.3-alpine

## Copy our default nginx config
COPY nginx/default.conf /etc/nginx/conf.d/

## Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

## From 'builder' stage copy over the artifacts in dist folder to default nginx public folder
COPY --from=builder /ng-app/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]

