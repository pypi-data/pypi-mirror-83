# lt-hist

lt-hist helps you to plot and analyze the load test response time through time.

![v1_customer_me](./docs/_v1_customers_me.png)

## Getting started

```
$ pip install lt-hist

$ ifood-aws-login
...

$ AWS_PROFILE=creds-ifood-prod-legacy lt-hist --lt-name lt-account --days 10
Fetching, downloading and extracting the last 10 reports
Copying the files from the gatling report
Deleting the leftovers
Consolidating all the info into one file
Ploting the graphs and saving them inside the ./plots dir
Done
```

Then, check the plots directory to see the graphs.

Pay attention to the AWS_PROFILE var being exported. If you have doubts about
which one you should one, check `~/.aws/config` file and see the one under
ifood-prod-legacy profile.

```
$ ls -1 plots
(GET) _accounts_{account_id}_metadata_namespaces_public-orders.png
(GET) _accounts_{account_id}_metadata_namespaces_public-user-attributes.png
(GET) _accounts_{account_id}_namespaces.png
(get) _accounts.png
(get) _accounts_{id}.png
(get) _accounts_{id}_contact-methods.png
(get) _accounts_{id}_details.png
(put) _accounts.png
_accounts_-_preferences.png
_accounts_{accountUuid}_tags.png
_identity-providers.png
_identity-providers_FB_auth.png
_identity-providers_OTP_authentications:loadtest.png
_v1_customers_me.png
_v2_access_tokens.png
_v2_identity-providers_CONTINUE_AS_authentications.png
_v4_identity-providers.png
accounts (post).png
```