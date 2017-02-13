#!/bin/bash -x

# Email address being used for FXA goes here
export FXA_USER_EMAIL=""

export SERVER_URL="https://webextensions-settings.stage.mozaws.net/v1"

ls out.env || fxa-client -v --bearer --auth ${FXA_USER_EMAIL} --account-server https://api.accounts.firefox.com/v1 --oauth-server https://oauth.accounts.firefox.com/v1 --scopes "sync:addon_storage" -o out.env
source out.env

http -v GET "${SERVER_URL}/buckets/default/collections" Authorization:"Bearer ${OAUTH_BEARER_TOKEN}"

http -v GET "${SERVER_URL}/buckets/default/collections/storage-sync-crypto/records" Authorer ${OAUTH_BEARER_TOKEN}"

echo '{"data": {"payload": {"encrypted": "SmluZ28gdGVzdA=="}}}' | http -v POST "${SERVER_URL}/buckets/default/collections/3e0f013d2362aa4fa7b0db2fefb40011b9545d78dcca7aabc0d32f0b42f1733d/records" Authorization:"Bearer ${OAUTH_BEARER_TOKEN}"